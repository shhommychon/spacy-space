from .stringify import *
from .whitespace import *


def preprocess(text):
    text = assert_string(text)
    text = strip_whitespace(text)
    text = collapse_whitespace(text)
    return text