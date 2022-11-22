from flask import Flask, render_template, request, redirect, url_for, jsonify, g
# from sqlite3 import dbapi2 as sqlite3
import sqlite3
import json
from openapi_server.util import _deserialize_object

db_filename = 'database.db'
# db = sqlite3.connect(db_filename)
app = Flask(__name__, static_url_path='/static')

scheme = ["id", "desc", "rare", "img"]


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(db_filename)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    return 'Hello World'


@app.route('/items/')
def show_items():
    db = get_db()
    cur = db.execute('select * from items')
    rows = cur.fetchall()
    items = [{
        scheme[i]: row[i]
        for i in range(len(scheme))
    } for row in rows]
    # return jsonify(obj)
    return json.dumps(items)


@app.route('/items/<int:item_id>')
def show_item(item_id):
    db = get_db()
    cur = db.execute('select * from items where id = ?', [item_id])
    row = cur.fetchone()
    item = {
        "id": row[0],
        "desc": row[1],
        "rare": row[2],
        "image": row[3]
    }
    return jsonify(item)


@app.route('/items', methods=['POST'])
def add_item():
    db = get_db()
    db.execute('insert into items (desc,rare,image) values (?,?,?)', \
               [request.form['name'], request.form['rare'], request.form['image']])
    db.commit()
    return redirect(url_for('show_items'))


@app.route('/items/image/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    db.execute('update items set name = ? where id = ?', [request.form['image'], item_id])
    db.commit()
    return redirect(url_for('show_items'))


@app.route('/items/random')
def random_item():
    db = get_db()
    cur = db.execute('select * from items order by random() limit 1')
    row = cur.fetchone()
    item = {scheme[i]: row[i] for i in range(len(scheme))}
    return jsonify(item=item)


if __name__ == '__main__':
    app.run()
