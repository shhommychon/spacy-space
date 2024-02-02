from copy import deepcopy
import numpy as np
from typing import Any, Dict, Union

import spacy
from spacy.tokens.token import Token
from spacy.util import SimpleFrozenDict
from spacy.vocab import Vocab
from thinc.api import Config

from .entities import DependencyEdge
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
        resource_lang_code = resource_lang_code.lower()
        if resource_lang_code in _LANG_ALIASES: resource_lang_code = _LANG_ALIASES[resource_lang_code]

        # normalize size code
        resource_size_code = resource_size_code.lower()
        if resource_size_code in _SIZE_ALIASES: resource_size_code = _SIZE_ALIASES[resource_size_code]

        # get spaCy model code
        resource_name = self.get_resource_name(resource_lang_code, resource_size_code)

        # set spaCy model as engine
        try:
            self.nlp_engine = spacy.load(
                resource_name, 
                # exclude every pipeline except "tok2vec", "tagger", "parser"
                exclude=["attribute_ruler", "lemmatizer", "morphologizer", "ner", "senter"],
                vocab=vocab,
                config=config,
            )
        except OSError:
            # package not yet downloaded.
            import subprocess
            cmd = f"python -m spacy download {resource_name}"
            subprocess.run(cmd, shell=True, check=True)

            # try again
            self.nlp_engine = spacy.load(
                resource_name, 
                exclude=["attribute_ruler", "lemmatizer", "morphologizer", "ner", "senter"],
                vocab=vocab,
                config=config,
            )

        self.__document = ""

    
    def load_document(self, text:str):
        """Loads a non-splitted string of single document and reformat.

        text (str): non-splitted string of a single document.
        """
        self.__document = text
        doc = self.nlp_engine(self.__document)

        self.__sentences = list() # ①
        self.__token_values = list() # ②
        self.__edges = list() # ③
        self.__valid_token_indices = list() # ④
        self.__subtree_indices = list() # ⑤

        for sent in doc.sents:
            # add raw sentence string into ①
            self.__sentences.append(str(sent))

            # temporary list objects for ② `self.__token_values`
            this_sent_token_values_m = [ None for _ in range(len(sent))]
            this_sent_token_values_l = [ None for _ in range(len(sent))]
            this_sent_token_values_r = [ None for _ in range(len(sent))]

            # temporary list object for ③ `self.__edges`
            this_sent_edges = list()

            # temporary list object for ④ `self.__valid_token_indices`
            this_sent_valid_token_indices = np.array([ True for _ in range(len(sent)) ])

            # temporary list object for ⑤ `self.__subtree_indices`
            this_sent_subtree_indices = [ None for _ in range(len(sent))]

            # enumerate through tokens inside a single sentence
            for i, token in enumerate(sent):
                # save token index of whole document
                if i == 0: token_index_offset = token.i
                
                # save ② raw token objects to post-process
                ## if token is a special character
                if self.__is_special_token(token):
                    # first ancestor from the `ancestors` generator is direct parent
                    for a in token.ancestors: parent_token = a; break

                    if token.i - parent_token.i < 0:
                        # parent at right
                        this_sent_token_values_l[i+1] = token
                        this_sent_valid_token_indices[i] = False # ④
                    else:
                        # parent at left
                        this_sent_token_values_r[i-1] = token
                        this_sent_valid_token_indices[i] = False # ④
                ## if token is not a special character
                else:
                    this_sent_token_values_m[i] = token

                # save ③ dependency edge infos
                for child in token.children:
                    # only if connected child is not a special character.
                    if not self.__is_special_token(child):
                        this_sent_edges.append(
                            DependencyEdge(
                                length=abs(child.i-token.i),
                                parent_index=token.i-token_index_offset,
                                child_index=child.i-token_index_offset
                            )
                        )
                
                # save ⑤ all children indices
                this_token_subtree_indices = np.array([ False for _ in range(len(sent))])
                for child in token.subtree:
                    this_token_subtree_indices[child.i-token_index_offset] = True
                this_sent_subtree_indices[i] = this_token_subtree_indices
            
            # post-process ② raw token objects into strings
            this_sent_token_values = list()
            for l, m, r in zip(
                this_sent_token_values_l, 
                this_sent_token_values_m, 
                this_sent_token_values_r
            ):
                if m is not None:
                    this_token_left_index = m.idx
                    this_token_right_index = m.idx + len(str(m))
                    
                    if l is not None: this_token_left_index = l.idx
                    if r is not None: this_token_right_index = r.idx + len(str(r))

                    this_sent_token_values.append(str(doc)[this_token_left_index:this_token_right_index])
                else:
                    this_sent_token_values.append('')
            self.__token_values.append(np.array(this_sent_token_values))

            self.__edges.append(sorted(this_sent_edges))
            self.__valid_token_indices.append(this_sent_valid_token_indices)
            self.__subtree_indices.append(this_sent_subtree_indices)
    

    def to_sentences(self):
        self.assert_doc_loaded()
        return deepcopy(self.__sentences)

            
    def __is_special_token(self, token: Token):
        return (
            token.is_bracket
            or token.is_currency
            or token.is_left_punct
            or token.is_punct
            or token.is_quote
            or token.is_right_punct
            or token.is_space
        )


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
    
    def assert_doc_loaded(self):
        assert self.__document, \
            f"Document is not loaded into engine. " \
            "Please load some documents via `LangEngine.load_document(text:str)`."
