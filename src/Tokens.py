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

    def __str__(self):
        pass

    def transpile(self):
        pass

class ColorToken(BaseToken):
    def __init__(self, name:str, r:int, g:int, b:int):
        super().__init__(
            name=name,
            key=Token.COLOR
        )
        self.r = r
        self.g = g
        self.b = b
    
    def __str__(self):
        return f"COLOR {self.name} {self.r} {self.g} {self.b}"

    def transpile(self):
        return f"{"{"}{self.r},{self.g},{self.b}{"}"}"

class KeyToken(BaseToken):
    def __init__(self, name:str, keycode:str, color:str):
        super().__init__(
            name=name,
            key=Token.KEY,
        )

        self.keycode = keycode
        self.color = color
    
    def __str__(self):
        return f"KEY {self.name} {self.keycode} {self.color}"
    
    def transpile(self):
        return f"{self.keycode}"
    
class DualKeyToken(BaseToken):
    

class LayerToken(BaseToken):
    def __init__(self, name:str, layout:str, keys:List[str]):
        super().__init__(
            key=Token.LAYER,
            name=name
        )

        self.layout = layout
        self.keys = keys

    def __str__(self):
        res = f"LAYER {self.name} {self.layout}"
        for key in self.keys:
            res += " " + key
        return res
    
    def transpile(self, TOKENS):
        keys = f"{self.layout}("
        colors = "{"

        for key in self.keys:
            key = TOKENS[key]
            color = TOKENS[key.color]
            keys += key.transpile() + ","
            colors += color.transpile() + ","

        colors = colors[:-1] + "}"
        keys = keys[:-1] + ")"

        return self.name, keys, colors