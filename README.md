# Serverless RDS Cluster Automation

This project automates the creation of a serverless RDS cluster using AWS SAM, Terraform, and CircleCI.

It provides a secure and fully automated pipeline for developers to request database clusters via an API, which are then provisioned through infrastructure-as-code practices.

## Tech Stack

- AWS SAM (API Gateway, Lambda, SQS, SNS)
- Terraform (RDS Cluster provisioning)
- CircleCI (CI/CD automation)
- Python (Lambda function logic)
- AWS Secrets Manager / SSM Parameter Store (secret management)

## Project Structure