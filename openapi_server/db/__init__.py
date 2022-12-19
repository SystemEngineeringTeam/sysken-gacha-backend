from flask import g
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.environ['DB_PATH']


def get_db():
    if ('db' not in g):
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    print(os.getcwd())
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

print(os.getcwd())
DB_schema = ["id", "desc", "rare", "image"]


def setup_db():
    DB_PATH = os.environ['DB_PATH']
    db = sqlite3.connect(DB_PATH)
    cur = db.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL 
    );''')

