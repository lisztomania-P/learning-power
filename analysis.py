#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/29
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : analysis.py
# @Function : 解析Json信息
import base64
import json
import os
import glob
from typing import Dict, List

import db_manage
import get_random
import user_msg
from article import Article
from configuration import MSG_APIS, TASK_APIS, \
    TASK_ID, WEEKLY_ANSWER_TOPICS_API, PROJECT_ANSWER_TOPICS_API, \
    DB_TEMP_DIR_JSON
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from video import Video

true = True
false = False
null = None


# 解析json
def analysis_json(tags: WebElement) -> Dict:
    result = json.loads(tags.text)
    return result


# 解析用户信息
class Analysis_Msg(object):
    # 积分窗口
    __score_driver: WebDriver
    # 累计积分
    __aggregate_score: Dict
    # 每日积分
    __daily_score: Dict
    # 任务进度
    __task_bar: Dict
    # 等级
    __level: Dict

    __wait: WebDriverWait

    def __init__(self, score_driver: WebDriver):
        self.__score_driver = score_driver
        self.__wait = WebDriverWait(self.__score_driver, 10)
        self.__messages()

    # 抓取信息
    def __messages(self):
        for key, value in MSG_APIS.items():
            self.__score_driver.get(value)
            msg_Ec = EC.presence_of_element_located(
                (
                    By.TAG_NAME, 'pre'
                )
            )
            temp_tags = self.__wait.until(msg_Ec)
            msg = analysis_json(tags=temp_tags)
            if key == 'aggregate_score_api':
                self.__aggregate_score = msg
            elif key == 'daily_score_api':
                self.__daily_score = msg
            elif key == 'task_bar_api':
                self.__task_bar = msg
            elif key == 'level_api':
                self.__level = msg

    # 获取用户ID
    @property
    def uid(self) -> int:
        return self.__aggregate_score['data']['userId']

    # 获取累计积分
    @property
    def aggregate_score(self) -> Dict:
        name = self.__aggregate_score['data']['scoreTypeName']
        aggregate_score: Dict = {
            'name': name if name else '总积分',
            'score': self.__aggregate_score['data']['score']
        }
        return aggregate_score

    # 获取每日积分
    @property
    def daily_score(self) -> Dict:
        name = self.__daily_score['data']['scoreTypeName']
        daily_score: Dict = {
            'name': name if name else '日积分',
            'score': self.__daily_score['data']['score']
        }
        return daily_score

    # 获取任务进度
    @property
    def task_bar(self) -> Dict:
        task_bar: Dict = dict()
        for task in self.__task_bar['data']['dayScoreDtos']:
            task_bar[TASK_ID[task['ruleId']]] = task
        return task_bar

    # 获取等级信息
    @property
    def level(self) -> Dict:
        level: Dict = {
            'name': self.__level['data']['levelName'],
            'level': self.__level['data']['level']
        }
        return level


# 任务分发器
class Analysis_Task(object):
    # 任务窗口
    __task_driver: WebDriver
    # 任务大纲
    __task_parent: Dict
    # 任务细则
    __task_son: str

    # 数据库
    __db: db_manage = db_manage

    __wait: WebDriverWait

    # 初始化，直至任务装填完毕
    def __init__(self, task_driver: WebDriver):
        self.__task_driver = task_driver
        self.__wait = WebDriverWait(self.__task_driver, 10)
        self.__db.connect_db()

    def __check_article_db(self, limit: int):
        temp = 1
        while not self.__db.exist_unseen_article(limit=limit):
            print("文章任务不足，正在获取中:"+str(temp))
            self.__check_task_parent()
            self.__set_task_son()
            self.__set_task_type()
            self.__check_file()
            temp += 1

    def __check_video_db(self, limit: int):
        temp = 1
        while not self.__db.exist_unseen_video(limit=limit):
            print("视频任务不足，正在获取中:"+str(temp))
            self.__check_task_parent()
            self.__set_task_son()
            self.__set_task_type()
            self.__check_file()
            temp += 1

    def __insert_db_article(self, task: Dict):
        article = Article(
            itemId=task['itemId'],
            url=task['url'],
            see=False
        )
        self.__db.exist_insert_article(article=article)

    def __insert_db_video(self, task: Dict):
        video = Video(
            itemId=task['itemId'],
            url=task['url'],
            see=False
        )
        self.__db.exist_insert_video(video=video)

    # 检查任务大纲
    def __check_task_parent(self):
        try:
            if self.__task_parent:
                pass
        except AttributeError:
            self.__set_task_parent()

    # 获取任务大纲
    def __set_task_parent(self):
        self.__task_driver.get(url=TASK_APIS['task_parent_api'])
        res_Ec = EC.presence_of_element_located(
            (
                By.TAG_NAME, 'pre'
            )
        )
        result = self.__wait.until(res_Ec)
        self.__task_parent = analysis_json(tags=result)

    # 获取任务细则
    def __set_task_son(self):
        pop = None
        for key in self.__task_parent:
            self.__task_driver.get(
                url=TASK_APIS['task_son_api'].format(key))
            if self.__task_driver.current_url == \
                    TASK_APIS['task_no_found_api']:
                continue
            temp_son = self.__task_driver.find_element_by_tag_name(
                name='pre').text
            self.__task_son = temp_son
            if self.__task_son:
                pop = key
                break
        self.__task_parent.pop(pop)

    # 分类任务
    def __set_task_type(self):
        tasks = self.__task_son
        result = eval(tasks)
        for task in result:
            if task['type'] == 'tuwen':
                self.__insert_db_article(task=task)
            elif task['type'] == 'shipin':
                self.__insert_db_video(task=task)
        self.__task_son = ''

    def __check_file(self):
        for path in glob.glob(DB_TEMP_DIR_JSON):
            with open(path, 'r', encoding='utf-8') as f:
                self.__task_son = f.read()
                f.close()
            self.__set_task_type()
            os.remove(path)

    # 抽取文章任务
    def get_article_tasks(self, task_number: int = 6) -> List[Article]:
        self.__check_article_db(limit=task_number)
        return self.__db.get_article(limit=task_number)

    # 抽取视频任务
    def get_video_tasks(self, task_number: int = 6) -> List[Video]:
        self.__check_video_db(limit=task_number)
        return self.__db.get_video(limit=task_number)

    # 更新文章已读
    def update_article_see(self, article: Article):
        self.__db.update_article_see(article=article)

    # 更新视频已读
    def update_video_see(self, video: Video):
        self.__db.update_video_see(video=video)


# 每周答题任务提取
class Analysis_Weekly_Answer(object):
    __topic_api: str = WEEKLY_ANSWER_TOPICS_API
    __topic_list: List[Dict] = []
    __driver: WebDriver = None

    def __init__(self, task_driver: WebDriver):
        self.__driver = task_driver
        self.__init_topic()

    def __init_topic(self):
        end = get_random.get_random_int(4, 5)
        for start in range(1, end):
            url = self.__topic_api.format(page=start)
            self.__driver.get(url=url)
            code: WebElement = self.__driver.find_element_by_tag_name(
                name='pre')
            code: Dict = analysis_json(tags=code)
            code['data_str'] = json.loads(
                base64.b64decode(code['data_str']).decode('utf-8')
            )
            if not code['data_str']['list']:
                break
            for topics in code['data_str']['list']:
                for topic in topics['practices']:
                    if not topic['seeSolution']:
                        self.__topic_list.append(topic)
            if self.__topic_list:
                break

    def get_topic(self) -> int:
        topic_num: int = len(self.__topic_list)
        index: int = get_random.get_random_int(0, topic_num - 1)
        temp: Dict = self.__topic_list.pop(index)
        return temp['id']


# 专项答题任务提取
class Analysis_Project_Answer(object):
    __topic_api: str = PROJECT_ANSWER_TOPICS_API
    __topic_list: List[Dict] = []
    __driver: WebDriver
    __wait: WebDriverWait

    def __init__(self, task_driver: WebDriver):
        self.__driver = task_driver
        self.__wait = WebDriverWait(self.__driver, 10)
        self.__except_topic()

    def __except_topic(self):
        while True:
            try:
                self.__init_topic()
                break
            except KeyError:
                continue

    def __init_topic(self):
        end = get_random.get_random_int(4, 5)
        for start in range(end, 0, -1):
            url = self.__topic_api.format(page=start)
            self.__driver.get(url=url)
            code_Ec = EC.presence_of_element_located(
                (
                    By.TAG_NAME, 'pre'
                )
            )
            code: WebElement = self.__wait.until(code_Ec)
            code: Dict = analysis_json(tags=code)
            code['data_str'] = json.loads(
                base64.b64decode(code['data_str']).decode('utf-8')
            )
            if not code['data_str']['list']:
                continue
            for topics in code['data_str']['list']:
                if not topics['overdue']:
                    self.__topic_list.append(topics)
            if self.__topic_list:
                break

    def get_topic(self) -> int:
        temp: Dict = self.__topic_list.pop()
        user_msg.USER_PROJECT_ANSWER_TASKS = temp['questionNum']
        return temp['id']
