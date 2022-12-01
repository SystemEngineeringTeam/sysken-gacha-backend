import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.gacha_item import GachaItem  # noqa: E501
from openapi_server.models.gacha_list import GachaList  # noqa: E501
from openapi_server import util

from dotenv import load_dotenv
import os

from openapi_server.db import get_db, close_db, DB_schema

load_dotenv()


def gacha_get() -> Tuple[GachaItem]:  # noqa: E501
    """ガチャリスト

    ガチャにて排出される全アイテムのリスト # noqa: E501


    :rtype: Union[GachaItem, Tuple[GachaItem, int], Tuple[GachaItem, int, Dict[str, str]]
    """
    db = get_db()
    cur = db.execute('select * from items')
    rows = cur.fetchall()
    items = [ {DB_schema[i]: row[i]
               for i in range(len(DB_schema))}
                    for row in rows]
        # { j[0]:j[1]
        #     for j in [DB_schema[i], row[i]
        #         if DB_schema[i] != 'image'
        # else DB_schema[i], os.path.join(os.environ['IMG_DIR'], row[i])]
        #     for i in range(len(DB_schema))
        #             } for row in rows]
    return items


def gacha_item_id_get(item_id) -> GachaList:  # noqa: E501
    """ガチャアイテム

    ガチャアイテム # noqa: E501

    :param item_id: ガチャID
    :type item_id: int

    :rtype: Union[GachaList, Tuple[GachaList, int], Tuple[GachaList, int, Dict[str, str]]
    """
    db = get_db()
    cur = db.execute('select * from items where id = ?', [item_id])
    row = cur.fetchone()
    item = {DB_schema[i]: row[i] for i in range(len(DB_schema))}
    return item


def static_pict_id_get(pict_id) :  # noqa: E501
    """画像

    指定されたIdの画像を返却します # noqa: E501

    :param pict_id: 取得したい画像の連番ID
    :type pict_id: int

    :rtype: Union[file, Tuple[file, int], Tuple[file, int, Dict[str, str]]
    """
    db = get_db()
    cur = db.execute('select image from items where id = ?', [pict_id])
    img_path = cur.fetchone()[0]
    file = open(
        os.path.join(os.environ['IMG_DIR'], img_path),
        'rb')
    return file.read()
def random_get() -> GachaItem:  # noqa: E501
    """ランダムガチャ

    ランダムガチャを引きます # noqa: E501
    :rtype: Union[GachaItem, Tuple[GachaItem, int], Tuple[GachaItem, int, Dict[str, str]]
    """
    db = get_db()
    cur = db.execute('select * from items order by random() limit 1')
    row = cur.fetchone()
    item = {DB_schema[i]: row[i]
               for i in range(len(DB_schema))}
    return item
def admin_item_put(id, name, rare, image) -> GachaItem:  # noqa: E501
    """アイテム追加

    アイテム追加 # noqa: E501

    :param name: アイテム名
    :type id: int
    :type name: str
    :type rare: int
    :type image: str

    :rtype: Union[GachaItem, Tuple[GachaItem, int], Tuple[GachaItem, int, Dict[str, str]]:
    """
    db = get_db()
    cur = db.execute('update items set description = ?, rare = ?, image = ? where id = ?',
                     [name, rare, image, id])
    db.commit()
    cur_get = db.execute('select * from items where id = ?', [id])
    row = cur_get.fetchone()
    item: GachaItem = {DB_schema[i]: row[i] for i in range(len(DB_schema))}
    return item


def admin_item_post(name, rare, image) -> dict:  # noqa: E501
    db = get_db()
    max_id: int = db.execute('select max(id) from items').fetchone()[0]
    cur = db.execute('insert into items (id, description, rare, image) values (?,?,?,?)',
                     [max_id + 1, name, rare, image])
    db.commit()
    getcur = db.execute('select * from items where id = ?', [max_id + 1])
    row = getcur.fetchone()
    item = {DB_schema[i]: row[i] for i in range(len(DB_schema))}
    return item


def admin_upload_post(file) -> Union[dict,str]:  # noqa: E501
    """画像アップロード

    画像アップロード # noqa: E501

    :param file: 画像ファイル
    :type file: werkzeug.datastructures.FileStorage
    """
    if file.filename == '':
        return 'No selected file'
    elif file:
        filename = file.filename
        file.save(os.path.join(os.environ['IMG_DIR'], filename))
        return {'status': 'success'}
