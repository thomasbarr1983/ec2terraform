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
#https://www.terraform.io/docs/providers/aws/r/instance.html
resource "aws_instance" "TomVM" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = "TomVM"
  subnet_id     = "subnet-c5919aa2"
  user_data     = <<-EOT
  #!/bin/bash
  # turns on bash error handling so bash exits on first command that returns an error
  set -e
  # print every command bash executes for debug
  set -x

  echo "Hello World"
  apt-get update
  apt-get -y install python3-pip
  pip3 install ansible
  echo "${var.git_deploy_key}" >git_deploy_key
  # makes it private to current user/owner
  chmod 600 git_deploy_key
  /usr/local/bin/ansible-pull --accept-host-key --private-key git_deploy_key --verbose \
    --url "${var.github_url}" --directory /var/local/src/instance-bootstrap "config.yml"
  echo "${aws_db_instance.default.endpoint}"
  EOT

  vpc_security_group_ids = [ aws_security_group.allow_ssh.id ]
  #these tags only allow one to groups resources together for management and billing purposes
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
  ingress {
    # python/flask 
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    # Please restrict your ingress to only necessary IPs and ports.
    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "instance_ip_addr" {
  value = aws_instance.TomVM.public_ip
}

output "endpointdb" {
  value = aws_db_instance.default.endpoint
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "11"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "foo"
  password             = "foobarbaz"
}

