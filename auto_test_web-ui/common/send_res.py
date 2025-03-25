import requests

class SendReportMessage:

    def send_dingtalk_message(self,data):
        #url = "https://oapi.dingtalk.com/robot/send?access_token=bcc76d081ad023f7aa7f78e7cb77b79dfc3616625bb40de4c8b57123c4faadd4"
        url = "https://oapi.dingtalk.com/robot/send?access_token=1c2023418fa8407c91e61c76af5828d21e8e894ce675ea9513865fdb3de03211"
        params = {"text": {"content":data},"msgtype":"text"}
        res = requests.post(url=url, json=params)
        print(res)

    def send_qiwei_message(self, data):
        pass
