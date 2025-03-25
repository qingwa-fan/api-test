import requests

class HandleRequest:

    def send(self, url, method, params=None, json=None, data=None, headers=None):
        # 将请求转换为小写
        method = method.lower()
        if method == "post":
            return requests.post(url=url, json=json, data=None, headers=headers)
        # elif method == "patch":
        #     return requests.patch(url=url, json=json, data=None, headers=headers)
        elif method == "get":
            return requests.get(url=url, params=params)

#
# class HandleSessionRequest:
#     """使用session鉴权的接口，使用这个类发送请求"""
#
#     def __init__(self):
#         self.session = requests.session()
#
#     def send(self, url, method, params=None, json=None, data=None, headers=None):
#         # 将请求转换为小写
#         method = method.lower()
#         if method == "post":
#             return self.session.post(url=url, json=json, data=None, headers=headers)
#         elif method == "patch":
#             return self.session.patch(url=url, json=json, data=None, headers=headers)
#         elif method == "get":
#             return self.session.get(url=url, params=params)
