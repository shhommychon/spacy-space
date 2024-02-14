from collections.abc import Iterable


def assert_string(text:str):
    """Checks if the input value is string type.
    """
    # Input is string
    if type(text) is str: return text

    # Input is an iterable of string elements
    if isinstance(text, Iterable) and all(isinstance(i, str) for i in text):
        from warnings import warn
        warn("A string was expected, but an iterable of strings was received. Joining all elements into one string.")
        return ' '.join(text)
    
    raise AssertionError("Input must be a string.")
