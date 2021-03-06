# Serverless Application


## 構成は以下
![serverless](https://user-images.githubusercontent.com/64523345/110412110-01b29b00-80cf-11eb-9177-9d6af11d9333.png)

<br>local環境はlocalディレクトリ
<br>AWS環境はcloudディレクトリ
<br>sls-tutorialディレクトリはserverless frameworkチュートリアル用


## 前提条件

nodejs（version 14.40）のインストール

aws cli のセットアップ（プロファイルの設定等も含む）

direnvのセットアップ

## 構築手順

### 共通

```bash
echo 'export AWS_DEFAULT_PROFILE=必要なprofile' >> ~/.bash_profile

echo 'export AWS_SDK_LOAD_CONFIG=1' >> ~/.bash_profile

git clone https://github.com/kiibo382/audio-text-sls.git
```

### serverless framework 練習用

解説を加え、少し機能を少なくしたバージョン。チュートリアル用にご使用ください。

```bash
cd sls-tutorial
npm install

# その後、serverless.ymlとdelete.shにて設定の調整（profileやバケット名）を行い、下記実行。
npm run sls-deploy
```

### Local環境

事前にローカル環境に
 - python のインストール
 - boto3 のインストール<br>

を済ましておいてください。

```bash
cd local
npm install

# .aws/config　に下記を追記
[s3local]
region = ap-northeast-1

# .aws/credentials に下記を追記
[s3local]
aws_access_key_id=S3RVER
aws_secret_access_key=S3RVER

# その後、.envファイルにて設定の調整（profileやバケット名）を行い、下記実行。
npm run sls-offline

# 疑似S3バケットにwavファイル、jsonファイルをアップロード
./upload.sh

# 下記URLにアクセスして動作確認
# http://localhost:3000/records/{bucket_name}/{key}
# http://localhost:3000/results/{bucket_name}/{key}
```

### AWS環境

処理する音声バケットは現状2つ。既存のS3バケットを想定しています。新規に音声バケットを作る場合、

serverless.yml
```yaml
fucntions:
  transcribe1:
    handler: transcribe.handler
    memorySize: 512
    events:
      - s3:
          bucket: ${env:RECORDS_BUCKET_NAME1}
          event: s3:ObjectCreated:*
          existing: true
          rules:
            - suffix: .wav
  transcribe2:
    handler: transcribe.handler
    memorySize: 512
    events:
      - s3:
          bucket: ${env:RECORDS_BUCKET_NAME2}
          event: s3:ObjectCreated:*
          existing: true
          rules:
            - suffix: .wav

```

から

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

に変更してください。（つまりexisiting: trueを削除する。）<br>
増やす場合、
.envファイルに

```jsx
RECORDS_BUCKET_NAME3=sls-sample-dev-records-bucket3
```

等、S3バケット名を追記する。

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

のように、provider.environmentとfunctionsの2項目追記する。

```bash
cd cloud
npm install

# その後、.envファイルにて設定の調整（profileやバケット名）を行い、下記実行。
npm run sls-deploy
```

1. デプロイ後にAWS SNSからメールが届くので、サブスクリプションを許可する。
2. 音声バケットにwavファイルをアップロードする
3. 指定したプロトコル（メール等）のエンドポイントにパスが受信できているか確認。
4. https://{API Gateway のFQDN}/受信したパス　にアクセスし、結果が返ってくることを確認。

### スタック削除

```bash
./delete.sh

# 削除できない場合
./delete-force.sh
# または
aws cloudformation delete-stack --stack-name スタック名
```
