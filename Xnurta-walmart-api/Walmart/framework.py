# test_AdsManagement.py
#!/usr/bin/env python3
import requests,pytest,os
from yiyan.Xnurta.Walmart.auth import get_token  # 导入 token
from xToolkit import xfile # 导入xToolkit，用来读取 excel
# 读取 execl 用例，创建 excel 的时候使用.xls后缀
test_date = xfile.read(r"/Users/liuby/PycharmProjects/pythonProject/Auto-test/Xnurta-walmart-api/Walmart/total接口测试用例.xls").excel_to_dict(sheet=0)
# print(test_date)
# print(test_date[0]["URL地址"]) # 第一行用例的URL，用下标获取
# for data in test_date: #循环列表 url 地址
#     print(data["URL地址"])
# 获取 token
token = get_token()  # 直接调用 get_token 函数

"""
@pytest.mark.parametrize 
1.被这个东西修饰的函数，会自动循环执行
2.循环的次数，由我们传入的列表长度决定
3.它会自动解析列表，每次循环时，都会把列表的元素按顺序拿出来，当做参数传递
"""
@pytest.mark.parametrize("case_info",test_date)   #参数化
def test_excute(case_info):
    headers={
    "Accept": "application/json, text/plain, */*",
    "Content-type": "application/json",
    "Accept-encoding": "gzip, deflate, br, zstd",
    "Accept-language": "zh-CN,zh;q=0.9,ru;q=0.8,nl;q=0.7,ko;q=0.6,ja;q=0.5,en;q=0.4,es;q=0.3,en-GB;q=0.2,en-US;q=0.1",
    "Authorization": token,
    "Dow": "1",
    "Profileid": "16333544",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Cache-control": "no-cache",
}
    response = requests.request(url=case_info["URL地址"],
                                method=case_info["请求方式"],
                                headers=headers,
                                json=eval(case_info["请求参数"])) #eval 格式化函数，根据你的 json 格式，自动转成对应的数据类型
    print(response.text)
    # 断言状态码
    assert response.status_code == int(case_info["预期状态码"]),f"状态码不匹配，实际状态码: {response.status_code}"
    try:
        json_response = response.json()
        assert json_response.get("message") == "success", f"响应消息不匹配，实际消息: {json_response.get('message')}"
    except ValueError:
        pytest.fail("响应不是有效的 JSON 格式")

"""
完整的自动化测试流程：测试提供数据 > 代码自动执行测试 > 生成测试报告 > 测试报告邮件发出
allure优势：可以跟 pytest 无缝衔接 -- 只要在代码证写了 allure 命令就行
allure 生成测试报告：让 pytest 生成一个 allure 的数据文件夹， --alluredir = 你想起的文件夹名字

有了数据后，生成一个好看，美观的测试报告文件
操作系统执行：allure generate [allure 数据文件夹] -o [测试报告名字] --clean
如果想让 pycharm 去执行操作系统命令(CMD，SHELL),python里面有个 OS库，直接调用操作系统的

"""


if __name__ == '__main__':
    pytest.main(["-vs",
                 "--capture=sys", # 控制台输出
                 "framework.py", # 要执行这个文件,Test_walmart
                 "--clean-alluredir", # 清除之前生成的测试报告
                 "--alluredir=allure-results" # 生成测试报告
                 ])
    os.system("allure generate allure-results -o ./allure_walmart_test --clean")# 执行操作系统命令，文件名变更