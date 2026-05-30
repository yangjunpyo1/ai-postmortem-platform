# EC2 Security Group
resource "aws_security_group" "ec2" {
  name        = "${var.project_name}-sg-ec2"
  description = "EC2 Grafana Security Group"
  vpc_id      = var.vpc_id

  # Grafana 포트 (VPC 내부에서만 접근)
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  # MySQL (RDS 접근)
  egress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  # HTTPS (CloudWatch 데이터 수집)
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
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

# IAM Role for EC2 (SSM + CloudWatch 접근)
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

# SSM 정책 연결 (터미널 접속용)
resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# CloudWatch 읽기 정책 연결 (Grafana용)
resource "aws_iam_role_policy_attachment" "ec2_cloudwatch" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2.name
}

# EC2 Instance (Grafana)
resource "aws_instance" "grafana" {
  ami                    = "ami-0f3a440bbcff3d043" # Amazon Linux 2023 (ap-northeast-2)
  instance_type          = var.ec2_instance_type
  subnet_id              = var.private_app_subnet_a
  vpc_security_group_ids = [aws_security_group.ec2.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2.name

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    docker run -d \
      --name grafana \
      -p 3000:3000 \
      --restart always \
      grafana/grafana
  EOF

  tags = {
    Name        = "${var.project_name}-ec2-grafana"
    Environment = var.environment
  }
}