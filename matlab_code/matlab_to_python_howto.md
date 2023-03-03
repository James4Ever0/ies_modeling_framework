One.a tool called as "matlab2python"
1、安装：
>>git clone https://github.com/ebranlard/matlab2python
>>cd matlab2python
>>pip install -r requirements.txt

如果有朋友不能翻墙clone不下来代码，把上面第一行命令换成：
>>git clone https://gitee.com/zongfang/matlab2python.git

2、使用：
在matlab2python目录下输入
>>python matlab2python.py file.m -o file.py

注意：file.m如果不指定位置就是当前目录下的，如果要用别的目录下的文件，需要指定路径。
