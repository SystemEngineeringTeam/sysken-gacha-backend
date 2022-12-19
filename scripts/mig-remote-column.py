import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.environ['DB_PATH']
db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row
cur = db.execute('ALTER TABLE items ADD COLUMN source string DEFAULT "local"')
db.commit()