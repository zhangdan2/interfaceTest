from common.basepage import BasePage
import json
from common import logger
import logging
a = BasePage()
def token():
    url = 'https://test-go-3-api.heyteago.com/api/service-upms/admin/user/login'
    data = {"username": "admin@heytea.com", "password": "Aa1234%^&*"}
    logging.info('开始请求登陆接口，获取token')
    try:
        headers = {'content-type': 'application/json;charset=UTF-8'}
        r = a.post(url=url, data=json.dumps(data), headers=headers)
        logging.info(f'获取token成功')
        return 'Bearer '+ json.loads(r.text)['data']['token']
    except:
        logging.exception('获取token失败')
