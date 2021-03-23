import ipaddress
import logging
import os

import pymysql.cursors

import query

RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USER_NAME = os.environ["RDS_USER_NAME"]
RDS_USER_PASS = os.environ["RDS_USER_PASS"]
RDS_DB_NAME = os.environ["RDS_DB_NAME"]


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


def exec_query(event, connection):
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = query.AUTH_QUERY
                cursor.execute(sql, event["headers"]["Authorization"])
                results = cursor.fetchall()
                return results
    except Exception as e:
        logger.error(e)
        raise e


def authorization(event, context):
    connection = rds_connect()
    results = exec_query(event, connection)

    for i in results:
        if i[4] is None or i[5] is None:
            continue
        if ipaddress.ip_address(
            event["requestContext"]["identity"]["sourceIp"]
        ) in ipaddress.ip_network(i[4] + "/" + str(i[5])):
            return {
                "principalId": 1,
                "policyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": "*",
                            "Effect": "Allow",
                            "Resource": event["methodArn"],
                        }
                    ],
                },
            }

    return {
        "principalId": 1,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "*",
                    "Effect": "Deny",
                    "Resource": event["methodArn"],
                }
            ],
        },
    }
