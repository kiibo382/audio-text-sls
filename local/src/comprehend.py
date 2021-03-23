import json
import logging
import os
import urllib.parse

import boto3

s3 = boto3.resource("s3")
comprehend = boto3.client("comprehend")
COMPREHEND_BUCKET_NAME = os.environ["COMPREHEND_BUCKET_NAME"]
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def s3_return_body(bucket_name, key):
    res_obj = s3.Object(bucket_name, key)
    res_data = res_obj.get()
    body = json.load(res_data["Body"])
    return body


def handler(event, context):
    TRANSCRIBE_BUCKET_NAME = event["Records"][0]["s3"]["bucket"]["name"]
    input_key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    try:
        body = s3_return_body(TRANSCRIBE_BUCKET_NAME, input_key)
    except Exception as e:
        logger.error(
            "Error comprehend object {} in bucket {}".format(
                input_key, TRANSCRIBE_BUCKET_NAME
            )
        )
        logger.error(e)
        raise e

    try:
        transcript = ""
        for i in body["results"]["transcripts"]:
            transcript += i["transcript"]

        sentiment_response = comprehend.detect_sentiment(
            Text=transcript, LanguageCode="ja"
        )
        key_phrases = comprehend.detect_key_phrases(Text=transcript, LanguageCode="ja")
    except Exception as e:
        logger.error("Error comprehend")
        logger.error(e)
        raise e

    output_key = input_key.replace("transcribe", "comprehend")
    res_dict = {
        "Sentiment": sentiment_response["Sentiment"],
        "SentimentScore": sentiment_response["SentimentScore"],
        "KeyPhrases": key_phrases["KeyPhrases"],
    }

    try:
        put_obj = s3.Object(COMPREHEND_BUCKET_NAME, output_key)
        put_obj.put(Body=json.dumps(res_dict))
    except Exception as e:
        logger.error("Error upload comprehend data into s3 bucket.")
        logger.error(e)
        raise e
