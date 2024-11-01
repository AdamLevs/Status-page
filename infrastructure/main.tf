terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region  = "us-east-1"
  profile = "default"
}

# Define VPC
module "vpc" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "5.0.0"
  name                 = "adams-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = ["us-east-1a", "us-east-1b"]
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets       = ["10.0.3.0/24", "10.0.4.0/24"]
  enable_nat_gateway   = true
  tags                 = { Name = "Adams-vpc", Uname = "Adam" }
}

# Define ECR repository
resource "aws_ecr_repository" "app_repo" {
  name = "adam-status-page-repo"
  tags = { Uname = "Adam" }
}

# Define EKS cluster
module "eks" {
  source              = "terraform-aws-modules/eks/aws"
  version             = "20.26.1"
  cluster_name        = "adams-eks-cluster"
  cluster_version     = "1.31"
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnets
  cluster_endpoint_public_access = true
  cluster_endpoint_public_access_cidrs = ["0.0.0.0/0"] # for security purposes change it to your local
  enable_cluster_creator_admin_permissions = true
  authentication_mode = "API" # this soon will be the only auth method since aws configmap deprecated
  eks_managed_node_groups = {
    Adam-EKS = {
      instance_types = ["t3.medium"]
      min_size       = 1
      max_size       = 3
      desired_size   = 1
    }
  }
  tags = { Name = "adams-eks", Uname = "Adam" }
}

# Security Group for EC2 instance
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-sg"
  description = "Allow necessary ports for EC2"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define ElastiCache for Redis
resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "Adam-redis-subnet-group"
  subnet_ids = module.vpc.private_subnets
  tags       = { Uname = "Adam" }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "adams-redis-cluster"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  subnet_group_name    = aws_elasticache_subnet_group.redis_subnet_group.name
  security_group_ids   = [aws_security_group.ec2_sg.id]
  parameter_group_name = "default.redis7"
  tags                 = { Uname = "Adam" }
}

# Define RDS
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "adam-rds-subnet-group"
  subnet_ids = module.vpc.private_subnets
  tags       = { Uname = "Adam" }
}

resource "aws_db_instance" "rds" {
  identifier            = "adams-rds"
  engine                = "postgres"
  instance_class        = "db.t3.micro"
  allocated_storage     = 20
  skip_final_snapshot   = true
  db_subnet_group_name  = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  db_name               = "status_page"
  username              = "status_page"
  password              = "Qz147369"  # Sensitive, need to replace with security manager or something else
  tags                  = { Uname = "Adam" }
}

# Define EC2 instance
resource "aws_instance" "ec2_instance" {
  ami                    = "ami-0866a3c8686eaeeba"  # Ubuntu 24 in us-east-1
  instance_type          = "t3.medium"
  subnet_id              = module.vpc.public_subnets[0]
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name               = "Adam-Macbook"
  tags = { Name = "adams-ec2-instance", Uname = "Adam" }
}

# Define ALB
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "8.0"
  name               = "adams-alb"
  load_balancer_type = "application"
  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets
  security_groups    = [aws_security_group.ec2_sg.id]
  tags               = { Name = "adams-alb", Uname = "Adam" }
}

resource "aws_lb_target_group" "ec2_tg" {
  name        = "Adam-ec2-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "instance"

  health_check {
    path     = "/"
    protocol = "HTTP"
  }
  tags = { Uname = "Adam" }
}

resource "aws_lb_listener" "alb_listener" {
  load_balancer_arn = module.alb.lb_arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ec2_tg.arn
  }
}

resource "aws_lb_target_group_attachment" "ec2_attachment" {
  target_group_arn = aws_lb_target_group.ec2_tg.arn
  target_id        = aws_instance.ec2_instance.id
  port             = 80
}

# Outputs for created resources
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnets" {
  value = module.vpc.public_subnets
}

output "private_subnets" {
  value = module.vpc.private_subnets
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "eks_node_group" {
  value = module.eks.eks_managed_node_groups["Adam-EKS"]
}

output "rds_endpoint" {
  value = aws_db_instance.rds.endpoint
}

output "rds_username" {
  value = aws_db_instance.rds.username
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "ec2_instance_public_ip" {
  value = aws_instance.ec2_instance.public_ip
}

output "alb_dns_name" {
  value = module.alb.lb_dns_name
}

# Local exec to output file
resource "null_resource" "output_to_file" {
  provisioner "local-exec" {
    command = <<EOT
      echo "VPC ID: ${module.vpc.vpc_id}" > terraform-outputs.txt
      echo "Public Subnets: ${join(", ", module.vpc.public_subnets)}" >> terraform-outputs.txt
      echo "Private Subnets: ${join(", ", module.vpc.private_subnets)}" >> terraform-outputs.txt
      echo "ECR Repository URL: ${aws_ecr_repository.app_repo.repository_url}" >> terraform-outputs.txt
      echo "EKS Cluster Name: ${module.eks.cluster_name}" >> terraform-outputs.txt
      echo "EKS Node Group: ${jsonencode(module.eks.eks_managed_node_groups["Adam-EKS"])}" >> terraform-outputs.txt
      echo "RDS Endpoint: ${aws_db_instance.rds.endpoint}" >> terraform-outputs.txt
      echo "RDS Username: ${aws_db_instance.rds.username}" >> terraform-outputs.txt
      echo "Redis Endpoint: ${aws_elasticache_cluster.redis.cache_nodes[0].address}" >> terraform-outputs.txt
      echo "EC2 Instance Public IP: ${aws_instance.ec2_instance.public_ip}" >> terraform-outputs.txt
      echo "ALB DNS Name: ${module.alb.lb_dns_name}" >> terraform-outputs.txt
    EOT
  }

  depends_on = [module.vpc, aws_ecr_repository.app_repo, aws_db_instance.rds, aws_elasticache_cluster.redis, module.alb, module.eks]
}
