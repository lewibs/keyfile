from enum import Enum
from typing import List

class Token(Enum):
    COMMENT="COMMENT",
    INJECT="INJECT",
    COLOR="COLOR",
    KEY="KEY",
    LAYER="LAYER",

class BaseToken():
    def __init__(self, key:Token, name:str):
        self.key = key
        self.name = name
        self.val = None

class ColorToken(BaseToken):
    def __init__(self, name:str, r:int, g:int, b:int):
        super().__init__(
            name=name,
            key=Token.COLOR
        )
        self.r = r
        self.g = g
        self.b = b

class KeyToken(BaseToken):
    def __init__(self, name:str, keycode:str, color:str):
        super().__init__(
            name=name,
            key=Token.KEY,
        )

        self.keycode = keycode
        self.color = color

class LayerToken(BaseToken):
    def __init__(self, name:str, layout:str, keys:List[str]):
        super().__init__(
            key=Token.LAYER,
            name=name
        )

        self.layout = layout
        self.keys = keys