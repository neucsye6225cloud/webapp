variable ssh_username {
  type = string
}

variable image_name {
  type = string
}

variable source_image_family {
  type = string
}

variable project_id {
  type        = string
  description = "project_id from GCP account"
}

variable zone {
  type = string
}

variable network {}

variable custom_image_family_name {
  type    = string
  default = "csye6225-app-image"
}
