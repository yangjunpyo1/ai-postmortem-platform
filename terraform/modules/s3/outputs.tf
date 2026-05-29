output "s3_bucket_name" {
  description = "S3 버킷 이름"
  value       = aws_s3_bucket.frontend.bucket
}

output "s3_bucket_arn" {
  description = "S3 버킷 ARN"
  value       = aws_s3_bucket.frontend.arn
}

output "cloudfront_domain" {
  description = "CloudFront 도메인"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "cloudfront_id" {
  description = "CloudFront ID"
  value       = aws_cloudfront_distribution.frontend.id
}