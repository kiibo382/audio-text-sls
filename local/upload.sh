aws --endpoint="http://localhost:4569" \
    s3 cp sample/sample.mp3 s3://${SERVICE_NAME}-${STAGE}-records-bucket1/sample.mp3 \
    --profile s3local

aws --endpoint="http://localhost:4569" \
    s3 cp sample/sample.wav s3://${SERVICE_NAME}-${STAGE}-records-bucket1/sample.wav \
    --profile s3local

aws --endpoint="http://localhost:4569" \
    s3 cp sample/sample-transcribe.json s3://${SERVICE_NAME}-${STAGE}-transcribe-bucket/${SERVICE_NAME}-${STAGE}-records-bucket1/sample-transcribe.json \
    --profile s3local

aws --endpoint="http://localhost:4569" \
    s3 cp sample/sample-comprehend.json s3://${SERVICE_NAME}-${STAGE}-comprehend-bucket/${SERVICE_NAME}-${STAGE}-records-bucket1/sample-comprehend.json \
    --profile s3local