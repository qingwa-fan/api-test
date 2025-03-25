import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class SendEmail:

    # 初始化服务器信息
    def __init__(self, mail_host, mail_user, mail_pass, sender, receives):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receivers = receives

    # 以文本的形式发送邮件
    def make_email_by_text(self, context, subject, from_address, to_address):
        message = MIMEText(context, 'plain', 'UTF-8')
        message['Subject'] = subject  # 邮件标题
        message['From'] = Header(from_address, "utf-8")  # 邮件主体中发送者名称
        message['To'] = Header(to_address, "utf-8")  # 邮件主体中接收者名称
        self.send_email(message)

    # 以文本和附件的形式发送邮件
    def make_email_by_att(self, context, file_path, subject, from_address, to_address):
        message = MIMEMultipart()
        message['Subject'] = subject  # 邮件标题
        message['From'] = Header(from_address, "utf-8")  # 邮件主体中发送者名称
        message['To'] = Header(to_address, "utf-8")  # 邮件主体中接收者名称
        body = MIMEText(context, 'plain', 'utf-8')
        message.attach(body)
        att_body = open(file_path, 'rb')  # 以二进制的格式打开附件
        att = MIMEApplication(att_body.read())  # 导入附件
        att_body.close()
        att.add_header('Content-Disposition', 'attachment', filename='allure测试报告.zip')  # 添加附件名称
        message.attach(att)
        self.send_email(message)

    # 登录并进行发送
    def send_email(self, message):

        # 进行登录发送
        try:
            # smtpobj = smtplib.SMTP()
            # smtpobj.connect(self.mail_host,25)
            smtpobj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpobj.login(self.mail_user, self.mail_pass)
            smtpobj.sendmail(self.sender, self.receivers, message.as_string())
            smtpobj.quit()
            print('success')
        except Exception as e:
            print(f'error: {e}')
            raise e