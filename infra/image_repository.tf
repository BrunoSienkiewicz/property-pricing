resource "awscc_ecr_repository" "image_repository_base_model" {
  repository_name      = "${var.project_name}/base_model"
  image_tag_mutability = "MUTABLE"

  lifecycle_policy = {
    lifecycle_policy_text = <<EOF
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Expire images older than 14 days",
                    "selection": {
                        "tagStatus": "untagged",
                        "countType": "sinceImagePushed",
                        "countUnit": "days",
                        "countNumber": 14
                    },
                    "action": {
                        "type": "expire"
                    }
                }
            ]
        }
        EOF
  }
}

resource "awscc_ecr_repository" "image_repository_app" {
  repository_name      = "${var.project_name}/app"
  image_tag_mutability = "MUTABLE"

  lifecycle_policy = {
    lifecycle_policy_text = <<EOF
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Expire images older than 14 days",
                    "selection": {
                        "tagStatus": "untagged",
                        "countType": "sinceImagePushed",
                        "countUnit": "days",
                        "countNumber": 14
                    },
                    "action": {
                        "type": "expire"
                    }
                }
            ]
        }
        EOF
  }
}

