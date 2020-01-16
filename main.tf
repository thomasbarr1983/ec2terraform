#Basic Terraform file to create an ec2 vm

provider "aws" {
  region = "us-east-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "TomVM" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = "TomVM"
  subnet_id     = "subnet-c5919aa2"
  user_data     = <<-EOT
  #!/bin/bash
  set -e
  set -x

  echo "Hello World"
  apt-get update
  apt-get -y install python3-pip
  pip3 install ansible
  echo "${var.git_deploy_key}" >git_deploy_key
  chmod 600 git_deploy_key
  /usr/local/bin/ansible-pull --accept-host-key --private-key git_deploy_key --verbose \
    --url "git@github.com:thomasbarr1983/ec2terraform.git" --directory /var/local/src/instance-bootstrap "config.yml"
  EOT

  vpc_security_group_ids = [ aws_security_group.allow_ssh.id ]
  tags = {
    Name = "Tom VM"  
    }
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow ssh inbound traffic"
  
  egress { 
   from_port    = 0
   to_port      = 0
   protocol     = -1
   cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    # ssh (change to whatever ports you need)
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    # Please restrict your ingress to only necessary IPs and ports.
    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "instance_ip_addr" {
  value = aws_instance.TomVM.public_ip
}



data "aws_vpc" "default" {
  default = true
}



