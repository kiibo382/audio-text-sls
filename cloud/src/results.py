import ast
import json
import os

import boto3

TRANSCRIBE_BUCKET_NAME = os.environ["TRANSCRIBE_BUCKET_NAME"]
COMPREHEND_BUCKET_NAME = os.environ["COMPREHEND_BUCKET_NAME"]

s3 = boto3.resource("s3")


def s3_return_body(bucket_name, key):
    res_obj = s3.Object(bucket_name, key)
    res_data = res_obj.get()
    body = res_data["Body"]
    return body


def get(event, context):
    records_bucket = event["pathParameters"]["records_bucket"]
    key = event["pathParameters"]["proxy"]

    try:
        body = s3_return_body(
            TRANSCRIBE_BUCKET_NAME, records_bucket + "/" + key + "-transcribe.json"
        )
        transcribe_dict = ast.literal_eval(
            body.read().decode("UTF-8")
        )
        transcribe_res = transcribe_dict["results"]["transcripts"]
    except Exception as e:
        print("no such file in the transcribe bucket")
        raise e

    try:
        comprehend_obj = s3.Object(
            COMPREHEND_BUCKET_NAME, records_bucket + "/" + key + "-comprehend.json"
        )
        comprehend_data = comprehend_obj.get()
    except Exception as e:
        print("no such file in the comprehend bucket")
        raise e

    try:
        response_body = {
            "transcirbe_result": transcribe_res,
            "comprehend_result": ast.literal_eval(
                comprehend_data["Body"].read().decode("UTF-8")
            ),
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_body),
            "isBase64Encoded": False,
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(e)
        raise e
