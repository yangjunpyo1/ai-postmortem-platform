output "sns_arn" {
  description = "SNS Topic ARN"
  value       = aws_sns_topic.alarm.arn
}

output "sqs_critical_arn" {
  description = "SQS Critical Queue ARN"
  value       = aws_sqs_queue.critical.arn
}

output "sqs_warning_arn" {
  description = "SQS Warning Queue ARN"
  value       = aws_sqs_queue.warning.arn
}

output "sqs_info_arn" {
  description = "SQS Info Queue ARN"
  value       = aws_sqs_queue.info.arn
}