resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier  = "redshift-cluster"
  node_type           = "dc2.large"
  master_username     = var.redshift_username
  master_password     = var.redshift_password
  cluster_type        = "single-node"
  database_name       = var.redshift_db_name
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.redshift_sg.id]

  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.name
  publicly_accessible       = false
}

resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "redshift-subnet-group"
  subnet_ids = aws_subnet.private_subnet[*].id
}

resource "aws_security_group" "redshift_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # Allow access from ECS
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

