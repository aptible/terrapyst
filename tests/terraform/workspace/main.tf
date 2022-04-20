terraform {
  required_providers {
    random = {
      version = "~> 3.0"
    }

    null = {
      version = "~> 3.0"
    }

  }
}


variable "test_string" {
  default = "unset test string"
}

resource "null_resource" "first_testing_input" {
  triggers = {
    id = var.test_string
  }
}

resource "random_string" "first" {
  length = 16
}

resource "null_resource" "first" {
  triggers = {
    id = "${random_string.first.id}"
  }
}


resource "random_string" "second" {
  length = 16
}

resource "null_resource" "second" {
  triggers = {
    id = "${random_string.second.id}"
  }
}


resource "random_string" "third" {
  length = 16
}

resource "null_resource" "third" {
  triggers = {
    id = "${random_string.third.id}"
  }
}
