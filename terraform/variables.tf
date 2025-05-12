variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_engine" {
  description = "RDS engine type (e.g., mysql or postgres)"
  type        = string
}

variable "env" {
  description = "Environment type (dev or prod)"
  type        = string
}