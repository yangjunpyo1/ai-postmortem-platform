terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"

  project_name              = var.project_name
  environment               = var.environment
  vpc_cidr                  = var.vpc_cidr
  public_subnet_a_cidr      = var.public_subnet_a_cidr
  public_subnet_c_cidr      = var.public_subnet_c_cidr
  private_app_subnet_a_cidr = var.private_app_subnet_a_cidr
  private_app_subnet_c_cidr = var.private_app_subnet_c_cidr
  private_db_subnet_a_cidr  = var.private_db_subnet_a_cidr
  private_db_subnet_c_cidr  = var.private_db_subnet_c_cidr
}

module "rds" {
  source = "./modules/rds"

  project_name        = var.project_name
  environment         = var.environment
  rds_instance_type   = var.rds_instance_type
  rds_db_name         = var.rds_db_name
  rds_username        = var.rds_username
  rds_password        = var.rds_password
  private_db_subnet_a = module.vpc.private_db_subnet_a_id
  private_db_subnet_c = module.vpc.private_db_subnet_c_id
  vpc_id              = module.vpc.vpc_id
  lambda_sg_id        = module.lambda.lambda_security_group_id
  ec2_sg_id           = module.ec2.ec2_security_group_id
}

module "s3" {
  source = "./modules/s3"

  project_name = var.project_name
  environment  = var.environment
}

module "sqs" {
  source = "./modules/sqs"

  project_name = var.project_name
  environment  = var.environment
}

module "lambda" {
  source = "./modules/lambda"

  project_name         = var.project_name
  environment          = var.environment
  vpc_id               = module.vpc.vpc_id
  private_app_subnet_a = module.vpc.private_app_subnet_a_id
  private_app_subnet_c = module.vpc.private_app_subnet_c_id
  sqs_critical_arn     = module.sqs.sqs_critical_arn
  sqs_warning_arn      = module.sqs.sqs_warning_arn
  sqs_info_arn         = module.sqs.sqs_info_arn
  rds_endpoint         = module.rds.rds_endpoint
  rds_db_name          = var.rds_db_name
  rds_username         = var.rds_username
  rds_password         = var.rds_password
  slack_bot_token      = var.slack_bot_token
  slack_channel_id     = var.slack_channel_id
  claude_api_key       = var.claude_api_key
  ec2_instance_id      = module.ec2.ec2_instance_id
  cloudfront_domain    = module.s3.cloudfront_domain
}

module "api_gateway" {
  source = "./modules/api_gateway"

  project_name       = var.project_name
  environment        = var.environment
  lambda_fastapi_arn = module.lambda.lambda_fastapi_arn
}

module "cloudwatch" {
  source = "./modules/cloudwatch"

  project_name   = var.project_name
  environment    = var.environment
  sns_arn        = module.sqs.sns_arn
  api_gateway_id = module.api_gateway.api_gateway_id
}

module "ec2" {
  source = "./modules/ec2"

  project_name           = var.project_name
  environment            = var.environment
  ec2_instance_type      = var.ec2_instance_type
  vpc_id                 = module.vpc.vpc_id
  private_app_subnet_a   = module.vpc.private_app_subnet_a_id
  grafana_admin_password = var.grafana_admin_password
}