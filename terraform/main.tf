data "aws_secretsmanager_secret_version" "rds_credentials" {
  secret_id = "rds/credentials"
}

locals {
  rds_creds = jsondecode(data.aws_secretsmanager_secret_version.rds_credentials.secret_string)
}

resource "aws_db_instance" "this" {
  identifier              = var.db_name
  engine                  = var.db_engine
  instance_class          = var.env == "prod" ? "db.t3.small" : "db.t3.micro"
  allocated_storage       = 20
  skip_final_snapshot     = true
  publicly_accessible     = false
  db_name                 = var.db_name

  # 🔐 נמשוך את המשתמש והסיסמה מתוך הסיקרט
  username                = local.rds_creds.username
  password                = local.rds_creds.password
}