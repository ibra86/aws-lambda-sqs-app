resource "aws_cloudwatch_event_rule" "lambda_producer_cw_event_rule_trigger" {
  name                = "lambda-producer-cron"
  schedule_expression = var.lambda_producer_cron_schedule
}

resource "aws_cloudwatch_event_target" "lambda_invoke_event_target" {
  rule = aws_cloudwatch_event_rule.lambda_producer_cw_event_rule_trigger.name
  arn  = module.producer_lambda_function.lambda_function_arn
}

resource "aws_lambda_permission" "allows_cw_event_trigger" {
  action        = "lambda:InvokeFunction"
  function_name = module.producer_lambda_function.lambda_function_arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_producer_cw_event_rule_trigger.arn
}

resource "aws_iam_role_policy" "producer_lambda_role_policy" {
  name = "producer-lambda-role-policy"
  role = module.producer_lambda_function.lambda_role_name

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sqs:*"
            ],
            "Resource": ["*"],
            "Effect": "Allow",
            "Sid": "Permissions"
        }
    ]
}
POLICY
}

resource "aws_lambda_event_source_mapping" "lambda_worker_sqs_trigger" {
  event_source_arn = module.sqs_queue.sqs_queue_arn
  function_name    = module.worker_lambda_function.lambda_function_arn
}

resource "aws_lambda_permission" "allows_sqs_trigger" {
  action        = "lambda:InvokeFunction"
  function_name = module.worker_lambda_function.lambda_function_arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_lambda_event_source_mapping.lambda_worker_sqs_trigger.event_source_arn
}


resource "aws_iam_role_policy" "worker_lambda_role_policy" {
  name = "worker-lambda-role-policy"
  role = module.worker_lambda_function.lambda_role_name

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sqs:*"
            ],
            "Resource": ["*"],
            "Effect": "Allow",
            "Sid": "Permissions"
        }
    ]
}
POLICY
}

resource "aws_sns_topic_subscription" "email-target" {
  topic_arn = module.sns_topic.sns_topic_arn
  protocol  = var.sns_protocol
  endpoint  = var.protocol_endpoint
}
