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