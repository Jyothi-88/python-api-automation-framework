import os

import boto3
import pytest

from tests.api_client import OrderApiClient


@pytest.fixture
def order_api_client():
    return OrderApiClient(
        base_url=os.getenv("API_BASE_URL", "https://api.example.test/v1"),
        token=os.getenv("API_TOKEN", "test-token"),
    )


def pytest_sessionfinish(session, exitstatus):
    """Optionally publish a test-suite completion metric to CloudWatch."""

    if os.getenv("PUBLISH_CLOUDWATCH_METRIC", "").lower() != "true":
        return

    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )

    cloudwatch.put_metric_data(
        Namespace="QA-Automation",
        MetricData=[
            {
                "MetricName": "PytestSuiteCompleted",
                "Value": 1,
                "Unit": "Count",
            }
        ],
    )