### 初始环境搭建
> 运行环境建议要求python3.6.0以上。

> 浏览器及浏览器对应版本的driver安装。
驱动：https://googlechromelabs.github.io/chrome-for-testing/
> Allure运行环境安装。

###Ps:环境搭建可参考以下地址:[windows scoop allure 安装](http://note.youdao.com/s/9ELlaBD5)

## 目前使用python3+pytest+selenium作为基础，二次封装常用API，简化代码，采用allure产生报告。

### 依赖包安装
第一次运行此项目时，可一键安排所有依赖包：pip install -r requirements.txt

###python一键执行文件使用相关
目前一键执行文件只使用于python变量。即在命令行下输入python 可进入python3的运行器。若本地环境同时安装python2和python3,环境变量使用python2和3区分，可修改一键执行文件中的python为python3.

## 目录结构

初始的目录结构如下：

~~~
AMC_Xnurta
|─Common                  公共方法
│  ├─readconfig.py        读取配置文件 类：ReadConfig.实例化对象：ini。获取config.ini文件中的值
│  └─readelement.py       读取元素 类：Element.获取读取yaml文件文件中的值
├─config                  配置文件.设置项目、报告等文件目录和元素定位类型、邮件信息、收件人等 
│  ├─config.py            类：ConfigManager.实例化对象:cm
│  └─config.ini           存放系统信息
├─logs                    运行日志信息
├─page                    
│  └─webpage.py           selenium基类 类：WebPage.页面元素定位等  鼠标滑动  页面操作等方法
├─page_element            
│  └─element.yaml         存放页面元素
├─page_object              
│  └─element.py           封装的页面方法类
├─screenshot              报错用例截图
├─TestCase                测试用例
├─utils                   测试工具：日志、时间
├─conftest.py            
├─pytest.ini           
├─README.md               README 文件
├─report.html             测试报告
├─requirements.txt        项目依赖包清单
├─runcase.py              linux服务器批量执行case统一执行入口
├─run.py                  本地批量执行case统一执行入口

