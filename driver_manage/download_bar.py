#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/12
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : download_bar.py
# @Function : 下载进度

import os
import requests
from urllib.request import urlopen
from tqdm import tqdm

from config.can_change_config import BAR_LENGTH


def download(url, dst):
    file_size = int(urlopen(url).info().get('Content-Length', -1))
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size,
        initial=first_byte,
        unit='B',
        unit_scale=True,
        desc=url.split('/')[-1],
        ncols=BAR_LENGTH
    )
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
            else:
                f.close()
    pbar.close()
    return file_size
