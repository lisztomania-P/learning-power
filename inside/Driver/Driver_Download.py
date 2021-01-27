#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/18
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Driver_Download.py
# @Function : 驱动下载
import os
import zipfile
from urllib.parse import ParseResult
from urllib.request import urlopen

import requests
import shutil
from tqdm import tqdm

from inside.Config.Path import PATH
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DRIVER_DOWNLOAD']


class DRIVER_DOWNLOAD(metaclass=SINGLETON):
    """驱动下载类"""

    def __Download(self, link: ParseResult, dst: str) -> int:
        """
        __Download(link: ParseResult, dst: str) -> str
        驱动下载本体

        :param link: 下载链接
        :param dst: 保存路径及文件名
        :return: str
        """
        size = int(urlopen(link.geturl()).info().get('Content-Length', -1))
        bar = tqdm(
            total=size,
            initial=0,
            unit='B',
            unit_scale=True,
            desc=os.path.basename(dst),
            ncols=70
        )
        req = requests.get(url=link.geturl(), stream=True)
        with open(dst, 'ab') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
                else:
                    f.close()
        bar.close()
        return size

    def __Unzip(self, dst: str) -> bool:
        """
        __Unzip(dst: str) -> bool
        解压zip文件

        :param dst: 解压路径
        :return:
        """
        if zipfile.is_zipfile(dst):
            files = zipfile.ZipFile(dst)
            if not files.testzip():
                files.extractall(path=PATH().Driver)
                return True
            return False

    def Download(self, link: ParseResult) -> int:
        """
        Download(link: ParseResult) -> int
        驱动下载

        :param link: 驱动下载链接
        :return: int 文件大小, 默认单位B
        """
        suffix = os.path.basename(link.path)
        zip_file = os.path.join(PATH().Driver, suffix)
        shutil.rmtree(path=PATH().Driver)
        os.mkdir(PATH().Driver)
        temp = self.__Download(link=link, dst=zip_file)
        self.__Unzip(dst=zip_file)
        return temp
