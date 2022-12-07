import connexion
import os
from typing import List

from openapi_server.models.gacha_item import GachaItem  # noqa: E501
# from openapi_server.models.gacha_list import GachaList  # noqa: E501
# from openapi_server import util

from openapi_server.db import get_db, close_db, DB_schema
from dotenv import load_dotenv
from typing import Union

load_dotenv()


def admin_item_put(id, name, rare, image) -> GachaItem:  # noqa: E501
    """アイテム更新

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


def admin_item_post(name, rare, **rest) -> dict:  # noqa: E501
    """アイテム追加

    アイテム追加 # noqa: E501

    :param name: アイテム名
    :type name: str
    :param rare: レア度
    :type rare: int
    :param rest: 非要求引数(0:画像パス)
    """
    db = get_db()
    max_id: int = db.execute('select max(id) from items').fetchone()[0]
    print(rest)
    if not rest or not rest['image']:

        print('not rest:' + 'true' if (not rest) else 'false'
                          + '\nnot rest[0]:' + 'true' if (not rest['image']) else 'false')
        cur = db.execute('insert into items (id, description, rare) values (?,?,?)',
                         [max_id + 1, name, rare])
    else:
        source = 'url' if rest['image'][:8] == 'https://' \
            or rest['image'][:7] == 'http://' else 'local'
        cur = db.execute('insert into items (id, description, rare, image, source) values (?,?,?,?,?)',
                         [max_id + 1, name, rare, rest['image'], source])
    db.commit()
    getcur = db.execute('select * from items where id = ?', [max_id + 1])
    row = getcur.fetchone()
    item = {DB_schema[i]: row[i] for i in range(len(DB_schema))}
    return item


def admin_upload_post(file) -> Union[dict, str]:  # noqa: E501
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
