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
import pickle
import glob
from typing import Dict, List
import get_random
import user_msg
from configuration import MSG_APIS, TASK_APIS, DB_PARENT_SON_FILE_PATH, \
    TASK_ID, DB_TEMP_DIR, WEEKLY_ANSWER_TOPICS_API, PROJECT_ANSWER_TOPICS_API
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

true = True
false = False
null = None


# 解析json
def analysis_json(tags: WebElement) -> Dict:
    result = json.loads(tags.text)
    return result


# 清理垃圾
def clear_files(func):
    def wrapper(*args, **kwargs):
        files = os.path.join(DB_TEMP_DIR, "*")
        for file in glob.glob(files):
            os.remove(path=file)
        return func(*args, **kwargs)

    return wrapper


# 解析用户信息
class Analysis_Msg(object):
    # 用户信息API
    apis: Dict = MSG_APIS
    # 任务ID
    task_id: Dict = TASK_ID
    # 积分窗口
    __score_driver: WebDriver = None
    # 累计积分
    __aggregate_score: Dict = None
    # 每日积分
    __daily_score: Dict = None
    # 任务进度
    __task_bar: Dict = None
    # 等级
    __level: Dict = None

    def __init__(self, score_driver: WebDriver):
        self.__score_driver = score_driver
        self.__messages()

    # 抓取信息
    def __messages(self):
        for key, value in self.apis.items():
            self.__score_driver.get(value)
            temp_tags = self.__score_driver.find_element_by_tag_name(
                name='pre')
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
    def get_uid(self) -> int:
        uid: int = self.__aggregate_score['data']['userId']
        return uid

    # 获取累计积分
    def get_aggregate_score(self) -> Dict:
        name = self.__aggregate_score['data']['scoreTypeName']
        aggregate_score: Dict = {
            'name': name if name else '总积分',
            'score': self.__aggregate_score['data']['score']
        }
        return aggregate_score

    # 获取每日积分
    def get_daily_score(self) -> Dict:
        name = self.__daily_score['data']['scoreTypeName']
        daily_score: Dict = {
            'name': name if name else '日积分',
            'score': self.__daily_score['data']['score']
        }
        return daily_score

    # 获取任务进度
    def get_task_bar(self) -> Dict:
        task_bar: Dict = dict()
        for task in self.__task_bar['data']['dayScoreDtos']:
            task_bar[self.task_id[task['ruleId']]] = task
        return task_bar

    # 获取等级信息
    def get_level(self) -> Dict:
        level: Dict = {
            'name': self.__level['data']['levelName'],
            'level': self.__level['data']['level']
        }
        return level


# 任务分发器
class Analysis_Task(object):
    # 任务API
    apis: Dict = TASK_APIS
    # 任务窗口
    __task_driver: WebDriver = None
    # 任务大纲
    __task_parent: Dict = None
    # 任务细则
    __task_son: List = None
    # 任务分类
    __task_type: Dict = {
        'article': [],
        'video': [],
        'other': []
    }

    # 过滤器
    __task_parent_son: Dict = dict()
    # 过滤文件路径
    __task_parent_son_path: str = DB_PARENT_SON_FILE_PATH

    # 初始化，直至任务装填完毕
    def __init__(self, task_driver: WebDriver):
        self.__task_driver = task_driver
        self.__check_parent_son()
        self.__set_task_parent()
        self.__check_type()

    # 获取任务大纲
    @clear_files
    def __set_task_parent(self):
        self.__task_driver.get(url=self.apis['task_parent_api'])
        result = self.__task_driver.find_element_by_tag_name(name='pre')
        self.__task_parent = analysis_json(tags=result)

    # 获取任务细则
    @clear_files
    def __set_task_son(self):
        pop = None
        for key in self.__task_parent:
            self.__task_driver.get(
                url=self.apis['task_son_api'].format(key))
            if self.__task_driver.current_url == \
                    self.apis['task_no_found_api']:
                continue
            temp_son = self.__task_driver.find_element_by_tag_name(
                name='pre').text
            self.__task_son = [key, temp_son]
            if self.__task_son:
                pop = key
                break
        self.__task_parent.pop(pop)
        if pop not in self.__task_parent_son:
            self.__task_parent_son[pop] = []
            self.__update_parent_son()

    # 分类任务
    def __set_task_type(self):
        tasks = self.__task_son[1]
        result = eval(tasks)
        for task in result:
            if task['itemId'] in self.__task_parent_son[self.__task_son[0]]:
                continue
            elif task['type'] == 'tuwen':
                self.__task_type['article'].append((self.__task_son[0], task))
            elif task['type'] == 'shipin':
                self.__task_type['video'].append((self.__task_son[0], task))
            else:
                self.__task_type['other'].append((self.__task_son[0], task))
        self.__task_son.clear()

    # 检查装填
    def __check_type(self):
        while True:
            if self.__task_type['article'] and self.__task_type['video']:
                break
            self.__set_task_son()
            self.__set_task_type()

    # 初始化检查过滤器
    def __check_parent_son(self):
        if glob.glob(pathname=self.__task_parent_son_path):
            self.__load_parent_son()
        else:
            self.__update_parent_son()

    # 更新过滤器(内部)
    def __update_parent_son(self):
        with open(self.__task_parent_son_path, 'wb') as f:
            pickle.dump(obj=self.__task_parent_son, file=f)
            f.close()

    # 加载过滤器
    def __load_parent_son(self):
        with open(self.__task_parent_son_path, 'rb') as f:
            self.__task_parent_son = pickle.load(file=f)
            f.close()

    # 更新过滤器(外部)
    def update_parend_son(self, task: List):
        self.__task_parent_son[task[0]].append(task[1]['itemId'])
        self.__update_parent_son()
        self.__load_parent_son()

    # 随机抽取文章任务
    def get_article_tasks(self, task_number: int = 6) -> List:
        if len(self.__task_type['article']) < task_number:
            self.__refresh_tasks(key='article')
        tasks: List = []
        articles_len: int = len(self.__task_type['article'])
        while len(tasks) != task_number:
            index = get_random.get_random_int(a=0, b=articles_len - 1)
            temp = self.__task_type['article'][index]
            if temp not in tasks:
                tasks.append(temp)
        for task in tasks:
            self.__task_type['article'].remove(task)
        return tasks

    # 随机抽取视频任务
    def get_video_tasks(self, task_number: int = 6) -> List:
        if len(self.__task_type['video']) < task_number:
            self.__refresh_tasks(key='video')
        tasks: List = []
        videos_len: int = len(self.__task_type['video'])
        while len(tasks) != task_number:
            index = get_random.get_random_int(a=0, b=videos_len - 1)
            temp = self.__task_type['video'][index]
            if temp not in tasks:
                tasks.append(temp)
        for task in tasks:
            self.__task_type['video'].remove(task)
        return tasks

    # 刷新任务池
    def __refresh_tasks(self, key):
        self.__task_type[key].clear()
        self.__check_type()


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
    __driver: WebDriver = None

    def __init__(self, task_driver: WebDriver):
        self.__driver = task_driver
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
            code: WebElement = self.__driver.find_element_by_tag_name(
                name='pre')
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
