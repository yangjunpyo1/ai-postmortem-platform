terraform {
  backend "s3" {
    bucket         = "yp-terraform-state-381492097392"
    key            = "ai-postmortem-platform/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "yp-terraform-lock"
    encrypt        = true
  }
}