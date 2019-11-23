resource "google_cloudfunctions_function" "function" {
  name        = var.function_title
  description = var.function_description
  runtime     = var.function_runtime

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.function.name
  timeout               = 120

  entry_point   = var.entry_point
  event_trigger {
    event_type  = "google.pubsub.topic.publish"
    resource    = google_pubsub_topic.trigger.name
  }

  environment_variables = {
    ACCESS_TOKEN = var.access_token
    PAGE_ID = var.page_id
  }
}

resource "google_pubsub_topic" "trigger" {
  name = var.pubsub_topic
}

resource "google_cloud_scheduler_job" "every_week" {
  name      = var.scheduler_job
  schedule  = "0 0 * * 0"

  pubsub_target {
    topic_name  = google_pubsub_topic.trigger.id
    data        = base64encode("start")
  }
}
