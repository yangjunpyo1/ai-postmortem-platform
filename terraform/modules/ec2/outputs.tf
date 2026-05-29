output "ec2_instance_id" {
  description = "EC2 인스턴스 ID"
  value       = aws_instance.grafana.id
}

output "ec2_private_ip" {
  description = "EC2 프라이빗 IP"
  value       = aws_instance.grafana.private_ip
}

output "ec2_security_group_id" {
  description = "EC2 보안 그룹 ID"
  value       = aws_security_group.ec2.id
}