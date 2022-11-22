#!/bin/bash
#dest_default='database.db'
if [ $# -ne 3 ]; then
    echo "Usage: $0 <source> <destination> <image_dir>"
    exit 1
fi
if [ ! -e $2 ]; then
  echo "Destination $2 does not exist. Creating..."
  sqlite3 $2 "
  CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY,
    description TEXT,
    rare INTEGER,
    image TEXT
  );"
fi
CURRENT=$(cd $(dirname "$0") && pwd)
echo "Migrating from $1 to $2"
echo "Current directory: $CURRENT"
cat $1 | sed -r -f $CURRENT/replace.sed| nl -s '' -nln|sed 's/  */,/g' >csv
sqlite3 $2 ".mode csv" \
".import ./csv items" \
"update items set image = '${3}resources (' || id || ').png' "
