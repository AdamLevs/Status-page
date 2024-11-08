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
resource "aws_security_group" "adam-global-sg" {
  name        = "adam-global-sg"
  description = "Allow traffic within VPC for all services"
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
resource "aws_db_subnet_group" "adam-db-subnet-group" {
  name       = "adam-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name  = "adam-db-subnet-group"
    Uname = "Adam"
  }
}

resource "aws_db_instance" "adam-rds-instance" {
  allocated_storage      = 20
  engine                 = "postgres"
  instance_class         = "db.t4g.medium"
  identifier             = "adam-status-page"
  skip_final_snapshot    = true
  db_name                = "statuspage"
  username               = "statuspage"
  password               = "Qz147369"
  db_subnet_group_name   = aws_db_subnet_group.adam-db-subnet-group.name
  vpc_security_group_ids = [aws_security_group.adam-global-sg.id]

  tags = {
    Name  = "adam-rds-instance"
    Uname = "Adam"
  }
}

# Define ElastiCache Cluster
resource "aws_elasticache_subnet_group" "adam-elasticache-subnet-group" {
  name       = "adam-elasticache-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name  = "adam-elasticache-subnet-group"
    Uname = "Adam"
  }
}

resource "aws_elasticache_cluster" "adam-redis-cluster" {
  cluster_id         = "adam-redis-cluster"
  engine             = "redis"
  node_type          = "cache.t4g.micro"
  num_cache_nodes    = 1
  security_group_ids = [aws_security_group.adam-global-sg.id]
  subnet_group_name  = aws_elasticache_subnet_group.adam-elasticache-subnet-group.name

  tags = {
    Name  = "adam-elasticache-cluster"
    Uname = "Adam"
  }
}

# Define ECR Repository
resource "aws_ecr_repository" "adam-ecr-repo" {
  name                 = "adam-ecr-repo"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name  = "adam-ecr-repo"
    Uname = "Adam"
  }
}

# IAM Role for EKS
resource "aws_iam_role" "adam-eks-cluster-role" {
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

# Broad permissions for EKS cluster role
resource "aws_iam_policy" "adam_eks_permissions" {
  name        = "adamEKSFullAccess"
  description = "Full access for EKS cluster and its resources"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "eks:*",
          "ec2:*",
          "ecr:*",
          "elasticloadbalancing:*",
          "cloudwatch:*",
          "logs:*",
          "autoscaling:*",
          "iam:PassRole"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_adam_eks_permissions" {
  policy_arn = aws_iam_policy.adam_eks_permissions.arn
  role       = aws_iam_role.adam-eks-cluster-role.name
}

# Define EKS Cluster
resource "aws_eks_cluster" "adam-eks-cluster" {
  name     = "adam-eks-cluster"
  role_arn = aws_iam_role.adam-eks-cluster-role.arn
  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.adam-global-sg.id]
  }

  tags = {
    Name  = "adam-eks-cluster"
    Uname = "Adam"
  }
}

# IAM Role for EKS Node Group
resource "aws_iam_role" "adam-eks-node-role" {
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

# Attach policies for the Node Role
resource "aws_iam_role_policy_attachment" "adam-eks-worker-nodes-policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.adam-eks-node-role.name
}

resource "aws_iam_role_policy_attachment" "adam-eks-cni-policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.adam-eks-node-role.name
}

resource "aws_iam_role_policy_attachment" "adam-ecr-access-policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.adam-eks-node-role.name
}

# Broad permissions for Node Role
resource "aws_iam_policy" "adam_eks_node_permissions" {
  name        = "adamEKSNodeFullAccess"
  description = "Full access for EKS node group and its resources"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:*",
          "ecr:*",
          "cloudwatch:*",
          "logs:*",
          "iam:PassRole"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_adam_eks_node_permissions" {
  policy_arn = aws_iam_policy.adam_eks_node_permissions.arn
  role       = aws_iam_role.adam-eks-node-role.name
}

# Define Node Group
resource "aws_eks_node_group" "adam-node-group" {
  cluster_name    = aws_eks_cluster.adam-eks-cluster.name
  node_group_name = "adam-node-group"
  node_role_arn   = aws_iam_role.adam-eks-node-role.arn
  instance_types  = ["t4g.medium"]
  ami_type        = "AL2023_ARM_64_STANDARD"
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

# Outputs
output "ecr_repository_url" {
  value = aws_ecr_repository.adam-ecr-repo.repository_url
}

output "rds_endpoint" {
  value = aws_db_instance.adam-rds-instance.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.adam-redis-cluster.configuration_endpoint
}

output "eks_cluster_name" {
  value = aws_eks_cluster.adam-eks-cluster.name
}