#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/17
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Driver_Analysis.py
# @Function : 驱动解析
import requests
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup, ResultSet

from inside.Config.System import SYSTEM
from inside.Template.ABC_Driver_Analysis import DRIVER_ANALYSIS
__all__ = ['GOOGLEAPIS_DRIVER_ANALYSIS', 'TAOBAO_DRIVER_ANALYSIS']


class GOOGLEAPIS_DRIVER_ANALYSIS(DRIVER_ANALYSIS):
    """驱动官网下载类"""

    @property
    def Master(self) -> ParseResult:
        """
        Master -> ParseResult
        官网

        :return: ParseResult
        """
        return urlparse(
            url="http://chromedriver.storage.googleapis.com/index.html"
        )

    def __Master(self) -> ParseResult:
        """
        __Master() -> ParseResult
        官网xml列表

        :return: ParseResult
        """
        return urlparse(
            url="http://chromedriver.storage.googleapis.com/?delimiter"
                "=/&prefix="
        )

    def __Definite(self) -> ParseResult:
        """
        __Definite() -> ParseResult
        具体版本xml列表

        :return: ParseResult
        """
        return urlparse(
            url="http://chromedriver.storage.googleapis.com/?delimiter=/&prefix={version}/"
        )

    def __Download_Link(self) -> ParseResult:
        """
        __Download_Link() -> ParseResult
        驱动下载链接

        :return: ParseResult
        """
        return urlparse(
            url="http://chromedriver.storage.googleapis.com/{path}"
        )

    def __All_Driver(self) -> ResultSet:
        """
        __All_Driver() -> ResultSet
        所有版本xml列表

        :return: ResultSet
        """
        html = requests.get(url=self.__Master().geturl())
        for retry in range(3):
            if html.status_code == 200:
                break
            html = requests.get(url=self.__Master().geturl())
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, 'lxml')
        return soup.select(selector='CommonPrefixes')

    def __Filtrate_Version(self, chrome_version: str) -> str:
        """
        __Filtrate_Version(chrome_version: str) -> str
        匹配驱动版本

        :param chrome_version: 谷歌浏览器版本号
        :return: str
        """
        res = []
        chrome_version = chrome_version.split('.')[:-1]
        for commonprefixes in self.__All_Driver():
            temp = commonprefixes.text
            if temp.split('.')[:-1] == chrome_version:
                res.append(temp.strip('/'))
        return max(res, key=lambda x: int(x.split('.')[-1]))

    def __Select_Driver(self, driver_version: str) -> ResultSet:
        """
        __Select_Driver(driver_version: str) -> ResultSet
        获取具体版本驱动xml列表

        :param driver_version: 驱动版本号
        :return: ResultSet
        """
        html = requests.get(
            url=self.__Definite().geturl().format(version=driver_version)
        )
        for retry in range(3):
            if html.status_code == 200:
                break
            html = requests.get(
                url=self.__Definite().geturl().format(version=driver_version)
            )
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, 'lxml')
        return soup.select(selector='Contents')

    def __Filtrate_Driver(self, system: SYSTEM, soups: ResultSet) -> str:
        """
        __Filtrate_Driver(system: SYSTEM, soups: ResultSet) -> str
        获取与系统匹配的驱动

        :param system: 系统类
        :param soups: 驱动xml列表
        :return: str
        """
        res = []
        Os = self._map.get(system.Name)
        for contents in soups:
            temp = contents.key.text
            if Os in temp:
                res.append(temp)
        if len(res) == 1:
            return res[0]
        else:
            t = [x for x in res if str(system.Bit) in x]
            if len(t) == 1:
                return t[0]
            return min(res, key=len)

    def Download(self, system: SYSTEM) -> ParseResult:
        """
        Download(system: SYSTEM) -> ParseResult
        获取驱动下载链接

        :param system: 系统类
        :return: ParseResult
        """
        driver_version = self.__Filtrate_Version(
            chrome_version=system.Chrome_Version)
        soups = self.__Select_Driver(driver_version=driver_version)
        path = self.__Filtrate_Driver(system=system, soups=soups)
        return urlparse(
            url=self.__Download_Link().geturl().format(path=path)
        )


class TAOBAO_DRIVER_ANALYSIS(DRIVER_ANALYSIS):
    """淘宝镜像类"""

    @property
    def Master(self) -> ParseResult:
        """
        Master -> ParseResult
        官网

        :return: ParseResult
        """
        return urlparse(
            url="http://npm.taobao.org/mirrors/chromedriver/"
        )

    def __Defininite(self) -> ParseResult:
        """
        __Definite() -> ParseResult
        具体版本列表

        :return: ParseResult
        """
        return urlparse(
            url="http://npm.taobao.org{path}"
        )

    def __Download_link(self) -> ParseResult:
        """
        __Download_link() -> ParseResult
        驱动下载链接

        :return: ParseResult
        """
        return urlparse(
            url="https://cdn.npm.taobao.org/dist{path}"
        )

    def __All_Driver(self) -> ResultSet:
        """
        __All_Driver() -> ResultSet
        所有驱动列表

        :return: ResultSet
        """
        html = requests.get(url=self.Master.geturl())
        for retry in range(3):
            if html.status_code == 200:
                break
            html = requests.get(url=self.Master.geturl())
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup.pre.select(selector='a')

    def __Filtrate_Version(self, chrome_version: str) -> str:
        """
        __Filtrate_Version(chrome_version: str) -> str
        获取与谷歌浏览器版本匹配的驱动版本

        :param chrome_version: 谷歌浏览器版本号
        :return: str
        """
        res = []
        chrome_version = chrome_version.split('.')[:-1]
        for a in self.__All_Driver():
            temp = a.text.split('.')[:-1]
            if temp == chrome_version:
                res.append(a)
        return max(res, key=lambda x: int(x.text.split('.')[-1].strip('/'))).attrs.get('href')

    def __Select_Driver(self, drivers_link: ParseResult) -> ResultSet:
        """
        __Select_Driver(drivers_link: ParseResult) -> ResultSet
        具体版本号驱动列表

        :param drivers_link: 具体版本号驱动链接
        :return: ResultSet
        """
        html = requests.get(url=drivers_link.geturl())
        for retry in range(3):
            if html.status_code == 200:
                break
            html = requests.get(url=drivers_link.geturl())
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup.pre.select(selector='a')

    def __Filtrate_Driver(self, system: SYSTEM, soups: ResultSet) -> str:
        """
        __Filtrate_Driver(system: SYSTEM, soups: ResultSet) -> str
        获取与系统匹配的驱动

        :param system: 系统类
        :param soups: 具体版本号驱动列表
        :return: str
        """
        res = []
        Os = self._map.get(system.Name)
        for a in soups:
            if Os in a.text:
                res.append(a)
        if len(res) == 1:
            return res[0].attrs.get('href')
        else:
            t = [x for x in res if str(system.Bit) in x.text]
            if len(t) == 1:
                return t[0].attrs.get('href')
            return min(res, key=lambda x: len(x.text)).attrs.get('href')

    def Download(self, system: SYSTEM) -> ParseResult:
        """
        Download(system: SYSTEM) -> ParseResult
        获取驱动下载链接

        :param system: 系统类
        :return: ParseResult
        """
        driver_version = self.__Filtrate_Version(
            chrome_version=system.Chrome_Version
        )
        driver_version = self.__Defininite().geturl().format(path=driver_version)
        driver_version = urlparse(url=driver_version)
        soups = self.__Select_Driver(drivers_link=driver_version)
        path = self.__Filtrate_Driver(system=system, soups=soups)
        index = path[1:].find('/')+1
        return urlparse(
            url=self.__Download_link().geturl().format(path=path[index:])
        )
