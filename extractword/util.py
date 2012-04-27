#!/usr/bin/env python
# -*- coding:utf-8 -*-

__doc__ = '''
ユーティリティメソッド、クラスを提供します
'''

__all__ = ("encoder", "guess_decode", )

## デコードで試す文字コードのリスト ###
codes = ('utf8', 'shift-jis', 'euc-jp')

def guess_decode(text):
    ''' 
    引数をunicode型に変換します 
    
    @param text: unicode or str
    @return: unicode
    '''
    if isinstance(text, unicode):
        return text
    for code in codes:
        try:
            return text.decode(code)
        except UnicodeDecodeError:
            pass
    else:
        raise UnicodeDecodeError("Can't decode %s." % text)
    
def encoder(text, encoding='utf8'):
    ''' 
    第一引数で指定した文字列を第二引数で指定したencodingでencodeします
     
    @param text: str or unicode
    @param encoding: str
    @return: str
    '''
    if not isinstance(text, unicode):
        return text 
    return text.encode(encoding)
