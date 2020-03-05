# atcoder-userinfo-notifier

## これは何？

<img src="https://github.com/nafuka11/atcoder-userinfo-notifier/blob/images/screenshot.png" width="510" alt="screenshot">

特定ユーザのAtCoderの成績を毎日取得し、上位5人の成績をSlackに投稿するスクリプトです。

Pythonで書かれていて、AWS Lambda上で動きます。

## 使い方

### 必要物
- AWSアカウント
- Node.js
- SlackのIncoming Webhook URL

### 手順
1. Serverless Frameworkのインストール
   - [公式](https://github.com/serverless/serverless)のQuick Startの手順を実行してください。
     <注意点>
     - 手順2のVideoの内容は古いです。[ドキュメント](https://github.com/serverless/serverless/blob/master/docs/providers/aws/guide/credentials.md)を読みましょう。
     - ドキュメントにあるgistはssmの権限がないため、以下を`Action`に追加してください。
       ```json
       "ssm:GetParameters",
       "ssm:GetParameter"
       ```
2. ssmの追加
   - AWSコンソール > AWS System Manager > パラメータストア > パラメータの作成

     各項目の値を以下のように設定し、`パラメータの作成` ボタン押下。
     |項目|値|
     |--|--|
     |名前|`/atcoder-userinfo-notifier/slack-url`|
     |利用枠|標準|
     |タイプ|安全な文字列|
     |KMS の主要なソース|現在のアカウント|
     |KMS キー ID|（そのままでよい）|
     |値|（SlackのIncoming Webhook URL）|
3. userlist.txtの編集
   1. `userlist_example.txt` をリネーム
      ```bash
      mv userlist_example.txt userlist.txt
      ```
   2. `userlist.txt` の編集
      - AtCoderのuseridを改行区切りで記入してください。末尾に改行は不要です。
4. 動作確認
   - 以下のコマンドを実行し、Slackのチャンネルにメッセージが投稿されていることを確認します。
     ```bash
     sls invoke local -f atcoder-userinfo-notifier
     ```
5. serverless.ymlの編集
   - 初期設定では `04:02` にメッセージが投稿されます。

     変更したい場合は、 `schedule` を変更してください（外部APIにアクセスするので頻繁な設定はやめてね）。
6. デプロイ
   -  ```bash
      sls deploy
      ```
