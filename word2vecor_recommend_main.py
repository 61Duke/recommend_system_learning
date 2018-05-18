# python3+
import json
from random import shuffle
import multiprocessing
import gensim
import csv


def train_song2vec():
    """
    :return: 所有歌单song2Vec模型的训练和保存
    """
    songlist_sequence = []
    # 读取网易云音乐原数据
    for i in range(1, 1292):
        with open("neteasy_playlist_data/{0}.json".format(i), 'r', encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
            parse_songlist_get_sequence(load_dict, songlist_sequence)

    # 多进程计算
    cores = multiprocessing.cpu_count()
    print('Using all {cores} cores'.format(cores=cores))
    print('Training word2vec model...')
    model = gensim.models.Word2Vec(sentences=songlist_sequence, size=150, min_count=3, window=7, workers=cores)
    print('Save model..')
    model.save('songVec.model')


def parse_songlist_get_sequence(load_dict, songlist_sequence):
    """
    解析每个歌单中的歌曲id信息
    :param load_dict: 包含一个歌单中所有歌曲的原始列表
    :param songlist_sequence: 一个歌单中所有给的id序列
    :return:
    """
    song_sequence = []
    for item in load_dict['playlist']['tracks']:
        try:
            song = [item['id'], item['name'], item['ar'][0]['name'], item['pop']]
            song_id, *song_name, artist, pop = song
            song_sequence.append(str(song_id))
        except:
            print('song format error')

    for i in range(len(song_sequence)):
        shuffle(song_sequence)
        # 这里的list()必须加上，要不songlist中歌曲根本就不是随机打乱序列，而是都相同序列
        songlist_sequence.append(list(song_sequence))


def song_data_preprocessing():
    """
    歌曲id到歌曲名字的映射
    :return: 歌曲id到歌曲名字的映射字典，歌曲名字到歌曲id的映射字典
    """
    csv_reader = csv.reader(open('neteasy_song_id_to_name_data.csv', encoding='utf-8'))
    id_name_dic = {}
    name_id_dic = {}
    for row in csv_reader:
        id_name_dic[row[0]] = row[1]
        name_id_dic[row[1]] = row[0]
    return id_name_dic, name_id_dic


# train_song2vec()

model_str = 'songVec.model'
# 载入word2vec模型
model = gensim.models.Word2Vec.load(model_str)
id_name_dic, name_id_dic = song_data_preprocessing()

song_id_list = list(id_name_dic.keys())[:20:2]
for song_id in song_id_list:
    result_song_list = model.most_similar(song_id)
    print(song_id, id_name_dic[song_id])
    print('\n相似歌曲和相似度分别为：')
    for song in result_song_list:
        print('\t' + id_name_dic[song[0]], song[1])
    print('\n')

