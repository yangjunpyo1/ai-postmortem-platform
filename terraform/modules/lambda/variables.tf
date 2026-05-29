variable "project_name" {
  description = "프로젝트 이름"
  type        = string
}

variable "environment" {
  description = "배포 환경"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "private_app_subnet_a" {
  description = "프라이빗 앱 서브넷 A존 ID"
  type        = string
}

variable "private_app_subnet_c" {
  description = "프라이빗 앱 서브넷 C존 ID"
  type        = string
}

variable "sqs_critical_arn" {
  description = "SQS Critical Queue ARN"
  type        = string
}

variable "sqs_warning_arn" {
  description = "SQS Warning Queue ARN"
  type        = string
}

variable "sqs_info_arn" {
  description = "SQS Info Queue ARN"
  type        = string
}

variable "rds_endpoint" {
  description = "RDS 엔드포인트"
  type        = string
}

variable "rds_db_name" {
  description = "RDS 데이터베이스 이름"
  type        = string
}

variable "rds_username" {
  description = "RDS 사용자 이름"
  type        = string
}

variable "rds_password" {
  description = "RDS 비밀번호"
  type        = string
  sensitive   = true
}

variable "slack_bot_token" {
  description = "Slack Bot Token"
  type        = string
  sensitive   = true
}

variable "slack_channel_id" {
  description = "Slack Channel ID"
  type        = string
}

variable "claude_api_key" {
  description = "Claude API Key"
  type        = string
  sensitive   = true
}