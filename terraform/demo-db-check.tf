resource "aws_db_instance" "demo-db-check" {
  identifier = "demo-db-check"
  engine = "mysql"
  instance_class = "db.t3.micro"
  username = "admin"
  password = "SuperSecure123!"
  allocated_storage = 20
  skip_final_snapshot = true
}