# Serverless Application

local環境はlocalディレクトリ
AWS環境はcloudディレクトリ


## 前提条件

nodejs（version 14.40）のインストール

aws cli のセットアップ（プロファイルの設定等も含む）

direnvのセットアップ

## 構築手順

### 共通

```bash
echo 'export AWS_DEFAULT_PROFILE=必要なprofile' >> ~/.bash_profile
# 必要なプロファイル例:
	# ccti-dev, inop-stg

git clone some URL（リポジトリは未定）

npm install -g serverless
```

### Local環境

```bash
npm install

# .aws/config　に下記を追記
[s3local]
region = ap-northeast-1

# .aws/credentials に下記を追記
[s3local]
aws_access_key_id=S3RVER
aws_secret_access_key=S3RVER

# その後、下記実行
sls offline start

# 疑似S3バケットにwavファイル、jsonファイルをアップロード
./upload.sh

# 実際に下記URLにアクセスして動作確認
# http://localhost:3000/records/{bucket_name}/{key}
# http://localhost:3000/results/{bucket_name}/{key}
```

### AWS環境

処理する音声バケットは現状2つ。増やす場合、

.envファイルに

```jsx
RECORDS_BUCKET_NAME3=kizawa-sample-dev-records-bucket3
```

を追記する。

serverless.yamlに

```yaml
provider:
  environment:
    RECORDS_BUCKET_NAME3: ${env:RECORDS_BUCKET_NAME3}
.
.
.
functions:
  transcribe3:
    handler: transcribe.lambda_handler
    memorySize: 512
    events:
      - s3:
          bucket: ${env:RECORDS_BUCKET_NAME3}
          event: s3:ObjectCreated:*
          existing: true
          rules:
            - suffix: .wav
```

のように、provider.environmentとfunctionsの2項目追記する。

```bash
npm install
sls deploy
```

1. デプロイ後にAWS SNSからメールが届くので、サブスクリプションを許可する。
2. 音声バケットにwavファイルをアップロードする
3. 指定したプロトコル（メール等）のエンドポイントにパスが受信できているか確認。
4. https://{API Gateway のFQDN}/受信したパス　にアクセスし、結果が返ってくることを確認。

### スタック削除

```bash
./delete.sh

# 削除できない場合
aws cloudformation delete-stack --stack-name スタック名
```