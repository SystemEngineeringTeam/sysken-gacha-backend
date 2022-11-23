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