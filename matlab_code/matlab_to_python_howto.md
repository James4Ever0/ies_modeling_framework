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
-----------------------------------------------------------------------------------------------
Two.pandas 的作用
pandas 主要承担下列matlab任务：

读写数据文件，一般是 excel 文件。例如：读取输入参数文件；将计算结果输出到 excel 文件。
按列名访问列数据、行数据。即使用 DataFrame 的行索引、列索引功能。
-------------------------------------------------------------------------------------------------
Three.Matlab 和 Python 的差异
1、索引操作符号：A(1)，A[0]
matlab 中访问矩阵中的元素，用圆括号做为索引操作符，像这样 A(1)，下标从1开始；而python中用方括号，像这样A[0],下表从0开始。
2.遍历循环
matlab中for i=1:L-1 与 python中for i in range(0,L)一样
3.

