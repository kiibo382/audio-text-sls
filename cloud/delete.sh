aws s3 rm s3://${SERVICE_NAME}-${STAGE}-records-bucket1 --recursive
aws s3 rm s3://${SERVICE_NAME}-${STAGE}-records-bucket2 --recursive
aws s3 rm s3://${SERVICE_NAME}-${STAGE}-transcribe-bucket --recursive
aws s3 rm s3://${SERVICE_NAME}-${STAGE}-comprehend-bucket --recursive
aws s3 rm s3://${SERVICE_NAME}-${STAGE}-deployment-bucket --recursive
sls remove