# RDS Security Group
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-sg-rds"
  description = "RDS Security Group"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [var.lambda_sg_id]
  }

  tags = {
    Name        = "${var.project_name}-sg-rds"
    Environment = var.environment
  }
}

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [var.private_db_subnet_a, var.private_db_subnet_c]

  tags = {
    Name        = "${var.project_name}-db-subnet-group"
    Environment = var.environment
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier        = "${var.project_name}-rds"
  engine            = "mysql"
  engine_version    = "8.0"
  instance_class    = var.rds_instance_type
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = var.rds_db_name
  username = var.rds_username
  password = var.rds_password
  port     = 3306

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  multi_az               = false
  publicly_accessible    = false
  skip_final_snapshot    = true
  deletion_protection    = false

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  tags = {
    Name        = "${var.project_name}-rds"
    Environment = var.environment
  }
}