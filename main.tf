provider "aws" {
  region = "us-east-1"
}

# Security Group
resource "aws_security_group" "python_sg" {
  name        = "python-security-group"
  description = "Security group con puerto 8000 abierto"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTP on port 8000"
    from_port   = 8000
    to_port     = 8000
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

# Key Pair
resource "aws_key_pair" "backend-ssh" {
  key_name   = "backend-ssh"
  public_key = file("backend-ssh.key.pub")
}

# EC2 Instance
resource "aws_instance" "python_server" {
  ami           = "ami-01816d07b1128cd2d"
  instance_type = "t2.large"
  key_name      = aws_key_pair.backend-ssh.key_name
  vpc_security_group_ids = [aws_security_group.python_sg.id]

  tags = {
    Name = "Backend-Chess-App"
  }

  depends_on = [aws_key_pair.backend-ssh, aws_security_group.python_sg]

  provisioner "file" {
    source      = "./chess_expert_store"          
    destination = "/tmp/chess_expert_store"       
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")       
    }
  }

  provisioner "file" {
    source      = "./docs"          
    destination = "/tmp/docs"       
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")       
    }
  }

  provisioner "file" {
    source      = "./src"          
    destination = "/tmp/src"       
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")       
    }
  }

  provisioner "file" {
    source      = "./main.py"          
    destination = "/tmp/main.py"       
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")       
    }
  }

  provisioner "file" {
    source      = "./.env"          
    destination = "/tmp/.env"       
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")       
    }
  }

  provisioner "file" {
    source      = "./requirements.txt"          
    destination = "/tmp/requirements.txt"       
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")       
    }
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("backend-ssh.key")
    }

    inline = [
      "sudo yum update -y",
      "sudo yum install python3.11 python3-pip -y",
      "sudo yum install -y coreutils",
      "mkdir -p /home/ec2-user/proyecto",
      "sudo mv /tmp/chess_expert_store /home/ec2-user/proyecto/",
      "sudo mv /tmp/docs /home/ec2-user/proyecto/",
      "sudo mv /tmp/src /home/ec2-user/proyecto/",
      "sudo mv /tmp/main.py /home/ec2-user/proyecto/",
      "sudo mv /tmp/.env /home/ec2-user/proyecto/",
      "sudo mv /tmp/requirements.txt /home/ec2-user/proyecto/",
      "sudo chown -R ec2-user:ec2-user /home/ec2-user/proyecto",
      "cd /home/ec2-user/proyecto",
      "python3.11 -m venv venv",
      "source venv/bin/activate",
      "pip install --no-cache-dir --upgrade -r requirements.txt",
      "echo '#!/bin/bash' > /home/ec2-user/proyecto/setup_and_run.sh",
      "echo 'cd /home/ec2-user/proyecto' >> /home/ec2-user/proyecto/setup_and_run.sh",
      "echo 'source venv/bin/activate' >> /home/ec2-user/proyecto/setup_and_run.sh",
      "echo 'nohup uvicorn src.app:app --host 0.0.0.0 --port 8000 > nohup.out 2>&1 &' >> /home/ec2-user/proyecto/setup_and_run.sh",
      "chmod +x /home/ec2-user/proyecto/setup_and_run.sh",
      "sudo -u ec2-user bash /home/ec2-user/proyecto/setup_and_run.sh"
    ]
  }
}

# Elastic IP
resource "aws_eip_association" "associate_eip" {
  instance_id   = aws_instance.python_server.id
  allocation_id = "eipalloc-049d33f0549d6d05e"
}
