from typing import Any, Dict, Union

import spacy
from spacy.util import SimpleFrozenDict
from spacy.vocab import Vocab
from thinc.api import Config

from .resources import _SUPPORTED_LANGUAGES, _LANG_ALIASES, _SIZE_ALIASES


class LangEngine:
    def __init__(
        self,
        resource_lang_code: str,
        resource_size_code: str,
        vocab: Union[Vocab, bool] = True,
        config: Union[Dict[str, Any], Config] = SimpleFrozenDict(),
    ):
        """Loads a spaCy model for sentence intra-splitting.

        resource_lang_code (str): language code mapped to spaCy package name.
            Refer to `LangEngine.get_available_lang_codes()` for proper language codes.
        resource_size_code (str): model size code mapped to spaCy package name.
            Refer to `LangEngine.get_available_size_codes(lang_code)` for proper size codes.
        vocab (Vocab): `vocab` parameter for `spacy.load()` function.
            A Vocab object. If True, a vocab is created.
        config (Dict[str, Any] / Config): `config` parameter for `spacy.load()` function.
            Config overrides as nested dict or dict keyed by section values in dot notation.
        """
        # normalize language code
        lang_code = lang_code.lower()
        if lang_code in _LANG_ALIASES: lang_code = _LANG_ALIASES[lang_code]

        # normalize size code
        size_code = size_code.lower()
        if size_code in _SIZE_ALIASES: size_code = _SIZE_ALIASES[size_code]

        # get spaCy model code
        resource_name = self.get_resource_name(resource_lang_code, resource_size_code)

        # set spaCy model as engine
        self.nlp_engine = spacy.load(
            resource_name, 
            # exclude every pipeline except "tok2vec", "tagger", "parser"
            exclude=["attribute_ruler", "lemmatizer", "morphologizer", "ner", "senter"],
            vocab=vocab,
            config=config,
        )

        self.__document = ""
        self.__sentences = list()


    # def __call__(self, text:str):


    def get_resource_name(self, lang_code, size_code):
        try:
            if lang_code in (): self.assert_lang_code(lang_code)
            model_code = _SUPPORTED_LANGUAGES[lang_code][size_code]
            return model_code
        except IndexError:
            self.assert_size_code(lang_code, size_code)
    
    def assert_lang_code(self, lang_code):
        available_lang_codes = self.get_available_lang_codes()
        assert lang_code in available_lang_codes, \
            f"'{lang_code}' is not an available language code. " \
            "Refer to `LangEngine.get_available_lang_codes()` for proper language codes."
    
    def assert_size_code(self, lang_code, size_code):
        available_size_codes = self.get_available_size_codes(lang_code)
        assert size_code in available_size_codes, \
            f"'{size_code}' is not an available size code " \
            f"among the available size codes {available_size_codes} for '{lang_code}' language."

    def get_available_lang_codes(self):
        return [ k for k, v in _SUPPORTED_LANGUAGES.items if len(v)>0 ]
    
    def get_available_size_codes(self, lang_code):
        try: return [ k for k, _ in _SUPPORTED_LANGUAGES[lang_code].items ]
        except: self.assert_lang_code(lang_code)
