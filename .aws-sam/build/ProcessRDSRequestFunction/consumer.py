import json

def lambda_handler(event, context):
    for record in event['Records']:
        message = record['body']
        print(f"Received message from SQS: {message}")
        # כאן בהמשך תשלבי קריאה ל-Terraform או פעולה אחרת
    return {
        "statusCode": 200,
        "body": json.dumps("Messages processed")
    }