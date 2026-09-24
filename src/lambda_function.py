import json
import os

import boto3

from bill_rules import assess

dynamodb = boto3.resource("dynamodb")
stats_table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    body = json.loads(event["body"])
    result = assess(
        body["server_type"],
        body["hours"],
        body["db_type"],
        body["db_hours"],
        body["nat"],
        body["gb_stored"],
        body["gb_out"],
    )
    try:
        stats_table.update_item(
            Key={"statId": "visits"},
            UpdateExpression="ADD visit_count :one",
            ExpressionAttributeValues={":one": 1},
        )
    except Exception as error:
        print("Counter update failed:", error)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result),
    }