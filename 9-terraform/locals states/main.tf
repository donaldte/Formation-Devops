terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16" # ceci voudrait dire que la version de aws doit être supérieure ou égale à 4.16
    }
  }

  required_version = ">= 1.2.0" # ceci voudrait dire que la version de terraform doit être supérieure ou égale à 1.2.0
}

provider "aws" {  # ceci est une configuration du provider aws
  region  = "us-east-1"
}

resource "aws_instance" "app_server" { # ceci est une configuration de la ressource aws_instance
  ami           = "ami-0023921b4fcd5382b" # ceci est une configuration de l'AMI
  instance_type = "t2.micro"

  tags = {
    Name = "tutoYoutubeEc2" # ceci est une configuration des tags
  } 
}
