import unittest

import os, sys
sys.path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))] + sys.path
from spacy_space.engine import SplitEngine


class NotStrippedTest(unittest.TestCase):
    def test_english_sentence_split(self):
        nlp = SplitEngine("en", "sm")

        text = """
        Alice said "Hi!" to Bob. Bob then gave her a 1,000 dollar worth pearl necklace.
        """

        nlp.load_document(text)

        print(nlp.to_chunks(len_chunk=20))

    def test_korean_sentence_split(self):
        nlp = SplitEngine("ko", "sm")

        text = """
        아린이는 "안녕!"이라고 범준이에게 말했어요. 그러자 범준이는 그녀에게 백만원 짜리 진주 목걸이를 주었어요.
        """

        nlp.load_document(text)

        print(nlp.to_chunks_by_len(10))


if __name__ == "__main__":
    unittest.main()