#!/bin/bash
#dest_default='database.db'
if [ $# -ne 1 ]; then
	echo "Usage: $0 <source>"
	echo "使用方法: $0 <C#のコードの場所>"
fi
source .env
if [ ! -e $2 ]; then
	echo "Destination $DB_PATH does not exist. Creating..."
	sqlite3 $DB_PATH "
  CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY,
    description TEXT,
    rare INTEGER,
    image TEXT
  );"
fi
CURRENT=$(cd $(dirname "$0") && pwd)
echo "Migrating from $1 to $DB_PATH"
echo "Current directory: $CURRENT"
cat $1 | sed -r -f $CURRENT/replace.sed | nl -s '' -nln | sed 's/  */,/g' >csv
sqlite3 $DB_DB_PATH ".mode csv" \
	".import ./csv items" \
	"update items set image = '${3}resource (' || id || ').jpg' "
echo "INFO:データが 1列 足りない と出るのは仕様です。実際には挿入されています"
