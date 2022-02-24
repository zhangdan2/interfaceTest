import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from common import logger
import logging
def email(receivers,html_path):
    '''
    receivers : 收件人邮箱地址，多个收件人以','分隔
    html_path : 发送的测试报告路径
    '''
    #设置登录及服务器信息
    mail_host = 'smtp.163.com'
    mail_user = 'sj17671874915@163.com'
    mail_pass = 'BIKIWYANQBNUWEOB'
    sender = 'sj17671874915@163.com'

    #设置eamil信息
    #添加一个MIMEmultipart类，处理正文及附件
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = '自动化测试报告'

    #推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
    content = '''<p>请下载附件查询测试报告</p>'''
    #设置html格式参数
    part1 = MIMEText(content,'html','utf-8')
    #添加一个html附件
    with open(rf'{html_path}','r',encoding='utf-8')as h:
        content2 = h.read()
    #设置html参数
    part2 = MIMEText(content2,'plain','utf-8')
    #附件设置内容类型，方便起见，设置为二进制流
    part2['Content-Type'] = 'application/octet-stream'
    #设置附件头，添加文件名
    part2['Content-Disposition'] = 'attachment;filename="result.html"'

    #将内容附加到邮件主体中
    message.attach(part1)
    message.attach(part2)

    #登录并发送
    try:
        logging.info('准备将测试报告发送到指定邮箱')
        smtpObj = smtplib.SMTP()
        logging.info(f'开始链接SMTP服务器')
        smtpObj.connect(mail_host,25)
        logging.info(f'开始登陆邮箱')
        smtpObj.login(mail_user,mail_pass)
        logging.info(f'开始发送邮件')
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        logging.info(f'发送邮件成功，退出邮箱')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        logging.info(f'发送邮件失败，错误信息：{e}')
