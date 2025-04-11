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

resource "aws_security_group" "ec2_sg1" {
    description = "Allow SSH and HTTP access"
    name       = "ec2_sg1"
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
        cidr_blocks = [ "0.0.0.0/0" ]
    }

    egress {
        description = "allow all outbound traffic"
        from_port   = 0
        to_port     = 0
        protocol    = "-1" # all protocols
        cidr_blocks = [ "0.0.0.0/0" ]
    }
  
}

resource "aws_instance" "bot_server" {
  ami           = "ami-0105b7fc0041ff22b"
  # "ami-0c1ac8a41498c1a9c" # Amazon Linux 2023 (HVM), SSD Volume Type
 # ami-0274f4b62b6ae3bd5 # Ubuntu Server 20.04 LTS (HVM), SSD Volume Type
 # ami-088c89fc150027121 # Amazon Linux 2 AMI (HVM), SSD Volume Type
 # ami-0d188df7cedce7d90 # Windows Server 2025 Base (HVM), SSD Volume Type
  instance_type = "t3.micro"
  key_name = "gmailAWS"
  vpc_security_group_ids = ["${aws_security_group.ec2_sg1.id}"]

  tags = {
    Name = "BotServerInstance"
  }
}

output "bot_server_public_ip" {
  value = aws_instance.bot_server.public_ip
  description = "Public IP of the bot server instance"
  
}

output "bot_server_name" {
  value = aws_instance.bot_server.tags["Name"]
  description = "Name of the bot server instance"
  
}
