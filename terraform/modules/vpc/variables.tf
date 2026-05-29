variable "project_name" {
  description = "프로젝트 이름"
  type        = string
}

variable "environment" {
  description = "배포 환경"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR 블록"
  type        = string
}

variable "public_subnet_a_cidr" {
  description = "퍼블릭 서브넷 A존 CIDR"
  type        = string
}

variable "public_subnet_c_cidr" {
  description = "퍼블릭 서브넷 C존 CIDR"
  type        = string
}

variable "private_app_subnet_a_cidr" {
  description = "프라이빗 앱 서브넷 A존 CIDR"
  type        = string
}

variable "private_app_subnet_c_cidr" {
  description = "프라이빗 앱 서브넷 C존 CIDR"
  type        = string
}

variable "private_db_subnet_a_cidr" {
  description = "프라이빗 DB 서브넷 A존 CIDR"
  type        = string
}

variable "private_db_subnet_c_cidr" {
  description = "프라이빗 DB 서브넷 C존 CIDR"
  type        = string
}