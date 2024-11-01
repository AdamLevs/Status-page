# Terraform AWS Infrastructure Setup

```shell
aws eks update-kubeconfig --name adams-eks-cluster --region us-east-1
```

This Terraform provides configuration to deploy a comprehensive infrastructure setup on AWS. The resources include a Virtual Private Cloud (VPC), Elastic Kubernetes Service (EKS) cluster, Elastic Container Registry (ECR), Elasticache for Redis, a PostgreSQL RDS database, an EC2 instance, and an Application Load Balancer (ALB).

## Table of Contents
- [Overview](#overview)
- [Infrastructure Architecture](#infrastructure-architecture)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Resources](#resources)
- [Outputs](#outputs)
- [License](#license)

## Overview

This infrastructure project automates the deployment of a web application environment. The key services included are:
- VPC with public and private subnets
- EKS cluster for containerized applications
- ECR for Docker image storage
- ElastiCache Redis for caching
- RDS PostgreSQL for relational database needs
- EC2 instance for web server or auxiliary services
- ALB (Application Load Balancer) to route incoming traffic to the EC2 instance

## Infrastructure Architecture

This architecture provides a scalable and highly available environment, with components separated into public and private subnets for security and network control:
- Public Subnets for the EC2 instance and ALB
- Private Subnets for the EKS cluster, Redis, and RDS database

## Prerequisites

To deploy this infrastructure, ensure you have the following installed:
- Terraform >= 1.0
- AWS account with IAM permissions to create resources
- AWS CLI configured with a profile for authentication
- SSH key pair for the EC2 instance (use Adam-Macbook key or create one with the name specified)

### Configurations
- AWS region: us-east-1
- AWS profile: default
- Required Providers:
  - hashicorp/aws version ~> 5.0

## Usage

### Clone the Repository
```bash
git clone https://github.com/AdamLevs/Status-page.git
cd Status-page/infrastructure
```

### Initialize Terraform
Initialize the project to download provider plugins.
```bash
terraform init
```

### Preview and Apply Changes
Review the resources that Terraform will create with:
```bash
terraform plan
```

Apply the infrastructure:
```bash
terraform apply
```

### Cleanup
To remove all resources created by this Terraform project:
```bash
terraform destroy
```

## Resources

This configuration deploys the following AWS resources:
- **VPC**: 2 public and 2 private subnets across two availability zones with a NAT gateway.
- **EKS Cluster**: Managed Kubernetes cluster with autoscaling node group.
- **ECR Repository**: For container image storage.
- **ElastiCache Redis**: Cache instance in a private subnet for application caching needs.
- **RDS PostgreSQL**: Relational database for application data.
- **EC2 Instance**: Web server instance with security group rules.
- **ALB**: Application load balancer for distributing incoming traffic.

### Security Group Rules
- SSH (22), HTTP (80), and HTTPS (443) ingress for the EC2 instance
- Allow All Egress for outgoing traffic

## Outputs

Upon successful deployment, the following outputs are provided:
- **EKS Cluster Name**: `eks_cluster_name` - EKS cluster name for Kubernetes deployments.
- **ECR Repository URL**: `ecr_repo_url` - URL for the ECR repository for Docker images.
- **RDS Endpoint**: `rds_endpoint` - Endpoint for the RDS PostgreSQL database.
- **ElastiCache Endpoint**: `elasticache_endpoint` - Endpoint for the Redis cache.
- **ALB DNS Name**: `alb_dns_name` - Public DNS of the ALB to access the web application.
- **EC2 Public IP**: `ec2_public_ip` - Public IP address of the EC2 instance.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
