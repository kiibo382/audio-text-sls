import json
import logging
import os

import boto3
import pymysql.cursors

import query

TRANSCRIBE_BUCKET_NAME = os.environ["TRANSCRIBE_BUCKET_NAME"]
COMPREHEND_BUCKET_NAME = os.environ["COMPREHEND_BUCKET_NAME"]
RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USER_NAME = os.environ["RDS_USER_NAME"]
RDS_USER_PASS = os.environ["RDS_USER_PASS"]
RDS_DB_NAME = os.environ["RDS_DB_NAME"]

s3 = boto3.resource("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def rds_connect():
    try:
        connection = pymysql.connect(
            host=RDS_ENDPOINT,
            user=RDS_USER_NAME,
            password=RDS_USER_PASS,
            database=RDS_DB_NAME,
            connect_timeout=5,
        )
        logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
        return connection
    except Exception as e:
        logger.error(e)
        raise e


def exec_query(uniqueid, connection):
    try:
        with connection:
            with connection.cursor(cursor=pymysql.cursors.DictCursorc) as cursor:
                sql = query.RECORDS_INFO_QUERY
                cursor.execute(sql, uniqueid)
                results = cursor.fetchall()
                logger.info("SUCCESS: execute query succeeded")
                return results
    except Exception as e:
        logger.error(e)
        raise e


def get(event, context):
    key = event["pathParameters"]["proxy"]
    uniqueid = key.split("/")[-1]
    connection = rds_connect()
    query_results = exec_query(uniqueid, connection)

    try:
        for i in query_results:
            response_body = {
                "records_data": query_results,
            }

        return {
            "statusCode": 200,
            "body": json.dumps(response_body, ensure_ascii=False),
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json;charset=UTF-8",
            },
        }

    except Exception as e:
        logger.error(e)
        raise e
