module "producer_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "producer-lambda"
  description   = "Producer lambda"
  handler       = "index.handler"
  runtime       = "python3.8"
  role_name     = "producer-lambda-role"
  publish       = true
  timeout       = 300

  source_path = "../functions/producer"
}

module "worker_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "worker-lambda"
  description   = "Worker lambda"
  handler       = "index.handler"
  runtime       = "python3.8"
  role_name     = "worker-lambda-role"
  publish       = true
  timeout       = 300

  layers = [
    module.lambda_layer_s3.lambda_layer_arn,
  ]

  source_path = "../functions/worker"
}

module "s3_bucket_lambda_layer" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "s3-bucket-right-bound-with-lambda-builds"
}

module "lambda_layer_s3" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lambda-layer-s3"
  description         = "Lambda layer"
  compatible_runtimes = ["python3.8"]

  source_path = "../vendor"

  store_on_s3 = true
  s3_bucket   = "s3-bucket-right-bound-with-lambda-builds"
}

module "sqs_queue" {
  source = "terraform-aws-modules/sqs/aws"

  name = "lambda-queue"
  visibility_timeout_seconds = 300
}

module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "s3-bucket-right-bound"
}

module "sns_topic" {
  source = "terraform-aws-modules/sns/aws"

  name = "timestamp-topic"
}