import base64
import boto3

s3 = boto3.resource(
    "s3",
    endpoint_url="http://localhost:4569",
    aws_access_key_id="S3RVER",
    aws_secret_access_key="S3RVER",
    region_name="ap-northeast-1",
)


def s3_return_body(bucket_name, key):
    res_obj = s3.Object(bucket_name, key)
    res_data = res_obj.get()
    body = res_data["Body"]
    return body


def get(event, context):
    records_bucket = event["pathParameters"]["records_bucket"]
    key = event["pathParameters"]["proxy"]
    try:
        body = s3_return_body(records_bucket, key)
    except Exception as e:
        print("no such file in the bucket")
        raise e

    try:
        records_bytes = body.read()
        records_encode = base64.b64encode(records_bytes)
        records_decode_str = records_encode.decode()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "audio/wav",
            },
            "body": records_decode_str,
            "isBase64Encoded": True,
        }
    except Exception as e:
        print(e)
        raise e
