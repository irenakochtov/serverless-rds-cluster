import json

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])

        db_name = message.get('db_name')
        db_engine = message.get('db_engine')
        env = message.get('env')

        print(f"Received request to create RDS:")
        print(f"Database Name: {db_name}")
        print(f"Database Engine: {db_engine}")
        print(f"Environment: {env}")

        # בעתיד: לקרוא ל-Terraform או SNS/SQS עם כל הערכים האלו

    return {
        "statusCode": 200,
        "body": json.dumps("RDS request processed")
    }