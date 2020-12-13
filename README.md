# 项目简介

<img src="https://www.python.org/static/img/python-logo@2x.png" width=150px hegiht=150px align=center title="Python 3.8.2" href="https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe">  <img src="https://www.xuexi.cn/favicon.ico" width=50px hegiht=50px align=center title="学习强国" href="https://www.xuexi.cn/">

> 学习强国自动化脚本，解放你的时间！
>
> 使用Selenium、requests开发而成



# 使用说明

> **注**：Chrome版本
>
> ![image-20201207091125954](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201207091125954.png)
>
> **如想更换版本**，只需要替换driver目录中的驱动删除，然后运行main.py，输入Chrome版本，程序会自动下载对应版本的驱动。
>
> **当然也可手动**
>
> 驱动下载链接：http://chromedriver.storage.googleapis.com/index.html
>
> 首次使用会生成数据库文件task.db，用于提高文章、视频任务效率。



## 依赖安装

> pip install -r requirements.txt
>
> 没有梯子的同学可使用国内阿里源：
>
> pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple



## 使用方法

> **一定要找个网络好的地方，不然可能会出现错误**
>
> 1、控制台运行：python main.py
>
> 2、选择选项（如非必要，尽量选择不显示自动化过程，以免误操）
>
> 等待片刻，连接学习强国服务器需要时间，等待时间与网速关系很大。
>
> 3、扫描二维码登录
>
> 4、选择任务(暂时只支持文章、视频、每日答题、每周答题、专项答题，后续功能正在开发，不过暂时也差不多够用了，45分呢)，可多选，不过每个选项要用空格隔开，选择文章或视频时，等待时间稍久一点。
>
> 5、任务完成后需手动结束程序



## 使用示例

### 缺少驱动情况

> **注**：下载驱动的速度与自身访问驱动下载站点的速度有关，下载有时候快有时候慢，有梯子的建议挂梯子。后续将尝试开发多线程下载。
>
> ![image-20201209114329468](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209114329468.png)
>
> ![image-20201213193556195](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201213193556195.png)
>
> ![image-20201213193853014](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201213193853014.png)
>
> ![image-20201213193926939](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201213193926939.png)
>
> ![image-20201213193948562](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201213193948562.png)

### 正常情况

> ![image-20201213193245188](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201213193245188.png)
>
> ![image-20201213193309585](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201213193309585.png)
>
> ![image-20201209114457238](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209114457238.png)
>
> ![image-20201209114712975](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209114712975.png)
>
> ![image-20201209115305018](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209115305018.png)
>
> ![image-20201209121854379](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209121854379.png)
>
> ![image-20201209121940399](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209121940399.png)
>
> ![image-20201209123111315](https://gitee.com/lisztomania/Figure-bed/raw/master/img/image-20201209123111315.png)



## 版本说明

> - [ ] ~~v0.1：文章、视频，分数：25~~
>- [ ] ~~v0.2：优化文章、优化视频、每日答题（百分百正确），分数30~~
> - [ ] ~~v0.3：新增每周答题、专项答题（也是百分百正确），分数45~~
> - [x] v0.31：优化记录存储、优化目录结构、优化配置文件结构，增加进度条、增加自动下载驱动、增加系统兼容（Linux、Windows、MacOS）



## 附语

> 既然看到这了，希望大佬点点start，给点动力，希望能给大家带来更多的功能！

