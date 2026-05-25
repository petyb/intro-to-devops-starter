output "vpc_id" {
  value = aws_vpc.this.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  value = aws_ecs_service.fruitapi.name
}

output "task_definition_family" {
  value = aws_ecs_task_definition.fruitapi.family
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.service.name
}

output "service_security_group_id" {
  value = aws_security_group.service.id
}

output "rds_endpoint" {
  value = aws_db_instance.fruitapi.address
}

output "db_secret_arn" {
  value = aws_secretsmanager_secret.db.arn
}

output "alb_dns_name" {
  description = "Public DNS name of the FruitAPI load balancer."
  value       = aws_lb.fruitapi.dns_name
}

output "alb_url" {
  description = "HTTP URL of the FruitAPI service."
  value       = "http://${aws_lb.fruitapi.dns_name}"
}
