import json
import time
import unittest
from common.HTMLTestRunner_PY3 import HTMLTestRunner
from common import dir_config
from lxml import etree
from bs4 import BeautifulSoup
import re
import requests
from common import logger
import logging
from common.basepage import BasePage
from common import get_email
from apscheduler.schedulers.blocking import BlockingScheduler
request = BasePage()
class runAll:
    # 封装一个读取txt文件里的测试用例的方法
    def yongli(self):
        list = []
        # 读取一个txt文件
        with open('caselist.txt', 'r',encoding='utf-8') as f:
            for i in f.readlines():
                data = str(i)
                # 判断文件名，带有‘#’号的文件名不读取
                if data != '' and not data.startswith('#'):
                    list.append(data.replace('\n',''))

        # 将读取到的文件名放入需要执行的测试用例
        test_suite = unittest.TestSuite()
        data1 = []
        for ii in list:
            name = ii.split('/')[-1]
            print(name+'.py')
            # 加载所有的用例
            discover = unittest.defaultTestLoader.discover(start_dir=f'./testCase',pattern = name+'.py',top_level_dir=None)
            data1.append(discover)

        # 判断读取到的用例大于0时执行用例
        if len(data1) >0:
            for suite in data1:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    # 执行测试用例，保存为测试报告
    def run(self):
        # 测试报告名称中加上格式化时间\
        now = time.strftime('%Y-%m-%d %H_%M_%S')
         # 测试报告路径
        self.report_path = dir_config.baogao_dir + '\\'+ now + 'Result.html'
        #加载测试用例
        discover = self.yongli()
        with open(self.report_path,'wb') as f:
            runner=HTMLTestRunner(stream=f,verbosity=2,title='自动化测试报告',description='用例执行详细信息')
            runner.run(discover)

        #爬取测试报告，提取需要的数据
        try:
            logging.info(f'开始爬取测试报告内的数据')

            #使用bs4解析测试报告文档
            soup = BeautifulSoup(open(rf'{self.report_path}',encoding='utf-8'))

            #提取测试报告里用例状态的数据
            a = str(soup.find_all('p',class_='attribute')[2])
            aa = a.split('</p')
            self.zhuangtai = aa[0].split('g>')[-1]

            #计算用例总数
            a2 = re.findall(r'\d', self.zhuangtai)
            if len(a2) == 1:
                self.a3 = int(a2[0])
            else:
                self.a3 = int(a2[0]) + int(a2[1])
            logging.info(f'用例总数：{self.a3}')
            logging.info(f'用例状态：{self.zhuangtai}')

            #提取测试报告里失败的测试用例
            b = soup.find_all('td', class_="failCase")
            self.shibai = re.findall(r'testcase">test_(.*?)</div>', str(b))
            logging.info(f'失败用例：{self.shibai}')

            # 若有失败的用例时，将爬取到的测试报告数据发送到钉钉消息群
            logging.info(f'开始发送测试信息到钉钉群')
            if self.shibai == []:
                logging.info(f'无失败用例')
                # 无失败的用例时，将测试报告内的数据发送到钉钉群
                url = 'https://oapi.dingtalk.com/robot/send?access_token=d676f3f2f0fedd043dcde9ee128ad1cc68f7dcc98edd379398d193730c684e23'
                headers = {"Content-Type": "application/json"}
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "自动化测试报告",
                        "text": "#### 自动化测试报告: \n "
                                f"> 用例总数：{self.a3}，状态：{self.zhuangtai}\n "
                                f">##### 请到邮箱查看详细测试报告"

                    },
                    "at": {
                        "isAtAll": False
                    }
                }
                request.post(url=url, data=json.dumps(data), headers=headers)

            else:
                string = ''
                for i in self.shibai:
                    string += f'>- {i}\n'
                url = 'https://oapi.dingtalk.com/robot/send?access_token=d676f3f2f0fedd043dcde9ee128ad1cc68f7dcc98edd379398d193730c684e23'
                headers = {"Content-Type": "application/json"}
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "自动化测试报告",
                        "text": "#### 自动化测试报告: \n "
                                f"> 用例总数：{self.a3}，状态：{self.zhuangtai}\n "
                                f"#### 失败用例:\n"
                                f"{string} "
                                f">##### 请到邮箱查看详细测试报告"

                    },
                    "at": {
                        "isAtAll": False
                    }
                }
                request.post(url=url, data=json.dumps(data), headers=headers)
        except:
            logging.info(f'爬取测试报告失败')

        #将测试报告发送到指定邮箱
        get_email.email(['1286417555@qq.com'],rf'{self.report_path}')

if __name__ == '__main__':

    from apscheduler.schedulers.background import BackgroundScheduler
    import requests
    sched = BlockingScheduler()
    # 每隔5s执行一次my_job函数，输出当前时间信息
    # sched.add_job(my_job, 'interval', seconds=5)
    # 时间： 每天定时执行自动化测试
    sched.add_job(runAll().run(), 'cron',hour=17,minute=29)
    sched.start()
    # url = 'https://github.com/kenwoodjw/python_interview_question'
    # api = 'https://api.github.com/repos/zhangdan2/zhangdan2'
    # last_update = None
    # while True:
    #     r = requests.get(url=api)
    #     cur_update = r.json()['updated_at']
    #     print(cur_update)
    #
    #     if last_update == None:
    #         last_update = cur_update
    #
    #     if last_update < cur_update:
    #         print(f'git有更新，更新时间：{cur_update}')
    #         last_update = cur_update
    #
    #     time.sleep(5000)