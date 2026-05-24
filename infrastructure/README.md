# Infrastructure

Terraform configurations for FruitAPI. Two stacks:

| Path | Backend | Purpose |
|------|---------|---------|
| `aws/`   | local (will move to S3 in L6) | The deliverable: ECS Fargate + VPC + IAM + CloudWatch logs. Extended in L4b (RDS+Secrets) and L5 (ALB). |
| `local/` | local | Optional, for the brief's state experiments. Runs the FruitAPI image on local Docker via the `kreuzwerker/docker` provider. |

## Prerequisites

- Terraform ≥ 1.7
- For `aws/`: an AWS account, IAM user with programmatic access, `aws configure` done locally. Free tier is enough for the homework footprint.
- For `local/`: Docker running; image built (`docker build -t fruitapi:dev .` from repo root).

## aws/ — deploy FruitAPI to ECS Fargate

```bash
cd infrastructure/aws
cp terraform.tfvars.example terraform.tfvars   # edit if needed
terraform init
terraform plan
terraform apply
```

Once applied:

- Find the running task: `aws ecs list-tasks --cluster $(terraform output -raw ecs_cluster_name)`
- Get its public IP from the ENI (`aws ecs describe-tasks` → attachment → `networkInterfaceId` → `aws ec2 describe-network-interfaces`).
- `curl http://<public-ip>:8000/health`

In L5 we add an ALB and stop poking the task IP directly.

### Image visibility

The default image is `ghcr.io/petyb/intro-to-devops-starter:latest`. After
the main-branch CI first pushes the image, the package is private by
default in GHCR. Either:

1. Make the package public (GitHub → your profile → Packages → the package
   → Package settings → Change visibility → Public), **or**
2. Configure `repositoryCredentials` on the task definition with a Secrets
   Manager secret holding a GHCR PAT. (Done in L4b alongside DB creds.)

Option 1 is simpler for grading.

## local/ — Docker provider experiments

This stack exists to practise the state operations the brief calls out
(`terraform state rm`, `terraform import`, etc.) without spending on AWS:

```bash
docker build -t fruitapi:dev ../..            # build the image first
cd infrastructure/local
terraform init
terraform apply
curl $(terraform output -raw url)/health

# Then try the brief's experiments:
terraform state list
terraform state rm docker_container.fruitapi
terraform plan                                 # Terraform now thinks it needs to recreate
terraform import docker_container.fruitapi $(docker inspect -f '{{.Id}}' fruitapi)
terraform plan                                 # back to no-op
```
