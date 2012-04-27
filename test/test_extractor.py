#!/usr/bin/env python
# -*- coding:utf-8 -*-

from extractword.extractor import Extractor
import unittest

class TestExtractor(unittest.TestCase):
    
    def setUp(self):
        self.ex = Extractor()
        self.text = u"2番目に重要な物を選んでください。"
        # 予測されるデータ
        self.correct = (
                ("2番目", 0),
                ("重要", 4)
            )
    
    def test_parse(self):
        emsg = "Not Match!"
        for i, pair in enumerate(self.ex.parse(self.text)):
            word, location = pair
            pre_word, pre_location = self.correct[i]
            self.assertEqual(word, pre_word, emsg)
            self.assertEqual(location, pre_location, emsg)
        self.assertEqual(i + 1, len(self.correct), "Not match the number of term.")

if __name__ == '__main__':
    unittest.main()