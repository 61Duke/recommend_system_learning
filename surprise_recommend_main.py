# -*- coding:utf-8-*-
"""
利用surprise推荐库 KNN协同过滤算法推荐网易云歌单
python2.7环境
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import csv
from surprise import KNNBaseline, Reader, KNNBasic, KNNWithMeans, evaluate
from surprise import Dataset


def recommend_model():
    file_path = os.path.expanduser('neteasy_playlist_recommend_data.csv')
    # 指定文件格式
    reader = Reader(line_format='user item rating timestamp', sep=',')
    # 从文件读取数据
    music_data = Dataset.load_from_file(file_path, reader=reader)
    # 计算歌曲和歌曲之间的相似度

    train_set = music_data.build_full_trainset()
    print('开始使用协同过滤算法训练推荐模型...')
    algo = KNNBasic()
    algo.fit(train_set)
    return algo


def playlist_data_preprocessing():
    csv_reader = csv.reader(open('neteasy_playlist_id_to_name_data.csv'))
    id_name_dic = {}
    name_id_dic = {}
    for row in csv_reader:
        id_name_dic[row[0]] = row[1]
        name_id_dic[row[1]] = row[0]
    return id_name_dic, name_id_dic


def song_data_preprocessing():
    csv_reader = csv.reader(open('neteasy_song_id_to_name_data.csv'))
    id_name_dic = {}
    name_id_dic = {}
    for row in csv_reader:
        id_name_dic[row[0]] = row[1]
        name_id_dic[row[1]] = row[0]
    return id_name_dic, name_id_dic


def playlist_recommend_main():
    print("加载歌单id到歌单名的字典映射...")
    print("加载歌单名到歌单id的字典映射...")
    id_name_dic, name_id_dic = playlist_data_preprocessing()
    print("字典映射成功...")
    print('构建数据集...')
    algo = recommend_model()
    print('模型训练结束...')

    current_playlist_id = id_name_dic.keys()[200]
    print('当前的歌单id：' + current_playlist_id)

    current_playlist_name = id_name_dic[current_playlist_id]
    print('当前的歌单名字：' + current_playlist_name)

    playlist_inner_id = algo.trainset.to_inner_uid(current_playlist_id)
    print('当前的歌单内部id：' + str(playlist_inner_id))

    playlist_neighbors = algo.get_neighbors(playlist_inner_id, k=10)
    playlist_neighbors_id = (algo.trainset.to_raw_uid(inner_id) for inner_id in playlist_neighbors)
    # 把歌曲id转成歌曲名字
    playlist_neighbors_name = (id_name_dic[playlist_id] for playlist_id in playlist_neighbors_id)
    print("和歌单<", current_playlist_name, '> 最接近的10个歌单为：\n')
    for playlist_name in playlist_neighbors_name:
        print(playlist_name, name_id_dic[playlist_name])


playlist_recommend_main()

file_path = os.path.expanduser('neteasy_playlist_recommend_data.csv')
# 指定文件格式
reader = Reader(line_format='user item rating timestamp', sep=',')
# 从文件读取数据
music_data = Dataset.load_from_file(file_path, reader=reader)
# 分成5折
music_data.split(n_folds=5)

algo = KNNBasic()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])
print(perf)
