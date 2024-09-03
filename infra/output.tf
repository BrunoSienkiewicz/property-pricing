output "api_url" {
  value = aws_apigatewayv2_api.api_gateway.api_endpoint
}

output "redshift_endpoint" {
  value = aws_redshift_cluster.redshift_cluster.endpoint
}
