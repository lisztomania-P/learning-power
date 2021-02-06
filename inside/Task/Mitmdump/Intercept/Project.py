#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Project.py
# @Function :
import base64
import json
import re
from random import randint
from typing import Dict, List

from inside.Task.Mitmdump.Intercept.ABC_Answer import ABC_ANSWER

from inside.Baidu_AI.Baidu_AI_Manage import BAIDU_AI_MANAGE
from inside.Options.Options import OPTIONS
__all__ = ['PROJECT']


class PROJECT(ABC_ANSWER):
    """专项答题拦截体"""

    def Url_Put(self, url: str) -> bool:
        """
        Url_Put(url: str) -> bool
        提交判断

        :param url: url
        :return: bool
        """
        return "https://pc-proxy-api.xuexi.cn/api/exam/service/detail/submitV3" \
               == url

    def Url_Res(self, url: str) -> bool:
        """
        Url_Res(url: str) -> bool
        答案判断

        :param url: url
        :return: bool
        """
        res = "https://pc-proxy-api.xuexi.cn/api/exam/service/detail" \
              "/queryV3\\?type=1&id=.*&forced=true"
        if re.match(res, url):
            return True
        return False

    def Extract(self, data: bytes) -> Dict:
        """
        Extract(data: bytes) -> Dict
        提取答案

        :param data: 包含答案的字节数据
        :return: Dict
        """
        data = data.decode('utf-8')
        data = json.loads(data)['data_str']
        return json.loads(base64.b64decode(data).decode('utf-8'))

    def __Answer(self, res: Dict) -> List[Dict]:
        """
        __Answer(res: Dict) -> List[Dict]
        由于专项答题没有答案，判题是在云端，所以需要分析答案

        :param res: 包含提示的题目
        :return: List[Dict]
        """
        res_type = res['questionDisplay']
        temp = []
        options = re.findall(r"<font color=\"red\">.*?</font>",
                             res['questionDesc'])
        for index, value in enumerate(options):
            options[index] = value.split('>')[1].split('<')[0]
        if res_type in (1, 2):
            for option in options:
                for answer in res['answers']:
                    if option in answer['content'] or answer['content'] in option:
                        tp = {
                            'answerId': answer['answerId'],
                            'value': answer['label']
                        }
                        if tp not in temp:
                            temp.append(tp)
            if not temp:
                for answer in res['answers']:
                    if answer['content'] in res['questionDesc']:
                        tp = {
                            'answerId': answer['answerId'],
                            'value': answer['label']
                        }
                        if tp not in temp:
                            temp.append(tp)
        elif res_type == 4:
            if OPTIONS().Baidu_AI:
                if res['questionDesc'] == '请观看视频':
                    body = res['body']
                    value = BAIDU_AI_MANAGE.Tools().Answer(video_link=res['videoUrl'])
                    print('检测到视频题目，由于专项答题答案匹配目前还未完善，所以需要手动填入答案')
                    print(f"题目部分:{body[body.index('（）')-len(value):]}")
                    print(f"答案为:{value}")
                    print("请从答案中提取个数与（）个数一致的答案，以空格分隔，注意顺序")
                    while True:
                        daan = input(":").strip().split()
                        check = [ck for ck in daan if ck in value]
                        if len(check) != len(daan):
                            print("输入非答案，重新输入！")
                            continue
                        break
                    for index, answer in enumerate(res['answers']):
                        temp.append({
                            'answerId': answer['answerId'],
                            'value': daan[index]
                        })
            else:
                num = res['body'].count('（）')
                if num == 1:
                    tp = ''
                    for option in options:
                        tp += option
                    temp.append(
                        {
                            'answerId': res['answers'][0]['answerId'],
                            'value': tp
                        }
                    )
                else:
                    for index, option in enumerate(options):
                        temp.append(
                            {
                                'answerId': res['answers'][index]['answerId'],
                                'value': option
                            }
                        )
        return temp

    def Inject(self, data: bytes, res: Dict) -> bytes:
        """
        Inject(data: bytes, res: Dict) -> bytes
        注入答案

        :param data: 原始提交数据
        :param res: 包含答案数据
        :return: 修改后的提交数据
        """
        data = json.loads(data.decode('utf-8'))
        data['uniqueId'] = res['uniqueId']
        data['questions'].clear()
        data['usedTime'] = randint(20, 50)
        for question in res['questions']:
            data['questions'].append(
                {
                    'questionId': question['questionId'],
                    'answers': self.__Answer(res=question)
                }
            )
        return json.dumps(data).encode('utf-8')