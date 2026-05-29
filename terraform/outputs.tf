output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "rds_endpoint" {
  description = "RDS 엔드포인트"
  value       = module.rds.rds_endpoint
}

output "api_gateway_url" {
  description = "API Gateway URL"
  value       = module.api_gateway.api_gateway_url
}

output "s3_bucket_name" {
  description = "S3 버킷 이름"
  value       = module.s3.s3_bucket_name
}

output "cloudfront_domain" {
  description = "CloudFront 도메인"
  value       = module.s3.cloudfront_domain
}