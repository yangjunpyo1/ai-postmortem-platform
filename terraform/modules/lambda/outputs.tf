output "lambda_fastapi_arn" {
  description = "FastAPI Lambda ARN"
  value       = aws_lambda_function.fastapi.arn
}

output "lambda_alarm_arn" {
  description = "알림 전송 Lambda ARN"
  value       = aws_lambda_function.alarm.arn
}

output "lambda_postmortem_arn" {
  description = "Postmortem 자동화 Lambda ARN"
  value       = aws_lambda_function.postmortem.arn
}

output "lambda_security_group_id" {
  description = "Lambda 보안 그룹 ID"
  value       = aws_security_group.lambda.id
}