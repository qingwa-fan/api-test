# auth.py
import requests

# 登录接口 URL
url = "https://api-test.xnurta.com/api/auths/login"

# 登录接口请求头
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-type": "application/json; charset=UTF-8"
}

# 登录接口请求参数
params = {
    "lang": "zh",
    "username": "test001@marketin.cn",
    "password": "QTEyMzQ1Ng=="
}

def logining(url, method, headers, json):
    """封装登录接口"""
    try:
        response = requests.request(url=url, method=method, headers=headers, json=json)
        print(f"登录接口返回状态码: {response.status_code}")
        print(f"登录接口返回结果: {response.text}")
        return response
    except Exception as e:
        print(f"登录请求异常: {e}")  # 增强异常信息输出
        return None
def get_token():
    """获取 token"""
    login_response = logining(url=url, method="post", headers=headers, json=params)

    if not login_response:
        print("登录请求失败，请检查网络或接口配置")
        return None

    if login_response.status_code == 200:
        try:
            token = "Bearer " + login_response.json()["data"]["jwt"]
            print("Token 获取成功")
            return token
        except KeyError:
            print("登录失败：返回数据中缺少 jwt 字段")
            return None
    else:
        print(f"登录失败：HTTP 状态码 {login_response.status_code}")
        return None
# 打印登陆结果和token
token = get_token()
print(token)