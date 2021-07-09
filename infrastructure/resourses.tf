resource "aws_sns_topic_subscription" "email-target" {
  topic_arn = module.sns_topic.sns_topic_arn
  protocol  = var.sns_protocol
  endpoint  = var.protocol_endpoint
}