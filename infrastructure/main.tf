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
  source             = "terraform-aws-modules/vpc/aws"
  version            = "5.0.0"
  name               = "adam-vpc"
  cidr               = "10.0.0.0/16"
  azs                = ["us-east-1a", "us-east-1b"]
  private_subnets    = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets     = ["10.0.3.0/24", "10.0.4.0/24"]
  enable_nat_gateway = true
  tags               = { Name = "adam-vpc", Uname = "Adam" }
}

# Global Security Group for all services
resource "aws_security_group" "global_sg" {
  name        = "adam-global-sg"
  description = "Allow traffic for all services in the VPC"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name  = "adam-global-sg"
    Uname = "Adam"
  }
}

# Define RDS Instance
resource "aws_db_subnet_group" "default" {
  name       = "adam-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name  = "adam-db-subnet-group"
    Uname = "Adam"
  }
}

resource "aws_db_instance" "default" {
  allocated_storage      = 20
  engine                 = "postgres"
  instance_class         = "db.t4g.micro"
  db_name                = "statuspage"
  username               = "statuspage"
  password               = "Qz147369"
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.global_sg.id] # Attach the global security group

  tags = {
    Name  = "adam-rds-instance"
    Uname = "Adam"
  }
}

# Define ElastiCache Cluster
resource "aws_elasticache_subnet_group" "default" {
  name       = "adam-elasticache-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name  = "adam-elasticache-subnet-group"
    Uname = "Adam"
  }
}

resource "aws_elasticache_cluster" "default" {
  cluster_id         = "adam-redis-cluster"
  engine             = "redis"
  node_type          = "cache.t3.micro"
  num_cache_nodes    = 1
  security_group_ids = [aws_security_group.global_sg.id] # Attach the global security group
  subnet_group_name  = aws_elasticache_subnet_group.default.name

  tags = {
    Name  = "adam-elasticache-cluster"
    Uname = "Adam"
  }
}

# Define ECR Repository
resource "aws_ecr_repository" "my_repository" {
  name                 = "adam-ecr-repo"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name  = "adam-ecr-repo"
    Uname = "Adam"
  }
}

# IAM Role for EKS
resource "aws_iam_role" "eks_cluster_role" {
  name = "adam-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })

  tags = {
    Name  = "adam-eks-cluster-role"
    Uname = "Adam"
  }
}

# Define EKS Cluster
resource "aws_eks_cluster" "my_cluster" {
  name     = "adam-eks-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.global_sg.id]
  }

  tags = {
    Name  = "adam-eks-cluster"
    Uname = "Adam"
  }
}

# Attach IAM Policy to EKS Role
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}

# IAM Role for EKS Node Group
resource "aws_iam_role" "eks_node_role" {
  name = "adam-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })

  tags = {
    Name  = "adam-eks-node-role"
    Uname = "Adam"
  }
}

# Attach IAM Policies to Node Role
resource "aws_iam_role_policy_attachment" "eks_worker_nodes_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "ecr_access_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}

# Define Node Group
resource "aws_eks_node_group" "my_node_group" {
  cluster_name    = aws_eks_cluster.my_cluster.name
  node_group_name = "adam-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = module.vpc.private_subnets

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  tags = {
    Name  = "adam-node-group"
    Uname = "Adam"
  }
}
