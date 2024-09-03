resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier = "example-cluster"
  node_type          = "dc2.large"
  master_username    = var.redshift_username
  master_password    = var.redshift_password
  cluster_type       = "single-node"
  database_name      = var.redshift_db_name
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.redshift_sg.id]

  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.name
}

resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "redshift-subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_security_group" "redshift_sg" {
  name        = "redshift_sg"
  description = "Security group for Redshift"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "null_resource" "db_init" {
  provisioner "local-exec" {
    command = <<EOT
psql -h ${aws_redshift_cluster.redshift_cluster.endpoint} -U ${var.redshift_username} -d ${var.redshift_db_name} -f ${path.module}/../db/migrations/0001_schema.sql
EOT
    environment = {
      PGPASSWORD = var.redshift_password
    }
  }

  depends_on = [aws_redshift_cluster.redshift_cluster]
}

