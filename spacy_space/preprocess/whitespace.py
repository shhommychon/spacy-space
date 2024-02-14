import re


# Regular expression matching whitespace:
__whitespace_re = re.compile(r"\s+")


def strip_whitespace(text:str):
    """Removes leading and trailing whitespace characters (spaces, tabs, and newlines) from input string.

    refer to pull request #2 (https://github.com/shhommychon/spacy-space/pull/2)
    """
    return text.strip()


def collapse_whitespace(text:str):
    """Collapse duplicate whitespace into single space.

    original code from: https://github.com/keithito/tacotron/blob/master/text/cleaners.py
    """
    return re.sub(__whitespace_re, ' ', text)