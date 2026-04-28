# api-suhebghare

A serverless REST API that serves personal profile and blog data for [suhebghare.tech](https://suhebghare.tech).

## Overview

This project is a complete serverless stack on AWS that exposes GET API endpoints returning JSON data about Suheb Ghare — profile information and blog articles. The data is sourced from two static JSON files (`profile.json` and `blogs.json`) bundled with the Lambda function.

## Architecture

```
Client → API Gateway (REST API) → Lambda (Python) → Returns JSON from profile.json / blogs.json
```

### AWS Services Used

- **AWS Lambda** (Python 3.12 runtime) — serves the API logic
- **Amazon API Gateway** (REST API) — public HTTP endpoint with CORS enabled
- **AWS IAM** — least-privilege execution role for Lambda
- **AWS CloudFormation / SAM** — infrastructure as code using AWS SAM (Serverless Application Model)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/profile` | Returns full profile data from `profile.json` |
| GET | `/blogs` | Returns all blog/article data from `blogs.json` |
| GET | `/health` | Returns `{ "status": "healthy" }` |

All endpoints must return JSON with appropriate `Content-Type: application/json` header and CORS headers (`Access-Control-Allow-Origin: *`).

## Project Structure

```
api-suhebghare/
├── README.md
├── profile.json              # Personal profile data (experience, skills, projects, etc.)
├── blogs.json                # Blog articles and metadata
├── src/
│   └── handler.py            # Lambda handler — reads JSON files and returns responses
├── template.yaml             # AWS SAM template defining API Gateway + Lambda + IAM
├── samconfig.toml             # SAM CLI deployment configuration
├── requirements.txt          # Python dependencies (if any)
├── tests/
│   └── test_handler.py       # Unit tests for the Lambda handler
└── .github/
    └── workflows/
        └── deploy.yml        # GitHub Actions CI/CD pipeline for auto-deploy to AWS
```

## Lambda Handler Requirements

- Single Python handler file (`src/handler.py`)
- Reads `profile.json` and `blogs.json` from the Lambda package (same directory or relative path)
- Routes requests based on the API Gateway event path (`/profile`, `/blogs`, `/health`)
- Returns proper HTTP responses with status code, JSON body, and CORS headers
- Handles errors gracefully with 404 for unknown paths and 500 for internal errors

## Infrastructure (SAM Template)

The `template.yaml` should define:

- **AWS::Serverless::Function** for the Lambda
  - Runtime: `python3.12`
  - Handler: `src/handler.lambda_handler`
  - MemorySize: `128`
  - Timeout: `10`
  - Architecture: `arm64` (Graviton for cost efficiency)
  - Events: API Gateway events for each route (`/profile`, `/blogs`, `/health`)
- **API Gateway** with CORS enabled globally
- **Outputs**: API endpoint URL

## CI/CD — GitHub Actions

The `.github/workflows/deploy.yml` pipeline should:

1. **Trigger** on push to `main` branch
2. **Steps**:
   - Checkout code
   - Set up Python 3.12
   - Install dependencies
   - Run unit tests
   - Set up AWS SAM CLI
   - Configure AWS credentials (using GitHub Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`)
   - Run `sam build`
   - Run `sam deploy --no-confirm-changeset --no-fail-on-empty-changeset`

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM user access key with CloudFormation, Lambda, API Gateway, IAM, S3 permissions |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | AWS region to deploy to (e.g., `ap-south-1`) |

## Data Files

### `profile.json`
Contains: name, title, summary, location, contact info, education, certifications, work experience, skills (cloud, containers, CI/CD, observability, security, AI/LLM, languages), core competencies, projects, and stats.

### `blogs.json`
Contains: profile metadata, experience highlights, detailed skills breakdown, expertise areas, and project case studies with impact metrics and article links.

## Local Development

```bash
# Build
sam build

# Start local API
sam local start-api

# Test endpoints
curl http://localhost:3000/profile
curl http://localhost:3000/blogs
curl http://localhost:3000/health

# Run tests
python -m pytest tests/
```

## Deployment

Automatic deployment happens on every push to `main` via GitHub Actions. For manual deployment:

```bash
sam build
sam deploy --guided   # first time
sam deploy            # subsequent deploys
```
