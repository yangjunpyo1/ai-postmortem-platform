terraform {
  backend "s3" {
    key            = "ai-postmortem-platform/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "yp-terraform-lock"
    encrypt        = true
  }
}