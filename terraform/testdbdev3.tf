resource "aws_db_instance" "testdbdev3" {
  identifier = "testdbdev3"
  engine = "mysql"
  instance_class = "db.t3.micro"
  username = "admin"
  password = "SuperSecure123!"
  allocated_storage = 20
  skip_final_snapshot = true
}