from common import dir_config
import requests
from common import logger
import time
import datetime
import logging

class BasePage:
    def post(self,url,data=None,headers=None):
        logging.info(f'开始请求接口：{url}')
        logging.info(f'请求头：{headers}')
        logging.info(f'请求参数：{data}')
        try:
            start = datetime.datetime.now()
            logging.info(f'请求开始时间{start}')
            r = requests.post(url=url,data=data,headers=headers)
            end = datetime.datetime.now()
            logging.info(f'请求结束时间{end}')
            logging.info(f'请求时长为{end - start}')
            if r.status_code != 500 or r.status_code != 404:
                logging.info(f'请求成功,响应内容:{r.text}')
            else:
                logging.info(f'请求失败，响应状态码：{r.status_code}')
            return r
        except:
            logging.exception(f'请求失败')
            raise

    def get(self,url,data=None,headers=None):
        logging.info(f'开始请求接口：{url}')
        logging.info(f'请求头：{headers}')
        logging.info(f'请求参数：{data}')
        try:
            start = datetime.datetime.now()
            logging.info(f'请求开始时间{start}')
            r = requests.get(url=url,params=data,headers=headers)
            end = datetime.datetime.now()
            logging.info(f'请求结束时间{end}')
            logging.info(f'请求时长为{end-start}')
            if r.status_code !=500 or r.status_code != 404:
                logging.info(f'请求成功，响应内容：{r.text}')
            else:
                logging.info(f'请求失败，响应状态码：{r.status_code}')
            return r
        except:
            logging.exception(f'请求失败')
            raise
    



