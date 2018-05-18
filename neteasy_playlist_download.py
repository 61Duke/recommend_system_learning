# -*- coding:utf-8 -*-
"""
爬虫爬取网易云音乐歌单的数据包保存成json文件
python2.7环境
"""
import requests
import json
import os
import base64
import binascii
import urllib
import urllib2
from Crypto.Cipher import AES
from bs4 import BeautifulSoup


class NetEaseAPI:
    def __init__(self):
        self.header = {
            'Host': 'music.163.com',
            'Origin': 'https://music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': 'application/json, text/javascript',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.cookies = {'appver': '1.5.2'}
        self.playlist_class_dict = {}
        self.session = requests.Session()

    def _http_request(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        connection = json.loads(self._raw_http_request(method, action, query, urlencoded, callback, timeout))
        return connection

    def _raw_http_request(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        if method == 'GET':
            request = urllib2.Request(action, self.header)
            response = urllib2.urlopen(request)
            connection = response.read()
        elif method == 'POST':
            data = urllib.urlencode(query)
            request = urllib2.Request(action, data, self.header)
            response = urllib2.urlopen(request)
            connection = response.read()
        return connection

    @staticmethod
    def _aes_encrypt(text, secKey):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    @staticmethod
    def _rsa_encrypt(text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    @staticmethod
    def _create_secret_key(size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    def get_playlist_id(self, action):
        request = urllib2.Request(action, headers=self.header)
        response = urllib2.urlopen(request)
        html = response.read().decode('utf-8')
        response.close()
        soup = BeautifulSoup(html, 'lxml')
        list_url = soup.select('ul#m-pl-container li div a.msk')
        for k, v in enumerate(list_url):
            list_url[k] = v['href'][13:]
        return list_url

    def get_playlist_detail(self, id):
        text = {
            'id': id,
            'limit': '100',
            'total': 'true'
        }
        text = json.dumps(text)
        nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
                   'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
                   '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
                   '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
                   '3ece0462db0a22b8e7')
        secKey = self._create_secret_key(16)
        encText = self._aes_encrypt(self._aes_encrypt(text, nonce), secKey)
        encSecKey = self._rsa_encrypt(secKey, pubKey, modulus)

        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        action = 'http://music.163.com/weapi/v3/playlist/detail'
        playlist_detail = self._http_request('POST', action, data)

        return playlist_detail


if __name__ == '__main__':
    nn = NetEaseAPI()

    index = 1
    for flag in range(1, 38):
        if flag > 1:
            page = (flag - 1) * 35
            url = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=' + str(
                page)
        else:
            url = 'http://music.163.com/discover/playlist'
        playlist_id = nn.get_playlist_id(url)
        for item_id in playlist_id:
            playlist_detail = nn.get_playlist_detail(item_id)

            with open('{0}.json'.format(index), 'w') as file_obj:
                json.dump(playlist_detail, file_obj, ensure_ascii=False)
                index += 1
                print("写入json文件：", item_id)
