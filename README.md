# DevOps & Software Engineer - Technical Assessment

Welcome! The goal of this assessment is to build, test, and deploy a small data processing application on AWS.

This is a practical, hands-on session designed to simulate a real-world task. Please feel free to ask questions at any point.

## 1. Your AWS Environment

We have pre-provisioned a dedicated set of AWS resources for you. Your IAM user has scoped permissions to interact only with these resources.

**Key Resource Names:**
* **ECS Cluster Name:** `candidate-test-cluster`
* **ECR Repository Name:** `candidate-test-repo`
* **S3 Bucket Name:** `candidate-test-bucket2k25`
* **CloudWatch Log Group:** `/ecs/candidate-test-task`

**Networking Details (for Fargate Task):**
* **Subnet ID:** `subnet-048995eadd3bbf8eb`
* **Security Group ID:** `sg-0917ce879ec223119`

## 2. The Task: Micro ETL Service

Your task is to create a containerized Python application that performs an ETL (Extract, Transform, Load) process.

### Core Requirements

1.  **Extract:** The application must fetch data from the public SpaceX API endpoint for all launches: `https://api.spacexdata.com/v4/launches`

2.  **Transform & Load:** Process the JSON data and save the result as a **Parquet file** named `launches.parquet` in the S3 bucket (`candidate-test-bucket2k25`). The transformed data must follow these two rules:
    * **Rule 1 (Select & Rename Fields):** Include only `flight_number`, `name` (as `mission_name`), `date_utc` (as `launch_date`), and `success` (as `mission_successful`).
    * **Rule 2 (Extract Nested Data):** Create a new field `webcast_url` from the `links.webcast` path in the original data.

3.  **Containerize:** Provide a `Dockerfile` for your Python application.

4.  **Deploy & Automate:** **Your deployment process must be automated via one or more scripts** (e.g., `deploy.sh`). Which can be a more robust CI/CD to implement in a situation where you have more time for the task?

5.  **Test / Validate:** Write a simple **integration test** to verify the correctness of your ETL process. The test should run *after* your main application, download the generated Parquet file from S3, and perform assertions to validate its content. This is a critical part of the evaluation.

### Best Practices

* **Configuration:** Your application must be configurable via **environment variables** (e.g., for the S3 bucket name).
* **Dependencies:** How you manage your Python dependencies.

## 3. Submission

Please commit all your code, including the `Dockerfile`, `requirements.txt`, deployment script, and any test files, to your public GitHub repository.

## 4. What We Will Evaluate

* **Code Quality:** Clarity, structure, and adherence to Python best practices.
* **Problem-Solving:** Your approach to fulfilling the requirements.
* **Testing Approach:** The quality and correctness of your integration test. We value this highly.
* **Automation Skills:** The quality and robustness of your deployment script.
* **Cloud-Native Principles:** Use of environment variables and stateless application design.
* **AWS & Docker Skills:** Correctly building and pushing the image, and successfully defining and running the ECS task.

Good luck!
