variable "project_name" {
  description = "프로젝트 이름"
  type        = string
}

variable "environment" {
  description = "배포 환경"
  type        = string
}

variable "lambda_fastapi_arn" {
  description = "FastAPI Lambda ARN"
  type        = string
}