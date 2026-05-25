resource "aws_db_subnet_group" "this" {
  name       = "${local.name_prefix}-db"
  subnet_ids = aws_subnet.public[*].id

  tags = { Name = "${local.name_prefix}-db-subnets" }
}

resource "aws_security_group" "db" {
  name        = "${local.name_prefix}-db"
  description = "MySQL access from FruitAPI tasks only"
  vpc_id      = aws_vpc.this.id

  ingress {
    description     = "MySQL from service SG"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.service.id]
  }

  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${local.name_prefix}-db-sg" }
}

resource "random_password" "db" {
  length      = 24
  special     = false # avoid '@' / ':' / '/' which complicate the URL
  min_lower   = 4
  min_upper   = 4
  min_numeric = 4
}

resource "aws_db_instance" "fruitapi" {
  identifier              = "${local.name_prefix}-mysql"
  engine                  = "mysql"
  engine_version          = "8.4"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  storage_type            = "gp3"
  storage_encrypted       = true
  db_name                 = "fruitapi"
  username                = "fruitapi"
  password                = random_password.db.result
  db_subnet_group_name    = aws_db_subnet_group.this.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  publicly_accessible     = false
  multi_az                = false
  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false
  apply_immediately       = true

  tags = { Name = "${local.name_prefix}-mysql" }
}
