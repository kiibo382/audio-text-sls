aws s3 rm s3://sls-sample-dev-records-bucket1 --recursive
aws s3 rm s3://sls-sample-dev-transcribe-bucket --recursive
aws s3 rm s3://sls-sample-deployment-bucket --recursive
sls remove -v