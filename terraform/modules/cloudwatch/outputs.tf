output "cpu_critical_alarm_arn" {
  description = "CPU Critical 알람 ARN"
  value       = aws_cloudwatch_metric_alarm.cpu_critical.arn
}

output "cpu_warning_alarm_arn" {
  description = "CPU Warning 알람 ARN"
  value       = aws_cloudwatch_metric_alarm.cpu_warning.arn
}

output "cpu_info_alarm_arn" {
  description = "CPU Info 알람 ARN"
  value       = aws_cloudwatch_metric_alarm.cpu_info.arn
}