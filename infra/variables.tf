variable "project_name" {
  type    = string
  default = "property_pricing"
}

variable "redshift_db_name" {
  type    = string
  default = "property_pricing"
}

variable "redshift_username" {
  type      = string
  sensitive = true
}

variable "redshift_password" {
  type      = string
  sensitive = true
}

variable "subnet_ids" {
  type    = list(string)
  default = []
}

variable "vpc_id" {
  type    = string
  default = ""
}


