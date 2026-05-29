variable "project_name" {
  description = "프로젝트 이름"
  type        = string
}

variable "environment" {
  description = "배포 환경"
  type        = string
}

variable "rds_instance_type" {
  description = "RDS 인스턴스 타입"
  type        = string
}

variable "rds_db_name" {
  description = "RDS 데이터베이스 이름"
  type        = string
}

variable "rds_username" {
  description = "RDS 마스터 사용자 이름"
  type        = string
}

variable "rds_password" {
  description = "RDS 마스터 비밀번호"
  type        = string
  sensitive   = true
}

variable "private_db_subnet_a" {
  description = "프라이빗 DB 서브넷 A존 ID"
  type        = string
}

variable "private_db_subnet_c" {
  description = "프라이빗 DB 서브넷 C존 ID"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "lambda_sg_id" {
  description = "Lambda 보안 그룹 ID"
  type        = string
}