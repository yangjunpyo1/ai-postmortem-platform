output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_a_id" {
  description = "퍼블릭 서브넷 A존 ID"
  value       = aws_subnet.public_a.id
}

output "public_subnet_c_id" {
  description = "퍼블릭 서브넷 C존 ID"
  value       = aws_subnet.public_c.id
}

output "private_app_subnet_a_id" {
  description = "프라이빗 앱 서브넷 A존 ID"
  value       = aws_subnet.private_app_a.id
}

output "private_app_subnet_c_id" {
  description = "프라이빗 앱 서브넷 C존 ID"
  value       = aws_subnet.private_app_c.id
}

output "private_db_subnet_a_id" {
  description = "프라이빗 DB 서브넷 A존 ID"
  value       = aws_subnet.private_db_a.id
}

output "private_db_subnet_c_id" {
  description = "프라이빗 DB 서브넷 C존 ID"
  value       = aws_subnet.private_db_c.id
}

output "nat_gateway_id" {
  description = "NAT Gateway ID"
  value       = aws_nat_gateway.main.id
}