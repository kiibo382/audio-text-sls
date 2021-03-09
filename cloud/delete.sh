#!/bin/bash

aws s3 rm s3://${SERVICE_NAME}-${STAGE}-comprehend-bucket --recursive
sls remove -v