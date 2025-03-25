import os

import yaml

from common.zip_file import zip_files
from common.send_email import SendEmail
from common.log import Logger

logging = Logger(__name__).get_logger()
def run_case():
    file_name = r'./config.yaml'
    with open(file_name, "r", encoding="UTF-8") as f:
        config = yaml.safe_load(f)
    allure_conf = config["test_allure"]
    # 执行pytest ./test_case/ -s -q --alluredir=./result/
    allure_test = allure_conf["run_test_allure"]
    os.system(allure_test)  # 通过os.system()执行命令行的命令
    # 执行allure allure generate ./result/ -o ./report/ --clean
    report_test = allure_conf["make_allure_report"]
    os.system(report_test)
    # 把报告文件夹进行压缩
    dir_path = r'./report'
    zip_path = r'./report_zip/report.zip'
    zip_report = zip_files(dir_path, zip_path)
    if zip_report:

        file_path = zip_path
        content = "测试执行结束，Allure测试报告在邮件附件中，请使用Pycharm打开查看。"
        Subject = 'webUI自动化测试报告'  # 邮件标题
        From = "Jie的QQ邮箱"  # 邮件主体中发送者名称
        To = "Jie的163邮箱"  # 邮件主体中接收者名称
        try:
            config_email = config["Email"]
            send = SendEmail(mail_host=config_email['mail_host'], mail_user=config_email['mail_user'],
                             mail_pass=config_email['mail_pass'],
                             sender=config_email['sender'], receives=config_email['receives'])
            send.make_email_by_att(content, file_path, Subject, From, To)
            logging.info(f"邮件发送成功，邮件标题：{Subject}")
        except Exception as e:
            logging.error(f"读取配置文件::{file_name}::失败::{e}")
            raise e

if __name__ == '__main__':
    run_case()


