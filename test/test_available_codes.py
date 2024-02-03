import unittest

import os, sys
sys.path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))] + sys.path
from spacy_space.engine import SplitEngine


class AvailableCodesTest(unittest.TestCase):
    def test_lang_codes(self):
        print(SplitEngine.get_available_lang_codes())

    def test_size_codes(self):
        print(SplitEngine.get_available_size_codes("en"))


if __name__ == "__main__":
    unittest.main()