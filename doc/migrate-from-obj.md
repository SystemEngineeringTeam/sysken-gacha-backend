# C#オブジェクトのコードからsqliteへの移植
## スクリプトの実行方法
`./script/migrate-from-obj.sh　<テキストファイル名> <sqliteファイル名> <画像フォルダ>`
を実行すると、プロジェクトのルートディレクトリにsqliteのファイルが生成されます。

データベースの場所を変更しない&フォルダパスはUnity側で処理する場合は以下のようになります
`./script/migrate-from-obj.sh　<テキストファイル名> database.db ''`