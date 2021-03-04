# serverless framework tutorial

構成は
S3（Records Bucket）　→　Transcribe　→　S3（Transcribe Bucket）　←　APIGateway
となります。

```bash
npm install

# その後、設定の調整（profileやバケット名）を行い、下記実行。
sls deploy
```