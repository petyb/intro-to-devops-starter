provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project   = "fruitapi"
      ManagedBy = "terraform"
      Owner     = "petyb"
    }
  }
}
