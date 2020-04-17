import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import configparser
import os

abs_path = '/home/xxm/project/monitor/'
cfg = configparser.ConfigParser()
cfg.read(os.path.join(abs_path,'email.ini'), encoding='utf-8')

cfg_dic = dict(cfg.items('email'))


class SendEMail(object):
    """封装发送邮件类"""

    def __init__(self):
        # 第一步：连接到smtp服务器
        self.smtp_s = smtplib.SMTP_SSL(host=cfg_dic['host'],
                                       port=cfg_dic['port'])
        # 第二步：登陆smtp服务器
        self.smtp_s.login(user=cfg_dic['user'],
                          password=cfg_dic['pwd'])

    def send_text(self,  content, to_user=cfg_dic['to_user'], subject=cfg_dic['subject']):
        """
        发送文本邮件
        :param to_user: 对方邮箱
        :param content: 邮件正文
        :param subject: 邮件主题
        :return:
        """
        # 第三步：准备邮件
        # 使用email构造邮件
        msg = MIMEText(content, _subtype='plain', _charset="utf8")
        # 添加发件人
        msg["From"] = cfg_dic['user']
        # 添加收件人
        msg["To"] = to_user
        # 添加邮件主题
        msg["subject"] = subject
        # 第四步：发送邮件
        self.smtp_s.send_message(msg, from_addr=cfg_dic['user'], to_addrs=to_user)
        return 1

    def send_file(self, to_user, content, subject, reports_path, file_name):
        """
        发送测试报告邮件
        :param to_user: 对方邮箱
        :param content: 邮件正文
        :param subject: 邮件主题
        :param reports_path: 测试报告路径
        :param file_name: 发送时测试报告名称
        """
        # 读取报告文件中的内容
        file_content = open(reports_path, "rb").read()
        # 2.使用email构造邮件
        # （1）构造一封多组件的邮件
        msg = MIMEMultipart()
        # (2)往多组件邮件中加入文本内容
        text_msg = MIMEText(content, _subtype='plain', _charset="utf8")
        msg.attach(text_msg)
        # (3)往多组件邮件中加入文件附件
        file_msg = MIMEApplication(file_content)
        file_msg.add_header('content-disposition', 'attachment', filename=file_name)
        msg.attach(file_msg)
        # 添加发件人
        msg["From"] = [cfg_dic['user']]
        # 添加收件人
        msg["To"] = to_user
        # 添加邮件主题
        msg["subject"] = subject
        # 第四步：发送邮件
        self.smtp_s.send_message(msg, from_addr=[cfg_dic['user']], to_addrs=to_user)


if __name__ == '__main__':
    s = SendEMail()
    s.send_text('test email')
