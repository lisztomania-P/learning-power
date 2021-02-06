#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/5
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Baidu_AI_Tools.py
# @Function : 百度AI图像文字识别工具
import requests
import base64
import cv2
from PIL import Image

from inside.DB.Table_Class.Baidu_AI import BAIDU_AI
from inside.Template.Meta_Singleton import SINGLETON
__all__ = ['BAIDU_AI_TOOLS']


class BAIDU_AI_TOOLS(metaclass=SINGLETON):
    """百度AI工具"""
    __token: str

    def __init__(self, baidu_ai: BAIDU_AI):
        """
        BAIDU_AI_TOOLS(baidu_ai: BAIDU_AI)
        初始化

        Args:
            baidu_ai: 百度AI
        """
        self.__self = '_'+type(self).__name__
        self.__ai = baidu_ai
        self.__Set_Token()

    def __Set_Token(self) -> None:
        """
        __Set_Token() -> None
        获取设置token

        Returns: None

        """
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type' \
               f'=client_credentials&client_id={self.__ai.Ak}&client_' \
               f'secret={self.__ai.Sk}'
        html = requests.get(host)
        self.__token = html.json().get('access_token')

    @classmethod
    def Cut(cls, video_link: str) -> bytes:
        """
        Cut(video_link: str) -> bytes
        取帧迭代器

        Args:
            video_link: 视频链接

        Returns: 图片

        """
        video = cv2.VideoCapture(video_link)
        if video.isOpened():
            frame_rate = video.get(5)
            frame_number = video.get(7)
            interval = frame_number // frame_rate
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate * (interval - 2))
            num = 0
            rval, frame = video.read()
            while rval:
                if num % frame_rate == 0:
                    ret, buf = cv2.imencode('.jpg', frame)
                    pic = Image.fromarray(buf).tobytes()
                    yield pic
                rval, frame = video.read()
                num += 1

    def Answer(self, video_link: str) -> str:
        """
        Answer(video_link: str) -> str
        获取答案
        通用文字识别（高精度版）

        Args:
            video_link: 视频链接

        Returns: str

        """
        video = self.Cut(video_link=video_link)
        while True:
            try:
                img = base64.b64encode(next(video))
            except StopIteration:
                break
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1" \
                          "/accurate_basic"
            params = {"image": img}
            request_url = request_url + "?access_token=" + self.__token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                for words in response.json()['words_result']:
                    for topic in ('考题答案:', '考题答案', '参考答案:', '参考答案'):
                        if topic in words['words']:
                            return words['words'].replace(topic, '').strip()
