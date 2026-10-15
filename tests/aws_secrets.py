import boto3


def get_api_token(secret_name: str, region_name: str = "ap-south-1") -> str:
    """Fetch an API token securely from AWS Secrets Manager."""
    client = boto3.client("secretsmanager", region_name=region_name)

    response = client.get_secret_value(SecretId=secret_name)

    return response["SecretString"]