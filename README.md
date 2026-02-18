# 🚀 MLflow on AWS - Complete Setup Guide

This guide walks you through deploying **MLflow Tracking Server on AWS
EC2** with **S3 as the artifact store** for a production-ready
experiment tracking setup.

------------------------------------------------------------------------

# 🏗️ Architecture Overview

-   **EC2 (Ubuntu)** → Hosts MLflow Tracking Server
-   **S3 Bucket** → Stores MLflow artifacts (models, metrics, files)
-   **IAM User** → Provides secure AWS access
-   **Security Group** → Opens Port 5000 for MLflow UI

------------------------------------------------------------------------

# 📌 Step 1: AWS IAM Setup

1.  Login to AWS Console.
2.  Go to **IAM → Users → Create User**
3.  Attach policy:
    -   `AdministratorAccess` *(For learning/demo purposes only ---
        restrict in production)*
4.  Download or copy:
    -   AWS Access Key
    -   AWS Secret Key

------------------------------------------------------------------------

# 📌 Step 2: Configure AWS CLI (Local Machine)

Install AWS CLI if not already installed:

``` bash
pip install awscli
```

Configure credentials:

``` bash
aws configure
```

Enter: - AWS Access Key - AWS Secret Key - Region (e.g., us-east-1) -
Output format (json)

------------------------------------------------------------------------

# 📌 Step 3: Create S3 Bucket

Go to AWS → S3 → Create Bucket

Example:

    mlflow-tracking-bucket

Make sure: - Bucket name is globally unique - Keep default settings (for
learning)

------------------------------------------------------------------------

# 📌 Step 4: Launch EC2 Instance

1.  Go to EC2 → Launch Instance
2.  Select **Ubuntu (Latest LTS)**
3.  Choose instance type (e.g., t2.micro)
4.  Configure Security Group:
    -   Allow HTTP (Port 80)
    -   Add Custom TCP → Port **5000**
    -   Source: Anywhere (0.0.0.0/0) *(for demo only)*

Launch and connect via SSH.

------------------------------------------------------------------------

# 📌 Step 5: Install Dependencies on EC2

Run the following:

``` bash
sudo apt update

sudo apt install python3-pip -y
sudo apt install pipenv -y
sudo apt install virtualenv -y

mkdir mlflow
cd mlflow

pipenv install mlflow
pipenv install awscli
pipenv install boto3

pipenv shell
```

------------------------------------------------------------------------

# 📌 Step 6: Configure AWS Credentials on EC2

Inside EC2:

``` bash
aws configure
```

Enter your IAM credentials.

------------------------------------------------------------------------

# 📌 Step 7: Start MLflow Server

``` bash
mlflow server   -h 0.0.0.0   -p 5000   --backend-store-uri sqlite:///mlflow.db   --default-artifact-root s3://mlflow-tracking-bucket
```

### Explanation:

-   `-h 0.0.0.0` → Allows external access
-   `-p 5000` → Runs on port 5000
-   `backend-store-uri` → Stores experiment metadata
-   `default-artifact-root` → Stores artifacts in S3

------------------------------------------------------------------------

# 📌 Step 8: Access MLflow UI

Open in browser:

    http://<EC2-PUBLIC-IP>:5000

Example:

    http://ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com:5000

------------------------------------------------------------------------

# 📌 Step 9: Connect from Local Machine

Set tracking URI:

### Linux / Mac

``` bash
export MLFLOW_TRACKING_URI=http://<EC2-PUBLIC-IP>:5000
```

### Windows (PowerShell)

``` powershell
setx MLFLOW_TRACKING_URI "http://<EC2-PUBLIC-IP>:5000"
```

Or set inside Python:

``` python
import mlflow
mlflow.set_tracking_uri("http://<EC2-PUBLIC-IP>:5000")
```

------------------------------------------------------------------------

# 🔒 Production Recommendations

For real-world deployment:

-   ❌ Do NOT use AdministratorAccess
-   ✅ Use IAM Role attached to EC2
-   ✅ Use RDS instead of SQLite
-   ✅ Use Nginx reverse proxy
-   ✅ Add SSL (HTTPS)
-   ✅ Restrict security group access

------------------------------------------------------------------------

# 🎯 Final Architecture (Production Ready)

    Client → Nginx → MLflow Server (EC2)
                            ↓
                        RDS Database
                            ↓
                        S3 Artifacts

------------------------------------------------------------------------

# 🏁 You Now Have:

✅ Remote MLflow Tracking\
✅ Centralized Experiment Logging\
✅ S3 Artifact Storage\
✅ Scalable MLOps Setup

------------------------------------------------------------------------

# 💡 Next Steps

-   Add MLflow Model Registry
-   Automate deployment using Docker
-   Integrate with CI/CD
-   Add DVC for data versioning

------------------------------------------------------------------------

Happy Experiment Tracking 🚀
