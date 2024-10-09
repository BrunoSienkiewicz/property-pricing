resource "aws_instance" "ec2" {
  ami           = "ami-0c55b159cbfafe1f0"  
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_subnet.id
  security_groups = [aws_security_group.ec2_sg.name]

  tags = {
    Name = "EC2 Instance"
  }

  # Provision the EC2 instance with a connection script to connect to RDS
  user_data = <<-EOF
                #!/bin/bash
                yum install -y postgresql
                psql -h ${aws_db_instance.postgres.address} -U admin -d mydatabase -c "SELECT 1"
              EOF

  depends_on = [aws_db_instance.postgres]
  key_name = "ec2"
}


