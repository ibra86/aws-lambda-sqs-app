terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region                  = var.region
  shared_credentials_file = var.credentials_file
  profile                 = var.aws_profile
}