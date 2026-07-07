# EC2 Security Group
resource "aws_security_group" "ec2" {
  name        = "${var.project_name}-sg-ec2"
  description = "EC2 Grafana Security Group"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-sg-ec2"
    Environment = var.environment
  }
}

# IAM Role for EC2
resource "aws_iam_role" "ec2" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-ec2-role"
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "ec2_cloudwatch" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "ec2_cloudwatch_agent" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2.name
}

# EC2 Instance (Grafana)
resource "aws_instance" "grafana" {
  ami                    = "ami-0f3a440bbcff3d043"
  instance_type          = var.ec2_instance_type
  subnet_id              = var.private_app_subnet_a
  vpc_security_group_ids = [aws_security_group.ec2.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2.name

  user_data = <<EOF
#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

apt-get update -y
curl -fsSL https://get.docker.com | sh
systemctl start docker
systemctl enable docker

# AWS CLI v2 설치 (apt 버전 대신 공식 설치)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
apt-get install -y unzip
unzip /tmp/awscliv2.zip -d /tmp
/tmp/aws/install
export PATH=$PATH:/usr/local/bin

# CloudWatch Agent 설치
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i amazon-cloudwatch-agent.deb

# CloudWatch Agent 설정
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'CWCONFIG'
{
  "metrics": {
    "namespace": "CWAgent",
    "metrics_collected": {
      "mem": {
        "measurement": ["mem_used_percent"],
        "metrics_collection_interval": 60
      },
      "disk": {
        "measurement": ["disk_used_percent"],
        "resources": ["/"],
        "metrics_collection_interval": 60
      }
    }
  }
}
CWCONFIG

# CloudWatch Agent 시작
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
  -s

# Grafana provisioning 디렉토리 생성
mkdir -p /etc/grafana/provisioning/datasources
mkdir -p /etc/grafana/provisioning/dashboards
mkdir -p /etc/grafana/dashboards

# CloudWatch 데이터 소스 자동 설정
cat > /etc/grafana/provisioning/datasources/cloudwatch.yaml << 'YAML'
apiVersion: 1
datasources:
  - name: cloudwatch
    type: cloudwatch
    uid: cloudwatch
    access: proxy
    isDefault: true
    jsonData:
      authType: default
      defaultRegion: ap-northeast-2
YAML

# 대시보드 프로비저닝 설정
cat > /etc/grafana/provisioning/dashboards/dashboard.yaml << 'YAML'
apiVersion: 1
providers:
  - name: default
    folder: ''
    type: file
    options:
      path: /etc/grafana/dashboards
YAML

# AI Postmortem 대시보드 JSON
cat > /etc/grafana/dashboards/postmortem.json << 'DASHBOARD'
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {"type": "grafana", "uid": "-- Grafana --"},
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {"legend": false, "tooltip": false, "viz": false},
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {"type": "linear"},
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": {"group": "A", "mode": "none"},
            "thresholdsStyle": {"mode": "off"}
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [{"color": "green", "value": null}, {"color": "red", "value": 80}]
          }
        },
        "overrides": []
      },
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
      "id": 1,
      "options": {
        "legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": true},
        "tooltip": {"mode": "single", "sort": "none"}
      },
      "targets": [
        {
          "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
          "dimensions": {},
          "expression": "",
          "id": "",
          "label": "",
          "logGroups": [],
          "matchExact": false,
          "metricEditorMode": 0,
          "metricName": "CPUUtilization",
          "metricQueryType": 0,
          "namespace": "AWS/EC2",
          "period": "60",
          "queryMode": "Metrics",
          "refId": "A",
          "region": "ap-northeast-2",
          "sqlExpression": "",
          "statistic": "Average"
        }
      ],
      "title": "CPU 사용률",
      "type": "timeseries"
    },
    {
      "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {"legend": false, "tooltip": false, "viz": false},
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {"type": "linear"},
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": {"group": "A", "mode": "none"},
            "thresholdsStyle": {"mode": "off"}
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [{"color": "green", "value": null}, {"color": "red", "value": 80}]
          }
        },
        "overrides": []
      },
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
      "id": 2,
      "options": {
        "legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": true},
        "tooltip": {"mode": "single", "sort": "none"}
      },
      "targets": [
        {
          "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
          "dimensions": {},
          "expression": "",
          "id": "",
          "label": "",
          "logGroups": [],
          "matchExact": false,
          "metricEditorMode": 0,
          "metricName": "mem_used_percent",
          "metricQueryType": 0,
          "namespace": "CWAgent",
          "period": "60",
          "queryMode": "Metrics",
          "refId": "A",
          "region": "ap-northeast-2",
          "sqlExpression": "",
          "statistic": "Average"
        }
      ],
      "title": "메모리 사용률",
      "type": "timeseries"
    },
    {
      "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {"legend": false, "tooltip": false, "viz": false},
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {"type": "linear"},
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": {"group": "A", "mode": "none"},
            "thresholdsStyle": {"mode": "off"}
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [{"color": "green", "value": null}, {"color": "red", "value": 80}]
          }
        },
        "overrides": []
      },
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
      "id": 3,
      "options": {
        "legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": true},
        "tooltip": {"mode": "single", "sort": "none"}
      },
      "targets": [
        {
          "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
          "dimensions": {},
          "expression": {},
          "id": "",
          "label": "",
          "logGroups": [],
          "matchExact": false,
          "metricEditorMode": 0,
          "metricName": "Errors",
          "metricQueryType": 0,
          "namespace": "AWS/Lambda",
          "period": "60",
          "queryMode": "Metrics",
          "refId": "A",
          "region": "ap-northeast-2",
          "sqlExpression": "",
          "statistic": "Sum"
        }
      ],
      "title": "Lambda 에러율",
      "type": "timeseries"
    },
    {
      "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {"legend": false, "tooltip": false, "viz": false},
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {"type": "linear"},
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": {"group": "A", "mode": "none"},
            "thresholdsStyle": {"mode": "off"}
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [{"color": "green", "value": null}, {"color": "red", "value": 80}]
          }
        },
        "overrides": []
      },
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
      "id": 4,
      "options": {
        "legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": true},
        "tooltip": {"mode": "single", "sort": "none"}
      },
      "targets": [
        {
          "datasource": {"type": "cloudwatch", "uid": "cloudwatch"},
          "dimensions": {},
          "expression": "",
          "id": "",
          "label": "",
          "logGroups": [],
          "matchExact": false,
          "metricEditorMode": 0,
          "metricName": "Duration",
          "metricQueryType": 0,
          "namespace": "AWS/Lambda",
          "period": "60",
          "queryMode": "Metrics",
          "refId": "A",
          "region": "ap-northeast-2",
          "sqlExpression": "",
          "statistic": "Average"
        }
      ],
      "title": "Lambda 응답 시간",
      "type": "timeseries"
    }
  ],
  "refresh": "30s",
  "schemaVersion": 39,
  "tags": [],
  "templating": {"list": []},
  "time": {"from": "now-1h", "to": "now"},
  "timepicker": {},
  "timezone": "",
  "title": "AI Postmortem 모니터링",
  "uid": "postmortem-dashboard",
  "version": 1,
  "weekStart": ""
}
DASHBOARD

# Grafana 실행 (버전 10.4.3으로 고정)
docker run -d \
  --name grafana \
  -p 3000:3000 \
  --restart always \
  -e GF_SECURITY_ADMIN_PASSWORD='${var.grafana_admin_password}' \
  -v grafana-storage:/var/lib/grafana \
  -v /etc/grafana/provisioning:/etc/grafana/provisioning \
  -v /etc/grafana/dashboards:/etc/grafana/dashboards \
  grafana/grafana:10.4.3

# IMDS hop limit 설정
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
REGION=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/region)
/usr/local/bin/aws ec2 modify-instance-metadata-options \
  --instance-id $INSTANCE_ID \
  --http-put-response-hop-limit 2 \
  --http-endpoint enabled \
  --region $REGION
EOF

  tags = {
    Name        = "${var.project_name}-ec2-grafana"
    Environment = var.environment
  }
}