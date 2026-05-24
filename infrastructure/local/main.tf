data "docker_image" "fruitapi" {
  name = var.image
}

resource "docker_container" "fruitapi" {
  name  = "fruitapi"
  image = data.docker_image.fruitapi.id

  ports {
    internal = 8000
    external = var.host_port
  }

  restart = "unless-stopped"
}

output "url" {
  value = "http://127.0.0.1:${var.host_port}"
}
