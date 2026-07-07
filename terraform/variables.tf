variable "aws_region" {
  description = "AWS 리전"
  type        = string
  default     = "ap-northeast-2"
}

variable "project_name" {
  description = "프로젝트 이름"
  type        = string
  default     = "yp"
}

variable "environment" {
  description = "배포 환경"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "VPC CIDR 블록"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_a_cidr" {
  description = "퍼블릭 서브넷 A존 CIDR"
  type        = string
  default     = "10.0.10.0/24"
}

variable "public_subnet_c_cidr" {
  description = "퍼블릭 서브넷 C존 CIDR"
  type        = string
  default     = "10.0.100.0/24"
}

variable "private_app_subnet_a_cidr" {
  description = "프라이빗 앱 서브넷 A존 CIDR"
  type        = string
  default     = "10.0.20.0/24"
}

variable "private_app_subnet_c_cidr" {
  description = "프라이빗 앱 서브넷 C존 CIDR"
  type        = string
  default     = "10.0.120.0/24"
}

variable "private_db_subnet_a_cidr" {
  description = "프라이빗 DB 서브넷 A존 CIDR"
  type        = string
  default     = "10.0.30.0/24"
}

variable "private_db_subnet_c_cidr" {
  description = "프라이빗 DB 서브넷 C존 CIDR"
  type        = string
  default     = "10.0.130.0/24"
}

variable "ec2_instance_type" {
  description = "EC2 인스턴스 타입 (Grafana)"
  type        = string
  default     = "t2.micro"
}

variable "grafana_admin_password" {
  description = "Grafana admin 비밀번호"
  type        = string
  sensitive   = true
}

variable "rds_instance_type" {
  description = "RDS 인스턴스 타입"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_db_name" {
  description = "RDS 데이터베이스 이름"
  type        = string
  default     = "postmortem"
}

variable "rds_username" {
  description = "RDS 마스터 사용자 이름"
  type        = string
  default     = "yangpyo"
}

variable "rds_password" {
  description = "RDS 마스터 비밀번호"
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