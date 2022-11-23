# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.gacha_item import GachaItem  # noqa: E501
from openapi_server.models.gacha_list import GachaList  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_gacha_get(self):
        """Test case for gacha_get

        ガチャリスト
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/gacha',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_gacha_item_id_get(self):
        """Test case for gacha_item_id_get

        ガチャアイテム
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/gacha/{item_id}'.format(item_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    # def test_static_pict_id_get(self):
    #     """Test case for static_pict_id_get
    #
    #     画像
    #     """
    #     file = open('../../img/resource (56).jpg','rb'),
    #     headers = {
    #         'Accept': 'image/jpeg',
    #     }
    #     response = self.client.open(
    #         '/static/{pict_id}'.format(pict_id=56),
    #         method='GET',
    #         headers=headers)
    #     self.assert200(response,
    #                    'Response body is : ' + response)


if __name__ == '__main__':
    unittest.main()
