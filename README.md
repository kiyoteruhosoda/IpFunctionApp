# IpFunctionApp

Azure Functions でアクセス元IPアドレスをJSONで返すサーバーレス関数アプリです。

## 機能
- HTTPトリガーでアクセスしたクライアントのIPアドレスを取得し、`{"ip": "xxx.xxx.xxx.xxx"}` の形式で返します。

## ローカルでの実行方法

1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

2. Azure Functions のローカル実行

```bash
func start
```

3. 動作確認

ブラウザやcurlで以下のURLにアクセスしてください。

```
http://localhost:7071/api/GetIpFunction
```

### レスポンス例
```json
{"ip": "203.0.113.1"}
```

## デプロイ
AzureポータルやAzure CLIを使ってデプロイ可能です。

## 注意
- `local.settings.json` には機密情報が含まれるためGit管理されません。
- Azure Functions Core Tools（funcコマンド）が必要です。

## ライセンス
このリポジトリはMITライセンスです。