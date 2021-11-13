# 1. 安装python环境3.8.9
1. 需要已经安装python3.6，并且环境变量中可以访问
	下载地址：https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe
   
2. 修改python访问数据源（可选，加快数据下载）
	a). 在用户目录(c:/Users/xxxx)下新建 pip/pip.ini 文件夹和文件
	文件内容如下：
>
> [global]
> index-url = https://pypi.tuna.tsinghua.edu.cn/simple
> 
> [install]
> trusted-host = mirrors.aliyun.com
> 
> [list]
> format = columns

3. 安装虚拟环境管理工具（命令行中执行，可以不是项目根目录） 
> pip install virtualenv

4. 管理员身份运行命令行工具，并切换到当前项目路径  
> cd xxxxx

5. 生成python3.6虚拟环境（相对项目根目录）  
> virtualenv venv

6. 激活虚拟环境（相对项目根目录）  
> venv\Scripts\activate.bat

7. 安装项目依赖（相对项目根目录，命令行前面：(venv)）
> pip install data/lib/pymssql-2.1.4-cp38-cp38-win_amd64.whl <br>
> pip install -r requirements.txt <br>
> pip freeze > requirements.txt <br>
> 扩展包地址：https://www.lfd.uci.edu/~gohlke/pythonlibs/
> 对于scikit-learn  如果安装不成功的话，可以从已有机器上复制过去

8. 运行项目
python main.py

### 问题：
1. No Module named Cython
> pip install Cython
2. Microsoft Visual C++ 14.0 or greater is required.
> 安装 data/lib/visualcppbuildtools.rar


# 验证码相关
## 1. 使用tesseract 识别图片验证码
下载地址

[https://digi.bib.uni-mannheim.de/tesseract/](https://digi.bib.uni-mannheim.de/tesseract/) 

[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

> github 下载地址：[https://github.com/UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract) 

1. 添加环境变量  
**注意：需要添加中文支持**  
将C:\Program Files\Tesseract-OCR 添加到环境变量中即可   
运行 tesseract -v 查看版本

2. python代码运行   
pip install pytesseract

3. 导出项目依赖
pip freeze > requirements.txt
安装：
pip install -r requirements.txt

# Linux 下运行说明
1. 虚拟化境激活
source venv/bin/activate

2. 退出虚拟环境
deactivate
   
# 项目说明
本项目主要是自动化下单执行客户端程序，用于执行服务端下发的指令信息。指令主要包括买入、卖出、持仓、成交、委托、资金、撤销委托等信息查询与操作。
本系统也可以当时使用不依赖于服务端完成自动化下单操作。

以下分两部分说明
### 1. 执行后端指令
1. 项目下载之后需要首先修改配置信息（config.ini）文件
其中每个配置项都做了说明，请确保client_id的值唯一，及不同客户端请使用不同的值，最好与数据库对应起来
2.  执行main.py 方法执行下单客户端程序。
3. 启动之后程序会自动连接配置文件中配置的websocket连接。
4. 连接成功之后会自动监听websocket中的指令。
5. socket的相关操作放在了/src/stock/socket 包下面
6. 客户端收到了服务端发来的指令时，会调用socket_message_handler中的方法去执行指令；
7. 真正执行指令的类时client_* 类；
8. 之后执行指令参考本地执行指令方法

### 2. 本地执行指令
1. 本地开发或者测试客户端程序请直接执行client_test 程序；