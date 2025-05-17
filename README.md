# Serverless RDS Cluster Automation 💡

This project provides a **serverless infrastructure automation solution** to provision **Amazon RDS clusters on demand**. It leverages AWS Lambda, API Gateway, SQS, and Terraform, following DevOps best practices with full CI/CD automation using **CircleCI**.

---

## 🔧 Use Case

Cloud engineers or developers can request an RDS database instance (MySQL/PostgreSQL) by sending a simple API call with JSON input.  
The system automates provisioning, environment selection (Dev/Prod), and secure credential handling — **without any manual steps**.

---

## 📐 Architecture Overview

```
[Client]
   │
   └──▶ [API Gateway]
               │
               └──▶ [Lambda: SendToQueue]
                           │
                           └──▶ [SQS Queue]
                                       │
                                       └──▶ [Lambda: ProcessRequest]
                                                   │
                                                   └──▶ [CircleCI triggers Terraform]
                                                                 │
                                                                 └──▶ [AWS RDS Instance Created]
```

---

## 🧰 Technologies Used

- **AWS Lambda**
- **Amazon API Gateway**
- **Amazon SQS**
- **Terraform**
- **AWS Secrets Manager**
- **AWS SAM**
- **CircleCI**
- **Python**

---

## 📦 JSON Input Example

```json
{
  "db_name": "demodb1",
  "db_engine": "postgres",
  "env": "dev"
}
```

---

## ⚙️ Environment Behavior

- `env = "dev"` → `db.t3.micro` (Free tier)
- `env = "prod"` → `db.t3.small`
- DB credentials (username/password) are securely stored and retrieved from **Secrets Manager**

---

## 🚀 Deployment & Flow

### 1. Deploy Lambda Stack
```bash
sam build && sam deploy --guided
```

### 2. Trigger API
```bash
curl -X POST https://<your-api-id>.execute-api.<region>.amazonaws.com/prod/ \
     -H "Content-Type: application/json" \
     -d '{"db_name": "demodb1", "db_engine": "postgres", "env": "dev"}'
```

### 3. CircleCI
- Detects SQS message
- Executes `terraform apply` with tfvars
- Provisions the database automatically

---

## 🧾 Files & Structure

```
serverless_rds_cluster/
├── lambda/                    → Lambda functions (producer/consumer)
├── terraform/                 → Terraform RDS provisioning
├── .circleci/config.yml       → CI/CD logic
├── samconfig.toml             → SAM deployment config
└── template.yaml              → AWS SAM template
```

---

## 📚 Author

**Irena Kochtov**  
Certified AWS Solutions Architect Associate  
☁️ Cloud & Infrastructure | DevOps Enthusiast | Data Center Expert  
🔗 [LinkedIn](https://www.linkedin.com/in/irena-kochtov)

---

## 🏁 Next Steps

- [ ] Add monitoring & alerts for RDS
- [ ] Add email/SNS notifications on creation success/failure
- [ ] Add retry logic for SQS messages
