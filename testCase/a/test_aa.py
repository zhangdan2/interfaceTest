from common.basepage import BasePage
from common.get_token import token
import unittest
from common import logger
import logging
import json
class get_shop(unittest.TestCase):
    def setUp(self) -> None:
        self.a = BasePage()
        self.url = 'https://test-go-3-api.heyteago.com/api/service-sale/admin/shop/shop-cities'
        self.headers = {'accept': 'application/json','authorization':token()}

    def tearDown(self) -> None:
        pass

    def test_获取门店列表2(self):
        r = self.a.get(url=self.url,headers=self.headers)
        print(r.text)
        logging.info(f'断言：{json.loads(r.text)["code"]} 等于 0 ')
        self.assertEqual(0,json.loads(r.text)['code'])
