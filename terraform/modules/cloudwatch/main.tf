# CloudWatch Alarm - Critical (CPU 90% 이상)
resource "aws_cloudwatch_metric_alarm" "cpu_critical" {
  alarm_name          = "${var.project_name}-cpu-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 90
  alarm_description   = "CPU 사용률 90% 초과 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    AutoScalingGroupName = "${var.project_name}-asg"
  }

  tags = {
    Name        = "${var.project_name}-cpu-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Alarm - Warning (CPU 70% 이상)
resource "aws_cloudwatch_metric_alarm" "cpu_warning" {
  alarm_name          = "${var.project_name}-cpu-warning"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 70
  alarm_description   = "CPU 사용률 70% 초과 - Warning"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    AutoScalingGroupName = "${var.project_name}-asg"
  }

  tags = {
    Name        = "${var.project_name}-cpu-warning"
    Environment = var.environment
    Severity    = "warning"
  }
}

# CloudWatch Alarm - Info (CPU 60% 이상)
resource "aws_cloudwatch_metric_alarm" "cpu_info" {
  alarm_name          = "${var.project_name}-cpu-info"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 60
  alarm_description   = "CPU 사용률 60% 초과 - Info"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    AutoScalingGroupName = "${var.project_name}-asg"
  }

  tags = {
    Name        = "${var.project_name}-cpu-info"
    Environment = var.environment
    Severity    = "info"
  }
}

# CloudWatch Alarm - 메모리 사용률 Critical (90% 이상)
resource "aws_cloudwatch_metric_alarm" "memory_critical" {
  alarm_name          = "${var.project_name}-memory-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "mem_used_percent"
  namespace           = "CWAgent"
  period              = 60
  statistic           = "Average"
  threshold           = 90
  alarm_description   = "메모리 사용률 90% 초과 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  tags = {
    Name        = "${var.project_name}-memory-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Alarm - Lambda 에러율 Critical
resource "aws_cloudwatch_metric_alarm" "lambda_errors_critical" {
  alarm_name          = "${var.project_name}-lambda-errors-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Lambda 에러 5회 이상 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  tags = {
    Name        = "${var.project_name}-lambda-errors-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Alarm - Lambda 응답 시간 Warning (5초 이상)
resource "aws_cloudwatch_metric_alarm" "lambda_duration_warning" {
  alarm_name          = "${var.project_name}-lambda-duration-warning"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Average"
  threshold           = 5000
  alarm_description   = "Lambda 응답 시간 5초 이상 - Warning"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  tags = {
    Name        = "${var.project_name}-lambda-duration-warning"
    Environment = var.environment
    Severity    = "warning"
  }
}

# CloudWatch Alarm - RDS 연결 오류 Critical
resource "aws_cloudwatch_metric_alarm" "rds_connections_critical" {
  alarm_name          = "${var.project_name}-rds-connections-critical"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Average"
  threshold           = 0
  alarm_description   = "RDS 연결 오류 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    DBInstanceIdentifier = "${var.project_name}-rds"
  }

  tags = {
    Name        = "${var.project_name}-rds-connections-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Alarm - RDS 쿼리 지연 Warning
resource "aws_cloudwatch_metric_alarm" "rds_latency_warning" {
  alarm_name          = "${var.project_name}-rds-latency-warning"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "ReadLatency"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Average"
  threshold           = 0.1
  alarm_description   = "RDS 쿼리 지연 100ms 이상 - Warning"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    DBInstanceIdentifier = "${var.project_name}-rds"
  }

  tags = {
    Name        = "${var.project_name}-rds-latency-warning"
    Environment = var.environment
    Severity    = "warning"
  }
}

# CloudWatch Alarm - RDS 스토리지 부족 Warning
resource "aws_cloudwatch_metric_alarm" "rds_storage_warning" {
  alarm_name          = "${var.project_name}-rds-storage-warning"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Average"
  threshold           = 5000000000
  alarm_description   = "RDS 스토리지 5GB 이하 - Warning"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    DBInstanceIdentifier = "${var.project_name}-rds"
  }

  tags = {
    Name        = "${var.project_name}-rds-storage-warning"
    Environment = var.environment
    Severity    = "warning"
  }
}

# CloudWatch Alarm - NAT Gateway 오류 Critical
resource "aws_cloudwatch_metric_alarm" "natgw_errors_critical" {
  alarm_name          = "${var.project_name}-natgw-errors-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "ErrorPortAllocation"
  namespace           = "AWS/NATGateway"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "NAT Gateway 포트 할당 오류 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  tags = {
    Name        = "${var.project_name}-natgw-errors-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Alarm - API Gateway 4xx 에러율 Warning
resource "aws_cloudwatch_metric_alarm" "apigw_4xx_warning" {
  alarm_name          = "${var.project_name}-apigw-4xx-warning"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "4xx"
  namespace           = "AWS/ApiGateway"
  period              = 60
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "API Gateway 4xx 에러 10회 이상 - Warning"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    ApiId = var.api_gateway_id
  }

  tags = {
    Name        = "${var.project_name}-apigw-4xx-warning"
    Environment = var.environment
    Severity    = "warning"
  }
}

# CloudWatch Alarm - API Gateway 5xx 에러율 Critical
resource "aws_cloudwatch_metric_alarm" "apigw_5xx_critical" {
  alarm_name          = "${var.project_name}-apigw-5xx-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "5xx"
  namespace           = "AWS/ApiGateway"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "API Gateway 5xx 에러 5회 이상 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  dimensions = {
    ApiId = var.api_gateway_id
  }

  tags = {
    Name        = "${var.project_name}-apigw-5xx-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Log Group - Lambda FastAPI
resource "aws_cloudwatch_log_group" "lambda_fastapi" {
  name              = "/aws/lambda/${var.project_name}-lambda-fastapi"
  retention_in_days = 30

  tags = {
    Name        = "${var.project_name}-lambda-fastapi-logs"
    Environment = var.environment
  }
}

# CloudWatch Log Group - Lambda Alarm
resource "aws_cloudwatch_log_group" "lambda_alarm" {
  name              = "/aws/lambda/${var.project_name}-lambda-alarm"
  retention_in_days = 30

  tags = {
    Name        = "${var.project_name}-lambda-alarm-logs"
    Environment = var.environment
  }
}

# CloudWatch Log Group - Lambda Postmortem
resource "aws_cloudwatch_log_group" "lambda_postmortem" {
  name              = "/aws/lambda/${var.project_name}-lambda-postmortem"
  retention_in_days = 30

  tags = {
    Name        = "${var.project_name}-lambda-postmortem-logs"
    Environment = var.environment
  }
}

# 에러 로그 필터 - Lambda FastAPI
resource "aws_cloudwatch_log_metric_filter" "lambda_fastapi_errors" {
  name           = "${var.project_name}-fastapi-errors"
  log_group_name = aws_cloudwatch_log_group.lambda_fastapi.name
  pattern        = "ERROR"

  metric_transformation {
    name      = "FastAPIErrorCount"
    namespace = "${var.project_name}/Lambda"
    value     = "1"
  }
}

# 에러 로그 필터 - Lambda Postmortem
resource "aws_cloudwatch_log_metric_filter" "lambda_postmortem_errors" {
  name           = "${var.project_name}-postmortem-errors"
  log_group_name = aws_cloudwatch_log_group.lambda_postmortem.name
  pattern        = "ERROR"

  metric_transformation {
    name      = "PostmortemErrorCount"
    namespace = "${var.project_name}/Lambda"
    value     = "1"
  }
}

# 경고 로그 필터 - Lambda FastAPI
resource "aws_cloudwatch_log_metric_filter" "lambda_fastapi_warnings" {
  name           = "${var.project_name}-fastapi-warnings"
  log_group_name = aws_cloudwatch_log_group.lambda_fastapi.name
  pattern        = "WARNING"

  metric_transformation {
    name      = "FastAPIWarningCount"
    namespace = "${var.project_name}/Lambda"
    value     = "1"
  }
}

# CloudWatch Alarm - FastAPI 에러 로그 Critical
resource "aws_cloudwatch_metric_alarm" "fastapi_log_errors_critical" {
  alarm_name          = "${var.project_name}-fastapi-log-errors-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "FastAPIErrorCount"
  namespace           = "${var.project_name}/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "FastAPI 에러 로그 5회 이상 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  tags = {
    Name        = "${var.project_name}-fastapi-log-errors-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}

# CloudWatch Alarm - Postmortem 에러 로그 Critical
resource "aws_cloudwatch_metric_alarm" "postmortem_log_errors_critical" {
  alarm_name          = "${var.project_name}-postmortem-log-errors-critical"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "PostmortemErrorCount"
  namespace           = "${var.project_name}/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Postmortem 에러 로그 5회 이상 - Critical"
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]

  tags = {
    Name        = "${var.project_name}-postmortem-log-errors-critical"
    Environment = var.environment
    Severity    = "critical"
  }
}