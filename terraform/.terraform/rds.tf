provider "aws" {
  region = "eu-north-1"
}

resource "aws_db_instance" "rds_instance" {
  identifier           = var.db_name
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "SuperSecure123!"
  skip_final_snapshot  = true
  publicly_accessible  = true
}