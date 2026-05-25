resource "aws_secretsmanager_secret" "db" {
  name                    = "${local.name_prefix}/db"
  description             = "FruitAPI MySQL credentials"
  recovery_window_in_days = 0 # let `terraform destroy` actually delete it
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    DB_HOST     = aws_db_instance.fruitapi.address
    DB_PORT     = tostring(aws_db_instance.fruitapi.port)
    DB_NAME     = aws_db_instance.fruitapi.db_name
    DB_USER     = aws_db_instance.fruitapi.username
    DB_PASSWORD = random_password.db.result
  })
}

# Allow the ECS task execution role to fetch this secret at task launch.
data "aws_iam_policy_document" "read_db_secret" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.db.arn]
  }
}

resource "aws_iam_policy" "read_db_secret" {
  name   = "${local.name_prefix}-read-db-secret"
  policy = data.aws_iam_policy_document.read_db_secret.json
}

resource "aws_iam_role_policy_attachment" "exec_read_db_secret" {
  role       = aws_iam_role.task_execution.name
  policy_arn = aws_iam_policy.read_db_secret.arn
}
