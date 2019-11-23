variable "function_title" {
  description = "The name of the function."
  default     = "yugiohbot__booster-pack"
}

variable "function_name" {
  description = "The name of the function archive."
  default     = "function"
}

variable "function_description" {
  description = "The description of the function."
  default     = "Booster Pack creator for the YuGiOhBot"
}

variable "function_runtime" {
  description = "The runtime for the function."
  default     = "python37"
}

variable "entry_point" {
  description = "The name of the function to run from main.py"
  default     = "function"
}

variable "pubsub_topic" {
  description = "Name of the PubSub topic to subscribe to."
  default     = "trigger-booster-pack"
}

variable "scheduler_job" {
  description = "Name of the Cloud Schedular job."
  default     = "every-week"
}

variable "access_token" {
  description = "The Facebook SDK Access Token"
}

variable "page_id" {
  description = "The Facebook Page ID"
}