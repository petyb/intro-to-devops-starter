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
