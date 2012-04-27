#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MeCab
from extractword.util import guess_decode, encoder


class FeatureManager():
    '''
    単語の管理クラス
    '''
    
    # 状態変数の定義
    # 無視する
    IGNORE = 0
    # ストップワード
    STOP = 1
    # 連続性
    CONTINUITY = 2
    
    def __init__(self):
        '''
        self.words: 単語を積むリスト
        self.location: 現在保持している単語の位置情報
        '''
        self.words = list()
        self.location = None
        self.setup()
        
    def setup(self):
        '''
        状態変数判定メソッドの初期化を行います
        '''
        self.is_ignore_list = [
                self.is_end,
                self.is_pp_particle,
                self.is_substantive
            ]
        self.is_continuity_list = [
                self.is_prefix,
                self.is_number
            ]
        self.is_stop_list = [
                self.is_postfix,
                self.is_noun
            ]

    def is_end(self, features):
        '''
        終端のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return features[0] == u'BOS/EOS'
        
    def is_prefix(self, features):
        '''
        接頭詞のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return features[0] == u'接頭詞'

    def is_postfix(self, features):
        '''
        名詞の接尾のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return self.is_noun(features) and features[1] == u'接尾'

    def is_pp_particle(self, features):
        '''
        助詞のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return features[0] == u'助詞'
    
    def is_noun(self, features):
        '''
        名詞のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return features[0] == u"名詞"
    
    def is_number(self, features):
        '''
        数のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return features[1] == u"数"
    
    def is_substantive(self, features):
        '''
        非自立語のとき真を返します
        
        @param features: 品詞情報のリスト
        @return: bool
        '''
        return features[1] == u"非自立"
        
    def get_condition(self, feature, default=None):
        '''
        指定した形態素から状態変数を取得します
        連続系を優先的に配置すべき
        
        @param feature: 形態素
        @param default: デフォルトの状態変数
        '''
        if default is None:
            default = self.IGNORE
        # 品詞情報を分割
        features = feature.split(',')
        
        for method in self.is_continuity_list:
            if method(features):
                return self.CONTINUITY
            
        for method in self.is_ignore_list:
            if method(features):
                return self.IGNORE
            
        for method in self.is_stop_list:
            if method(features):
                return self.STOP

        return default
    
    def put(self, word, location, feature):
        '''
        真を返す場合は単語を返します
        
        @param word: str: 対象の単語
        @param location: int: 対象の単語の位置情報
        @param feature: str: 対象の品詞情報
        @return: bool 
        '''
        condition = self.get_condition(guess_decode(feature))
        if condition == self.IGNORE:
            return len(self.words) > 0
        return self._put(word, location, condition)
    
    def _put(self, word, location, condition):
        '''
        単語リストに単語を追加します
        
        @param word: 追加対象の単語
        @param location: 位置情報
        @param condition: 状態変数
        @return: bool
        '''
        if self.location is None:
            self.location = location
        self.words.append(word)
        return condition == self.STOP
        
    def get(self):
        '''
        累積している単語を連結して返します
        
        @return: str, int
        '''
        word = "".join(self.words)
        location = self.location
        self.clear()
        return word, location
    
    def clear(self):
        '''
        保持している情報をクリアします
        '''
        del self.words[:]
        self.location = None
    

class SimpleExtractor():
    ''' 自立語抽出の基底クラス '''
    
    def __init__(self):
        self.setup()
        
    def setup(self):
        pass
    
    def parse(self, *args, **kw):
        ''' 指定したテキストをパースして自立語を抽出して返します '''
        assert False, "Not Implemented."
        
            
class Extractor(SimpleExtractor):
    ''' 日本語の単語抽出クラス '''
    
    def __init__(self):
        SimpleExtractor.__init__(self)
        self.tagger = MeCab.Tagger('-Ochasen2')
        self.fm = FeatureManager()
        
    def parse(self, text):
        '''
        指定したテキストから単語とその位置情報を抽出します
        
        @param text: str or unicode
        @return: str, int
        '''
        _text = encoder(text)
        # 文書の先頭からの位置
        cur = 0
        node = self.tagger.parseToNode(_text)
        while node:
            u_word = guess_decode(node.surface)
            # 半角スペースの数を算出
            cur += node.rlength - node.length
            if self.fm.put(node.surface, cur, node.feature):
                yield self.fm.get()
            cur += len(u_word)
            node = node.next
            
            