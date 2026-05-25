variable "region" {
  description = "AWS region for all resources."
  type        = string
  default     = "eu-central-1"
}

variable "project" {
  description = "Logical project name; used to namespace resources."
  type        = string
  default     = "fruitapi"
}

variable "environment" {
  description = "Environment label (dev/stage/prod). Free-form, used in resource names."
  type        = string
  default     = "dev"
}

variable "image" {
  description = "Container image reference (registry/repo:tag)."
  type        = string
  default     = "ghcr.io/petyb/intro-to-devops-starter:latest"
}

variable "container_port" {
  description = "Port the FruitAPI container listens on."
  type        = number
  default     = 8000
}

variable "task_cpu" {
  description = "ECS task vCPU units (256 = 0.25 vCPU)."
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "ECS task memory in MiB."
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Number of ECS service replicas."
  type        = number
  default     = 1
}

variable "vpc_cidr" {
  description = "CIDR block for the project VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDRs for the public subnets (one per AZ)."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 14
}

variable "ingress_cidrs" {
  description = "CIDRs allowed to reach the container port directly. Tightens to ALB-only in lecture 5."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
