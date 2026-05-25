resource "aws_cloudwatch_log_group" "service" {
  name              = "/ecs/${local.name_prefix}"
  retention_in_days = var.log_retention_days
}
