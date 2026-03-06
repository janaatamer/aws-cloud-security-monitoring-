import boto3
from datetime import datetime

sns_client = boto3.client("sns")
SNS_TOPIC_ARN = "arn:aws:sns:eu-north-1:369012867517:security-alerts"

def lambda_handler(event, context):

    detail = event.get("detail", {})

    user = detail.get("userIdentity", {}).get("userName", "Unknown")
    instance_id = detail.get("requestParameters", {}).get("instancesSet", {}).get("items", [{}])[0].get("instanceId", "Unknown")

    region = event.get("region", "Unknown")
    time = event.get("time", datetime.utcnow().isoformat())

    message = f"""
AWS Security Alert
=================
Event Type: EC2 Instance Started

User: {user}
Instance ID: {instance_id}
Region: {region}
Time: {time}

Action Required:
Verify this instance startup was authorized.
"""

    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="AWS Security Alert: EC2 Instance Started",
        Message=message
    )

    return {"statusCode": 200}
