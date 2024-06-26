packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = ">= 1"
    }
  }
}

source "googlecompute" "centos" {
  project_id          = "${var.project_id}"
  source_image_family = "${var.source_image_family}"
  ssh_username        = "${var.ssh_username}"
  zone                = "${var.zone}"
  network             = "${var.network}"
  use_internal_ip     = false
  image_family        = "${var.custom_image_family_name}"
  image_labels = {
    "created-by" : "packer",
    "custom-app" : "blogapp"
  }
}

build {
  name    = "csye6225-packer-build"
  sources = ["source.googlecompute.centos"]

  provisioner "shell" {
    script = "./packer/scripts/os_setup.sh"
  }

  provisioner "file" {
    source      = "./webapp.zip"
    destination = "/tmp/"
  }

  // provisioner "shell" {
  //   script = "./packer/scripts/db.sh"
  // }

  provisioner "shell" {
    script = "./packer/scripts/app_setup.sh"
  }

  provisioner "shell" {
    script = "./packer/scripts/user_permission.sh"
  }

  provisioner "shell" {
    script = "./packer/scripts/ops_agent_setup.sh"
  }

  provisioner "file" {
    source      = "./csye6225.service"
    destination = "/tmp/"
  }

  provisioner "shell" {
    script = "./packer/scripts/services.sh"
  }

  # restart service part 
  provisioner "file" {
    source      = "./packer/scripts/wb_restart.sh"
    destination = "/tmp/"
  }

  provisioner "shell" {
    script = "./packer/scripts/wb_restart_permission.sh"
  }

  provisioner "file" {
    source      = "./web_service_restart.service"
    destination = "/tmp/"
  }

  provisioner "shell" {
    script = "./packer/scripts/wb_restart_service.sh"
  }

  provisioner "shell" {
    inline = ["sleep 30",
    "sudo systemctl restart google-cloud-ops-agent"]
  }

  post-processor "manifest" {
    output = "/tmp/image_manifest.json"
  }
}
