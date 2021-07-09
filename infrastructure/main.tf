module "producer_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "producer-lambda"
  description   = "Producer lambda"
  handler       = "index.handler"
  runtime       = "python3.8"
  role_name     = "producer-lambda-role"

  source_path = "../functions/producer"
}

module "worker_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "worker-lambda"
  description   = "Worker lambda"
  handler       = "index.handler"
  runtime       = "python3.8"
  role_name     = "worker-lambda-role"

  source_path = "../functions/worker"
}

module "sqs_queue" {
  source = "terraform-aws-modules/sqs/aws"

  name = "lambda-queue"
}

module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "s3-bucket-right-bound"
}

module "sns_topic" {
  source = "terraform-aws-modules/sns/aws"

  name = "timestamp-topic"
}