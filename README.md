# Serverless Application


## Architecture
![serverless](https://user-images.githubusercontent.com/64523345/110412110-01b29b00-80cf-11eb-9177-9d6af11d9333.png)

## Setup
### Installation
 - Node.js (version 14.40)
 - aws cli (including profile settings, etc.)
 - (optional) direnv
 - python3
  - boto3

### Common

```bash
echo 'export AWS_DEFAULT_PROFILE=Required profile' >> ~/.bash_profile

echo 'export AWS_SDK_LOAD_CONFIG=1' >> ~/.bash_profile

git clone https://github.com/kiibo382/audio-text-sls.git
```

## Usage

### Tutorial

```bash
cd sls-tutorial
npm install

# Then, adjust the settings (profile and bucket name) in serverless.yml and delete.sh, and execute the following.
npm run sls-deploy
```

### Local

```bash
cd local
npm install

# Add the following to `.aws/config`
[s3local]
region = ap-northeast-1

# Add the following to `.aws/credentials`
[s3local]
aws_access_key_id=S3RVER
aws_secret_access_key=S3RVER

# Then, adjust settings (profile and bucket name) in the .env file and execute the following.
npm run sls-offline

# Upload wav and json files to minio (S3 compatible object storage)
./upload.sh

# Access the following URL to check the operation.
# http://localhost:3000/records/{bucket_name}/{key}
# http://localhost:3000/results/{bucket_name}/{key}
```

### Production

```bash
cd cloud
npm install
npm run sls-deploy
```
After executing the command, please do the following.

1. after deployment, allow subscriptions you will receive from AWS SNS via email.
2. upload the wav file to the audio bucket
3. check if the path is received at the endpoint of the specified protocol (such as email).
4. access `https://{FQDN of the API Gateway}/{path received}` and confirm that the result is returned.

#### Note
The voice buckets to be processed are assumed to be two existing S3 buckets.
If you are creating a new voice bucket, please make sure that your `serverless.yml` is as follows

```yaml
fucntions:
  transcribe1:
    handler: transcribe.handler
    memorySize: 512
    events:
      - s3:
          bucket: ${env:RECORDS_BUCKET_NAME1}
          event: s3:ObjectCreated:*
          rules:
            - suffix: .wav
  transcribe2:
    handler: transcribe.handler
    memorySize: 512
    events:
      - s3:
          bucket: ${env:RECORDS_BUCKET_NAME2}
          event: s3:ObjectCreated:*
          rules:
            - suffix: .wav

```

To add a bucket, append the name of the S3 bucket to the `.env` file. (See example below.)

```jsx
RECORDS_BUCKET_NAME3=sls-sample-dev-records-bucket3
```

Also, add the following two items to `serverless.yaml`: provider.environment and functions.

```yaml
provider:
  environment:
    RECORDS_BUCKET_NAME3: ${env:RECORDS_BUCKET_NAME3}
.
.
.
functions:
  transcribe3:
    handler: transcribe.handler
    memorySize: 512
    events:
      - s3:
          bucket: ${env:RECORDS_BUCKET_NAME3}
          event: s3:ObjectCreated:*
          existing: true
          rules:
            - suffix: .wav
```

### Clean up

```bash
./delete.sh
```
