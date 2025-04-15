terraform {

  # Configure the Terraform AWS Provider
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_security_group" "ec2_sg2" {
  description = "Allow SSH and HTTP access"
  name        = "ec2_sg2"
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "allow HTTP access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_instance" "bot_server" {
  ami = "ami-0105b7fc0041ff22b"
  # "ami-0c1ac8a41498c1a9c" # Amazon Linux 2023 (HVM), SSD Volume Type
  # ami-0274f4b62b6ae3bd5 # Ubuntu Server 20.04 LTS (HVM), SSD Volume Type
  # ami-088c89fc150027121 # Amazon Linux 2 AMI (HVM), SSD Volume Type
  # ami-0d188df7cedce7d90 # Windows Server 2025 Base (HVM), SSD Volume Type
  instance_type          = "t3.micro"
  key_name               = "gmailAWS"
  vpc_security_group_ids = ["${aws_security_group.ec2_sg2.id}"]

  user_data = <<-EOF
              #!/bin/bash
              # Update system and install Python
              sudo apt-get update -y
              sudo apt-get install -y python3 python3-pip python3-venv git
              sudo apt install python3.12-venv

              # Set ownership of /home/ubuntu to the ubuntu user
              sudo chown -R ubuntu:ubuntu /home/ubuntu

              # Create venv as the ubuntu user (no sudo needed)
              python3 -m venv /home/ubuntu/venv
              source /home/ubuntu/venv/bin/activate
              
              
              # Clone the 'deploy' branch (replace with your repo)
              git clone -b deploy https://github.com/petbell/bot-telegram.git /home/ubuntu/bot-telegram

              # Change to the directory where your script is located
              cd /home/ubuntu/bot-telegram


              

              # Install requirements (if any)
              pip install --upgrade pip
              #pip install -r https://raw.githubusercontent.com/petbell/bot-telegram/deploy/requirements.txt  # (Optional)
              pip install -r /home/ubuntu/bot-telegram/requirements.txt

              # Clone your GitHub repo
              #git clone https://github.com/petbell/bot-telegram.git /home/ubuntu/bot-telelgram

              # Run your Python script (jidebot.py)
              python3 /home/ubuntu/bot-telegram/jidebot.py
              EOF

  tags = {
    Name = "BotServerInstance"
  }


}

output "bot_server_public_ip" {
  value       = aws_instance.bot_server.public_ip
  description = "Public IP of the bot server instance"

}

output "bot_server_name" {
  value       = aws_instance.bot_server.tags["Name"]
  description = "Name of the bot server instance"

}


