#!/usr/bin/env python
# -*- coding:utf-8 -*-

from extractword.extractor import Extractor

def main():
    import sys
    query = sys.argv[1]
    ex = Extractor()
    for word, location in ex.parse(query):
        print "word: %s, location:%d" % (word, location)
        
if __name__ == "__main__":
    main()