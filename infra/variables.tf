variable "project_name" {
  type    = string
  default = "property-pricing"
}

variable "db_name" {
  type    = string
  default = "property_pricing"
}

variable "db_username" {
  type      = string
  sensitive = true
}

variable "db_password" {
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


