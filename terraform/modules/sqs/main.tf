# SNS Topic
resource "aws_sns_topic" "alarm" {
  name = "${var.project_name}-sns"

  tags = {
    Name        = "${var.project_name}-sns"
    Environment = var.environment
  }
}

# SQS Queue - Critical
resource "aws_sqs_queue" "critical" {
  name                       = "${var.project_name}-critical-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 345600
  receive_wait_time_seconds  = 20

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.critical_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Name        = "${var.project_name}-critical-queue"
    Environment = var.environment
  }
}

# SQS Queue - Warning
resource "aws_sqs_queue" "warning" {
  name                       = "${var.project_name}-warning-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 345600
  receive_wait_time_seconds  = 20

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.warning_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Name        = "${var.project_name}-warning-queue"
    Environment = var.environment
  }
}

# SQS Queue - Info
resource "aws_sqs_queue" "info" {
  name                       = "${var.project_name}-info-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 345600
  receive_wait_time_seconds  = 20

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.info_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Name        = "${var.project_name}-info-queue"
    Environment = var.environment
  }
}

# Dead Letter Queue - Critical
resource "aws_sqs_queue" "critical_dlq" {
  name                      = "${var.project_name}-critical-dlq"
  message_retention_seconds = 1209600

  tags = {
    Name        = "${var.project_name}-critical-dlq"
    Environment = var.environment
  }
}

# Dead Letter Queue - Warning
resource "aws_sqs_queue" "warning_dlq" {
  name                      = "${var.project_name}-warning-dlq"
  message_retention_seconds = 1209600

  tags = {
    Name        = "${var.project_name}-warning-dlq"
    Environment = var.environment
  }
}

# Dead Letter Queue - Info
resource "aws_sqs_queue" "info_dlq" {
  name                      = "${var.project_name}-info-dlq"
  message_retention_seconds = 1209600

  tags = {
    Name        = "${var.project_name}-info-dlq"
    Environment = var.environment
  }
}

# SNS → SQS 구독 - Critical
resource "aws_sns_topic_subscription" "critical" {
  topic_arn = aws_sns_topic.alarm.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.critical.arn
}

# SNS → SQS 구독 - Warning
resource "aws_sns_topic_subscription" "warning" {
  topic_arn = aws_sns_topic.alarm.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.warning.arn
}

# SNS → SQS 구독 - Info
resource "aws_sns_topic_subscription" "info" {
  topic_arn = aws_sns_topic.alarm.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.info.arn
}

# SQS 정책 - Lambda가 접근할 수 있도록
resource "aws_sqs_queue_policy" "critical" {
  queue_url = aws_sqs_queue.critical.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "sns.amazonaws.com" }
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.critical.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.alarm.arn
          }
        }
      }
    ]
  })
}

resource "aws_sqs_queue_policy" "warning" {
  queue_url = aws_sqs_queue.warning.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "sns.amazonaws.com" }
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.warning.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.alarm.arn
          }
        }
      }
    ]
  })
}

resource "aws_sqs_queue_policy" "info" {
  queue_url = aws_sqs_queue.info.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "sns.amazonaws.com" }
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.info.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.alarm.arn
          }
        }
      }
    ]
  })
}