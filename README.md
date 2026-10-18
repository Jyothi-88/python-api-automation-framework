# Python API Automation Framework with AWS & AI Pricing Validation

A Python-based API test automation framework demonstrating REST API testing, reusable test components, negative testing, AWS service integration patterns, and validation of mocked AI-generated pricing outputs.

## Project Overview

This project demonstrates a modular approach to API test automation using **Python, pytest, requests, responses, and boto3**.

The framework focuses on testing an illustrative Order Management API, including order creation, retrieval, status updates, deletion, authentication, and validation scenarios.

It also includes AWS integration components and a standalone pricing validation harness to demonstrate additional quality engineering considerations.

## Key Features

- **REST API Automation:** Positive and negative API test scenarios covering order operations and validation.
- **Reusable API Client:** Centralized HTTP request handling using Python requests.
- **Mocked API Testing:** HTTP response simulation using the responses library, without requiring a running API server.
- **Authentication Testing:** Missing and invalid bearer-token scenarios.
- **Data-Driven Testing:** pytest parameterization for order deletion state rules.
- **AWS Secrets Manager:** API token retrieval helper using boto3.
- **AWS SQS:** Order status-change event publishing with a mocked SQS client in the test suite.
- **AWS CloudWatch:** Optional test-suite completion metric publishing.
- **AI Pricing Validation:** Range-based validation of mocked pricing outputs, including outlier detection.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Automation development |
| pytest | Test execution, fixtures, parameterization |
| requests | REST API client |
| responses | HTTP mocking |
| boto3 | AWS service integration |
| AWS Secrets Manager | Credential retrieval |
| AWS SQS | Event publishing |
| AWS CloudWatch | Optional execution metrics |

## Repository Structure

```text
python-api-automation-framework/
│
├── tests/
│   ├── api_client.py
│   ├── aws_secrets.py
│   ├── order_events.py
│   └── test_orders.py
│
├── pricing_harness.py
├── conftest.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Test Coverage

The automated API test suite includes 16 test cases covering:

- Successful order creation
- Invalid order weights
- Incomplete pickup and drop-off addresses
- Missing and invalid authentication
- Successful order retrieval
- Order-not-found handling
- Order deletion rules across different statuses
- Successful order status updates
- Invalid status transitions
- SQS order status-change event publishing

The tests use mocked responses and dependencies to support repeatable execution without external API or AWS infrastructure.

## Getting Started

### Prerequisites

- Python 3.11 or later
- pip

### Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the API Test Suite

```bash
pytest -v
```

**Latest local validation: 16 tests passed.**

The API requests are mocked, so no live API server is required.

## AI Pricing Output Validation

The standalone `pricing_harness.py` demonstrates validation of mocked AI-generated pricing outputs against predefined acceptable ranges.

The harness:

- Evaluates sample pricing scenarios
- Compares mocked outputs against minimum and maximum thresholds
- Reports pass/fail results
- Identifies out-of-range pricing values
- Returns a nonzero exit code when validation fails

Run it using:

```bash
python pricing_harness.py
```

**Note:** The harness intentionally includes an outlier scenario. A nonzero exit code demonstrates that the validation guardrail has detected an unacceptable output; it does not mean the API pytest suite failed.

The project does not invoke or train a live AI model.

## AWS Integration

The framework includes boto3-based components for AWS Secrets Manager, SQS, and CloudWatch.

- Secrets Manager provides a helper for retrieving API tokens by secret name.
- SQS provides an order status-change event publisher.
- CloudWatch publishing is optional and controlled through an environment variable.

AWS service integrations require suitable configuration and permissions when used against actual AWS services. The default API tests do not require live AWS access.

## Configuration

The API client fixture supports the following environment variables:

| Variable | Purpose |
|---|---|
| `API_BASE_URL` | API endpoint, defaulting to a sample test URL |
| `API_TOKEN` | API bearer token, defaulting to a placeholder |
| `AWS_REGION` | Region for optional CloudWatch publishing |
| `PUBLISH_CLOUDWATCH_METRIC` | Enables optional CloudWatch metric publishing when set to `true` |

Do not commit actual credentials, tokens, or environment-specific secrets.

## Scope and Limitations

This is a portfolio demonstration project, not a production-deployed API service.

- API responses are mocked.
- The AI pricing values are simulated.
- AWS integrations are implemented as reusable boto3 components; live AWS integration testing is not claimed.
- Test cases demonstrate expected behavior for an illustrative Order Management API rather than validating a deployed service.

## Quality Engineering Approach

The project emphasizes reusable automation design, positive and negative test coverage, authentication validation, test isolation, event verification, and explicit checks on AI-generated outputs.

The goal is to demonstrate practical API automation implementation alongside security, maintainability, and risk-based quality considerations.

## About the Author

**Jyothi G.M.**  
**QA Lead | Software Quality Engineering | Test Automation**

QA professional with 8.5+ years of experience in software testing, quality assurance, test strategy, and QA leadership.

Experienced in Functional testing, API testing, Selenium with Java, Python with Robot Framework, Agile methodologies, and test planning, with a focus on developing practical automation solutions using Python, pytest, and AWS integrations.

This project is part of my technical portfolio, demonstrating hands-on implementation of API automation, reusable testing components, and AI output validation.

**GitHub:** [Jyothi-88](https://github.com/Jyothi-88)

**LinkedIn:** [Jyothi G.M.](https://www.linkedin.com/in/jyothi-aradhya/)