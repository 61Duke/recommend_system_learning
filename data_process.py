# -*- coding:utf-8-*-
"""
对网易云所有歌单爬虫的json文件进行数据预处理成csv文件
python3.6环境
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
import json


def parse_playlist_item():
    """
    :return: 解析成userid itemid rating timestamp行格式
    """
    file = open("neteasy_playlist_recommend_data.csv", 'a', encoding='utf8')
    for i in range(1, 1292):
        with open("neteasy_playlist_data/{0}.json".format(i), 'r', encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
            try:
                for item in load_dict['playlist']['tracks']:
                    # playlist id # song id # score # datetime
                    line_result = [load_dict['playlist']['id'], item['id'], item['pop'], item['publishTime']]
                    for k, v in enumerate(line_result):
                        if k == len(line_result) - 1:
                            file.write(str(v))
                        else:
                            file.write(str(v) + ',')
                    file.write('\n')
            except Exception:
                print(i)
                continue
    file.close()


def parse_playlist_id_to_name():
    file = open("neteasy_playlist_id_to_name_data.csv", 'a', encoding='utf8')
    for i in range(1, 1292):
        with open("neteasy_playlist_data/{0}.json".format(i), 'r', encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
            try:
                line_result = [load_dict['playlist']['id'], load_dict['playlist']['name']]
                for k, v in enumerate(line_result):
                    if k == len(line_result) - 1:
                        file.write(str(v))
                    else:
                        file.write(str(v) + ',')
                file.write('\n')
            except Exception:
                print(i)
                continue
    file.close()


def parse_song_id_to_name():
    file = open("neteasy_song_id_to_name_data.csv", 'a', encoding='utf8')
    for i in range(1, 1292):
        with open("neteasy_playlist_data/{0}.json".format(i), 'r', encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
            try:
                for item in load_dict['playlist']['tracks']:
                    # playlist id # song id # score # datetime
                    line_result = [item['id'], item['name'] + '-' + item['ar'][0]['name']]
                    for k, v in enumerate(line_result):
                        if k == len(line_result) - 1:
                            file.write(str(v))
                        else:
                            file.write(str(v) + ',')
                    file.write('\n')
            except Exception:
                print(i)
                continue
    file.close()
#
# parse_playlist_item()
# parse_playlist_id_to_name()
# parse_song_id_to_name()
