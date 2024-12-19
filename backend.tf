terraform {
 backend "s3" {
   bucket         = "chess-mentor-api-vivs-backend-block"
   key            = "global/s3/terraform.tfstate"
   region         = "us-east-1"
   dynamodb_table = "chess-mentor-api-vivs-backend-block"
   encrypt        = true
 }
}
