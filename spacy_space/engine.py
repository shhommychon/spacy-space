from copy import deepcopy
import numpy as np
import sys
from typing import Any, Dict, Union

import spacy
from spacy.tokens.token import Token
from spacy.util import SimpleFrozenDict
from spacy.vocab import Vocab
from thinc.api import Config

from .entities import DependencyEdge
from .preprocess import preprocess
from .resources import _SUPPORTED_LANGUAGES, _LANG_ALIASES, _SIZE_ALIASES


class SplitEngine:
    def __init__(
        self,
        resource_lang_code: str,
        resource_size_code: str,
        vocab: Union[Vocab, bool] = True,
        config: Union[Dict[str, Any], Config] = SimpleFrozenDict(),
    ):
        """Loads a spaCy model for sentence intra-splitting.

        resource_lang_code (str): language code mapped to spaCy package name.
            Refer to `SplitEngine.get_available_lang_codes()` for proper language codes.
        resource_size_code (str): model size code mapped to spaCy package name.
            Refer to `SplitEngine.get_available_size_codes(lang_code)` for proper size codes.
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
            python_executable = sys.executable
            cmd = f"{python_executable} -m spacy download {resource_name}"
            subprocess.run(cmd, shell=True, check=True) # if error occurs, download manually.

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
        self.__document = preprocess(text)
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
        """Converts the loaded document into a list of sentences.

        RETURNS (List[str]): List of sentences in the document.
        """
        self.assert_doc_loaded()
        return deepcopy(self.__sentences)


    def to_chunks(self, num_chunk:int=None, len_chunk:int=None):
        """Converts the loaded document into chunks based on either number or length.

        num_chunk (int): Number of chunks to create.
        len_chunk (int): Maximum length of each chunk.

        RETURNS (List[str]): List of chunks.
        """
        self.assert_doc_loaded()
        assert (num_chunk is not None) or (len_chunk is not None), \
            "Either `num_chunk` param or `len_chunk` param must be given."
        if len_chunk is None:
            return self.to_chunks_by_num(num_chunk)
        if num_chunk is None:
            return self.to_chunks_by_len(len_chunk)

    def to_chunks_by_num(self, num_chunk:int):
        """Converts the loaded document into chunks based on the given number.

        num_chunk (int): Number of chunks to create.

        RETURNS (List[str]): List of chunks.
        """
        self.assert_doc_loaded()
        assert num_chunk > 0, "Valid `num_chunk` param must be given."

        chunks = list()
        for token_values, edges, valid_token_indices, subtree_indices in zip(
            self.__token_values, self.__edges, self.__valid_token_indices, self.__subtree_indices
        ):
            # Early stopping if there are fewer tokens than `num_chunk`.
            if len(token_values) <= num_chunk:
                for t in token_values: chunks.append(t)
                continue

            this_sent_subtree_indices = [deepcopy(valid_token_indices)]  # sentence subtree indices memory
            for i in range(num_chunk-1):
                edge = edges[i]
                this_sent_subtree_indices.append(deepcopy(subtree_indices[edge.child_index]))
            
            indices = list()
            condition = deepcopy(valid_token_indices)
            while this_sent_subtree_indices:
                this_chunk_subtree_indices = this_sent_subtree_indices.pop()  # last subtree in, first out
                this_chunk_subtree_indices = np.logical_and(this_chunk_subtree_indices, condition)  # check for already used parts of subtree
                if True in this_chunk_subtree_indices:  # if valid subtree indices,
                    indices.append(sorted(np.where(this_chunk_subtree_indices)[0]))
                condition = np.logical_and(np.logical_not(this_chunk_subtree_indices), condition)  # update condition on used parts of subtree
            indices = sorted(indices)  # final subtree indices
            for ids in indices:
                chunks.append(self.__token_array_to_chunk(token_values[ids]))
        
        return chunks

    def to_chunks_by_len(self, len_chunk:int):
        """Converts the loaded document into chunks based on the given length.

        len_chunk (int): Maximum length of each chunk.

        RETURNS (List[str]): List of chunks.
        """
        self.assert_doc_loaded()
        assert len_chunk > 0, "Valid `len_chunk` param must be given."

        chunks = list()
        for token_values, edges, valid_token_indices, subtree_indices in zip(
            self.__token_values, self.__edges, self.__valid_token_indices, self.__subtree_indices
        ):
            # Early stopping if the sentence has already shorter length than `len_chunk`.
            if len(self.__token_array_to_chunk(token_values)) <= len_chunk:
                chunks.append(self.__token_array_to_chunk(token_values))
                continue

            i = 0
            while i < len(edges):
                ok = True
                this_sent_subtree_indices = [deepcopy(valid_token_indices)]  # sentence subtree indices memory
                for j in range(i+1):
                    edge = edges[j]
                    this_sent_subtree_indices.append(deepcopy(subtree_indices[edge.child_index]))
                
                indices = list()
                condition = deepcopy(valid_token_indices)
                while this_sent_subtree_indices:
                    this_chunk_subtree_indices = this_sent_subtree_indices.pop()  # last subtree in, first out
                    this_chunk_subtree_indices = np.logical_and(this_chunk_subtree_indices, condition)  # check for already used parts of subtree
                    if True in this_chunk_subtree_indices:  # if valid subtree indices,
                        indices.append(sorted(np.where(this_chunk_subtree_indices)[0]))
                        if len(self.__token_array_to_chunk(token_values[indices[-1]])) > len_chunk:
                            # if this chunk does not meet the requirements,
                            ok = False
                            break  # start over
                    condition = np.logical_and(np.logical_not(this_chunk_subtree_indices), condition)  # update condition on used parts of subtree
                
                if not ok: i += 1; continue  # start over
                else: break
            
            if ok:
                indices = sorted(indices)  # final subtree indices
                for ids in indices:
                    t = self.__token_array_to_chunk(token_values[ids])
                    if t:
                        chunks.append(t)
            else:
                # if failed to meet the conditions, even when whole edges were deleted,
                for t in token_values:
                    if t: chunks.append(t)
        
        return chunks

            
    def __is_special_token(self, token: Token):
        """Check if a given spaCy token is a special character.

        token (Token): A spaCy token.

        RETURNS (bool): True if the token is a special character, False otherwise.
        """
        return (
            token.is_bracket
            or token.is_currency
            or token.is_left_punct
            or token.is_punct
            or token.is_quote
            or token.is_right_punct
            or token.is_space
        )
    
    def __token_array_to_chunk(self, token_array: np.ndarray):
        """Converts an array of spaCy tokens into a chunk string.

        token_array (np.ndarray): An array of spaCy tokens.

        RETURNS (str): Chunk string.
        """
        return ' '.join(token_array).replace("  ", ' ')


    def get_resource_name(self, lang_code, size_code):
        """Gets the spaCy model name based on language and size codes.

        lang_code (str): Language code.
            Refer to `SplitEngine.get_available_lang_codes()` for available language codes.
        size_code (str): Model size code.
            Refer to `SplitEngine.get_available_size_codes(lang_code)` for available size codes.

        RETURNS (str): SpaCy model name.
        """
        try:
            if lang_code in (): self.assert_lang_code(lang_code)
            model_code = _SUPPORTED_LANGUAGES[lang_code][size_code]
            return model_code
        except IndexError:
            self.assert_size_code(lang_code, size_code)
    
    def assert_lang_code(self, lang_code):
        """Asserts that the provided language code is valid.

        lang_code (str): Language code.

        RAISES (AssertionError): If the language code is not valid.
        """
        available_lang_codes = self.get_available_lang_codes()
        assert lang_code in available_lang_codes, \
            f"'{lang_code}' is not an available language code. " \
            "Refer to `SplitEngine.get_available_lang_codes()` for proper language codes."
    
    def assert_size_code(self, lang_code, size_code):
        """Asserts that the provided language code is valid.

        lang_code (str): Language code.
        size_code (str): Model size code.

        RAISES (AssertionError): If the size code is not valid for the language.
        """
        available_size_codes = self.get_available_size_codes(lang_code)
        assert size_code in available_size_codes, \
            f"'{size_code}' is not an available size code " \
            f"among the available size codes {available_size_codes} for '{lang_code}' language."

    @classmethod
    def get_available_lang_codes(cls):
        """Gets a list of available language codes.

        RETURNS (List[str]): List of available language codes.
        """
        return [ k for k, v in _SUPPORTED_LANGUAGES.items() if len(v)>0 ]
    
    @classmethod
    def get_available_size_codes(cls, lang_code):
        """Gets a list of available size codes for the given language.

        lang_code (str): Language code.

        RETURNS (List[str]): List of available size codes.
        """
        try: return [ k for k, _ in _SUPPORTED_LANGUAGES[lang_code].items() ]
        except: cls.assert_lang_code(lang_code)
    
    def assert_doc_loaded(self):
        """Asserts that a document is loaded into the engine.

        RAISES (AssertionError): If no document is loaded.
        """
        assert self.__document, \
            f"Document is not loaded into engine. " \
            "Please load some documents via `SplitEngine.load_document(text:str)`."
