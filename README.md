# シス研ガチャバックエンドサーバー

## 概要
シス研ガチャのAPIです。
[OpenAPI Generator](https://openapi-generator.tech) によって生成されました。
[OpenAPI-Spec](https://openapis.org) に準拠しています。
[Connexion](https://github.com/zalando/connexion)を使用しています。

## 必要バージョン
Python 3.5.2+

## 設定
.envファイルを使用して、サーバーの設定を変更できます。

```
DB_PATH=./db.sqlite3
IMG_PATH=./img
```

## オブジェクトからのデータベースの作成
```
./scripts/migrate-from-obj.sh
```

## 使用方法
プログラムを実行する場合は、以下のコマンドを実行してください。

```
pip3 install -r requirements.txt
python3 -m openapi_server
```

APIは以下のURLで確認できます。

```
http://localhost:8080/ui/
```

Your OpenAPI definition lives here:

```
http://localhost:8080/openapi.json
```

テストは以下のコマンドで実行できます。

```
sudo pip install tox
tox
```

## Dockerで実行する場合

 Docker containerで実行するには, プロジェクトのルートディレクトリで以下のコマンドを実行してください。

```bash
# building the image
docker build -t openapi_server .

# starting up a container
docker run -p 8080:8080 openapi_server
```

## コードを変更する場合

エンドポイントを変更するには、`openapi/openapi.yaml`を変更してください。
コードは、`openapi_server`ディレクトリに生成されます。
データベースのモデルは、`openapi_server/models`ディレクトリに生成されます。
データ処理ロジックは、`openapi_server/controllers`ディレクトリに生成されます。