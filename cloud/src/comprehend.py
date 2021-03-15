import json
import os
import urllib.parse

import boto3

s3 = boto3.resource("s3")
comprehend = boto3.client("comprehend")
sns = boto3.resource("sns")
COMPREHEND_BUCKET_NAME = os.environ["COMPREHEND_BUCKET_NAME"]
TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


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
        print(
            "Error comprehend object {} in bucket {}".format(
                input_key, TRANSCRIBE_BUCKET_NAME
            )
        )
        print(e)
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
        print("Error comprehend")
        print(e)
        raise e

    output_key = input_key.replace("transcribe", "comprehend")
    res_dict = {
        "Sentiment": sentiment_response["Sentiment"],
        "SentimentScore": sentiment_response["SentimentScore"],
        "KeyPhrases": key_phrases["KeyPhrases"],
    }

    try:
        put_obj = s3.Object(COMPREHEND_BUCKET_NAME, output_key)
        put_obj.put(Body=json.dumps(res_dict, ensure_ascii=False))
    except Exception as e:
        print("Error upload comprehend data into s3 bucket.")
        print(e)
        raise e

    try:
        topic = sns.Topic(TOPIC_ARN)
        message_text = {
            "record_path": "records/" + output_key.replace("-comprehend.json", ".wav"),
            "result_path": "results/" + output_key.replace("-comprehend.json", ""),
        }
        message = {
            "default": json.dumps(message_text),
            "record_path": "records/" + output_key.replace("-comprehend.json", ".wav"),
            "result_path": "results/" + output_key.replace("-comprehend.json", ""),
        }
        topic.publish(Message=json.dumps(message), MessageStructure="json")
    except Exception as e:
        print("Error send message to SNS")
        print(e)
        raise e
