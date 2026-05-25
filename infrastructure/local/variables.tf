variable "image" {
  description = "FruitAPI image to run locally. Build it first: docker build -t fruitapi:dev ../.."
  type        = string
  default     = "fruitapi:dev"
}

variable "host_port" {
  description = "Host port mapped to the container."
  type        = number
  default     = 8000
}
