import os
import copy
import importlib

from typing import Tuple

SO_LIB_PATH = os.environ.get("SO_LIB_PATH", "rwkv")

CPP_LIB = importlib.import_module(SO_LIB_PATH)

class ModelWrapper:

    def __init__(
            self, 
            *,
            model_path: str,
            so_lib_name="rwkv",
            ):

        self.cpp_instance = CPP_LIB.initRwkv()

        CPP_LIB.loadModel(self.cpp_instance, model_path)
        self.init_output()
        self.init_state()


    def init_output(self):
        return CPP_LIB.initOutput(self.cpp_instance)

    def init_state(self, tokens: Tuple[int] = ()):
        CPP_LIB.initState(self.cpp_instance)
        for token in tokens:
            self.forward(token)

    def sample(self):
        return CPP_LIB.typicalSample(self.cpp_instance)


    def forward(self, token: int):
        CPP_LIB.modelForward(self.cpp_instance, token)
        
        return (
                CPP_LIB.getOutput(self.cpp_instance), 
                CPP_LIB.getState(self.cpp_instance)
                )
     

class TokenizerWrapper:

    def __init__(self, *, vocab_path: str, merges_path: str):
        self.tokenizer_instance = CPP_LIB.initTokenizer(vocab_path, merges_path)


    def encode(self, string: str):
        return CPP_LIB.tokenizerEncode(self.tokenizer_instance, string)


    def decode(self, token: int):
        return CPP_LIB.tokenizerDecode(self.tokenizer_instance, token)


