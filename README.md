# Flask Student Registration System – CI/CD Pipeline using GitHub Actions

## Project Overview

This project demonstrates a complete Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Flask-based Student Registration application.

The application is containerized using Docker, stored in Amazon Elastic Container Registry (ECR), and automatically deployed to an Amazon EC2 instance using GitHub Actions.

MongoDB Atlas is used as the backend database, and every deployment is verified through a health check endpoint. Email notifications are sent for both successful and failed pipeline executions.

---

## Technology Stack

- Python 3.12
- Flask
- MongoDB Atlas
- Docker
- GitHub Actions
- Amazon ECR
- Amazon EC2
- Pytest
- Gmail SMTP (Email Notifications)

---

## Project Structure

```
flask_Practice/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── templates/
├── Dockerfile
├── app.py
├── requirements.txt
├── test_app.py
├── README.md
└── start_flask.sh
```

---

## CI/CD Workflow

The pipeline is automatically triggered whenever code is pushed to the **main** branch. It can also be executed manually using the GitHub Actions **Run Workflow** option.

The pipeline performs the following steps:

1. Checkout source code
2. Configure Python
3. Install project dependencies
4. Execute Pytest test cases
5. Configure AWS credentials
6. Login to Amazon ECR
7. Build Docker image
8. Tag image using Git Commit SHA
9. Push image to Amazon ECR
10. Connect to EC2 using SSH
11. Pull latest Docker image
12. Replace the running container
13. Execute application health check
14. Send success or failure email notification

---

## CI/CD Architecture

```
                Developer

                     │
              git push main

                     │

                     ▼

          GitHub Actions Pipeline

                     │

         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼

     Run Pytest             Docker Build

                     │

                     ▼

              Push Image to ECR

                     │

                     ▼

             SSH into EC2 Instance

                     │

                     ▼

           Pull Latest Docker Image

                     │

                     ▼

        Stop Existing Docker Container

                     │

                     ▼

        Start New Docker Container

                     │

                     ▼

           Execute /health Endpoint

                     │

         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼

   Success Email           Failure Email
```

---

## Docker Image

The application is packaged as a Docker image.

Docker image naming convention:

```
<ECR Repository>:<Git Commit SHA>
```

Using the commit SHA ensures every deployment is uniquely versioned and traceable.

---

## Health Check

The application exposes the following endpoint:

```
/health
```

This endpoint is used after deployment to verify that the application is running successfully before the pipeline is marked as successful.

---

## Automated Testing

Pytest is used as the testing framework.

The following functionality is validated automatically during every pipeline execution:

- Health endpoint
- Home page
- Add Student
- Update Student
- Delete Student

The deployment process continues only if all tests pass successfully.

---

## Email Notifications

The pipeline sends email notifications for both scenarios:

### Success

The email includes:

- Branch name
- Commit SHA
- EC2 deployment target
- Health check status
- GitHub Actions run link

### Failure

The email includes:

- Failed pipeline stage
- Branch name
- Commit SHA
- GitHub Actions log link

This helps identify deployment issues quickly.

---

## AWS Resources Used

### Amazon EC2

Hosts the Docker container running the Flask application.

### Amazon ECR

Stores Docker images built during every pipeline execution.

### IAM

Used for secure authentication between GitHub Actions and AWS services.

---

## GitHub Secrets

The following repository secrets are configured:

```
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

EC2_HOST

EC2_SSH_KEY

MONGO_URI

FLASK_SECRET_KEY

SMTP_USERNAME

SMTP_PASSWORD

EMAIL_TO
```

Sensitive information is never stored in the source code.

---

## Running the Application Locally

Clone the repository:

```bash
git clone https://github.com/bkori17/flask_Practice.git

cd flask_Practice
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the environment variables:

```
MONGO_URI=<MongoDB Atlas Connection String>

SECRET_KEY=<Your Secret Key>
```

Run the application:

```bash
python app.py
```

Open:

```
http://localhost:5000
```

---

## Running with Docker

Build the Docker image:

```bash
docker build -t flask-practice .
```

Run the container:

```bash
docker run -d \
-p 5000:5000 \
--name flask-practice-container \
-e MONGO_URI="<MongoDB URI>" \
-e SECRET_KEY="<Secret Key>" \
flask-practice
```

Application URL:

```
http://localhost:5000
```

---

## Pipeline Validation

The project was successfully validated by:

- Executing all Pytest test cases
- Building Docker image
- Pushing image to Amazon ECR
- Deploying updated container on EC2
- Verifying deployment using `/health`
- Receiving success email notification
- Verifying pipeline failure using an intentionally failed execution
- Receiving failure email notification

---

## Repository

GitHub Repository:

```
https://github.com/bkori17/flask_Practice
```

---

## Conclusion

This project demonstrates a complete CI/CD implementation using GitHub Actions and AWS services. Every code change is automatically validated through testing, packaged into a Docker image, stored in Amazon ECR, deployed to Amazon EC2, verified using a health check, and reported through automated email notifications.

This pipeline ensures consistent, repeatable, and reliable deployments while reducing manual intervention.
