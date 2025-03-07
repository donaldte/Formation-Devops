terraform {

    backend "s3" {
        bucket         = "my-terraform-backend-youtube"  # Replace with your actual S3 bucket name
        key            = "terraform/state.tfstate"  # Path to the state file in S3
        region         = "us-west-2"  # Region of the S3 bucket
        dynamodb_table = "terraform-lock"  # Name of the DynamoDB table for state locking
        encrypt        = true  # Encrypt the state file for security
    }

   required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16" # ceci voudrait dire que la version de aws doit être supérieure ou égale à 4.16
    }
  }

  required_version = ">= 1.2.0" # ceci voudrait dire que la version de terraform doit être supérieure ou égale à 1.2.0
}

provider "aws" {  # ceci est une configuration du provider aws
  region  = "us-west-2"
}

resource "aws_instance" "app_server" { # ceci est une configuration de la ressource aws_instance
  ami           = "ami-830c94e3"
  instance_type = "t2.micro"

  tags = {
    Name = var.instance_name # ceci est une configuration des tags
  }
}
