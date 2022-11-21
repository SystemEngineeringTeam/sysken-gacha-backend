# Swaggerについて
## インストール
### Mac
Homebrewがおすすめ
`brew install swagger-codegen`
## CODEGENの実行コマンド
`swagger-codegen generate -i swagger.yaml -l python-flask -o flask`
### オプションの解説
- -i swaggerの定義ファイルを指定する
- -l 生成するファイルの言語
- -o 生成先のフォルダ
## swaggerの実行
### condaの場合
#### hセットアップ
```shell
conda install connexion
conda install swagger-ui-bundle
```
