import json

import boto3


class OrderEventPublisher:
    """Publishes order state-change events to an AWS SQS queue."""

    def __init__(self, queue_url: str, region_name: str = "ap-south-1"):
        self.queue_url = queue_url
        self.sqs = boto3.client("sqs", region_name=region_name)

    def publish_status_change(
        self,
        order_id: str,
        old_status: str,
        new_status: str,
    ):
        message = {
            "event_type": "ORDER_STATUS_CHANGED",
            "order_id": order_id,
            "old_status": old_status,
            "new_status": new_status,
        }

        return self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message),
        )