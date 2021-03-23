import boto3
import logging
import os
import urllib.parse


transcribe = boto3.client("transcribe")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
MINIMUM_RECORDS_SIZE = os.environ["MINIMUM_RECORDS_SIZE"]


def handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    print("event s3 obj")
    print(type(event["Records"][0]["s3"]["object"]["size"]))
    print(event["Records"][0]["s3"]["object"]["size"])
    if event["Records"][0]["s3"]["object"]["size"] < MINIMUM_RECORDS_SIZE:
        raise Exception("Records file is too small.")
    path_list = key.split("/")

    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=path_list[-1] + "_Transcription",
            LanguageCode="ja-JP",
            Media={
                "MediaFileUri": "https://s3.ap-northeast-1.amazonaws.com/"
                + bucket
                + "/"
                + key
            },
            OutputBucketName=os.environ["TRANSCRIBE_BUCKET_NAME"],
            OutputKey=bucket + "/" + key[:-4] + "-transcribe.json",
        )
    except Exception as e:
        logger.error(e)
        logger.error("Error transcribe object {} in bucket {}".format(key, bucket))
        raise e
