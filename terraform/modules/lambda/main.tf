# Lambda Security Group
resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-sg-lambda"
  description = "Lambda Security Group"
  vpc_id      = var.vpc_id

  # HTTPS (Slack, Claude API 호출)
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # MySQL (RDS 접근)
  egress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  tags = {
    Name        = "${var.project_name}-sg-lambda"
    Environment = var.environment
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-lambda-role"
    Environment = var.environment
  }
}

# IAM Policy for Lambda
resource "aws_iam_role_policy" "lambda" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:GetMetricData",
          "cloudwatch:GetMetricStatistics",
          "logs:FilterLogEvents",
          "logs:GetLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda 기본 실행 정책 연결
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Lambda 함수 - FastAPI 백엔드
resource "aws_lambda_function" "fastapi" {
  filename      = "${path.module}/lambda_fastapi.zip"
  function_name = "${var.project_name}-lambda-fastapi"
  role          = aws_iam_role.lambda.arn
  handler       = "app.main.handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 256

  vpc_config {
    subnet_ids         = [var.private_app_subnet_a]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      DB_HOST     = var.rds_endpoint
      DB_NAME     = var.rds_db_name
      DB_USER     = var.rds_username
      DB_PASSWORD = var.rds_password
    }
  }

  tags = {
    Name        = "${var.project_name}-lambda-fastapi"
    Environment = var.environment
  }
}

# Lambda 함수 - 알림 전송
resource "aws_lambda_function" "alarm" {
  filename      = "${path.module}/../../../lambda/alarm/lambda_alarm.zip"
  function_name = "${var.project_name}-lambda-alarm"
  role          = aws_iam_role.lambda.arn
  handler       = "handler.handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 256

  vpc_config {
    subnet_ids         = [var.private_app_subnet_a]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      SLACK_BOT_TOKEN  = var.slack_bot_token
      SLACK_CHANNEL_ID = var.slack_channel_id
    }
  }

  tags = {
    Name        = "${var.project_name}-lambda-alarm"
    Environment = var.environment
  }
}

# Lambda 함수 - Postmortem 자동화
resource "aws_lambda_function" "postmortem" {
  filename      = "${path.module}/../../../lambda/postmortem/lambda_postmortem.zip"
  function_name = "${var.project_name}-lambda-postmortem"
  role          = aws_iam_role.lambda.arn
  handler       = "handler.handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 256

  vpc_config {
    subnet_ids         = [var.private_app_subnet_c]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      SLACK_BOT_TOKEN  = var.slack_bot_token
      SLACK_CHANNEL_ID = var.slack_channel_id
      CLAUDE_API_KEY   = var.claude_api_key
      DASHBOARD_URL   = "https://${var.cloudfront_domain}"
      EC2_INSTANCE_ID = var.ec2_instance_id
      DB_HOST          = var.rds_endpoint
      DB_NAME          = var.rds_db_name
      DB_USER          = var.rds_username
      DB_PASSWORD      = var.rds_password
    }
  }

  tags = {
    Name        = "${var.project_name}-lambda-postmortem"
    Environment = var.environment
  }
}

# SQS → Lambda 트리거 - Critical
resource "aws_lambda_event_source_mapping" "critical" {
  event_source_arn = var.sqs_critical_arn
  function_name    = aws_lambda_function.alarm.arn
  batch_size       = 1
}