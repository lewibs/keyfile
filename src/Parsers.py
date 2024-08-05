from env import PATH
from Exceptions import ERROR_STACK, ParserException
import os

class Token:
    COMMENT="COMMENT"
    INJECT="INJECT"
    COLOR="COLOR"
    KEY="KEY"
    LAYER="LAYER"
    KEYBOARD="KEYBOARD"

class Words:
    TOKEN="token"
    COMMENT="comment"
    INITIALIZE="initialize"
    PATH="path"
    COLOR="color"
    UINT="uint"
    KEYCODE="keycode"
    COLOR_REF="color_ref"
    KEY_REF="key_ref"
    LAYER_REF="layer_ref"
    DECLARE_LAYER="declare_layer"
    KEY_MODIFIER="key_modifier"
    LAYER_MODIFIER="layer_modifier"
    MACRO="macro"

class GlobalDefinitions:
    KEYBOARD="keyboard"
    DUAL="DUAL"
    SKIP="SKIP"

SENTENCES = {}
SENTENCES_ARR = []
FILES = {}
KEY_MODIFIERS = {"LSFT", "RSFT", "LCTL", "RCTL", "LALT", "RALT"}
LAYER_MODIFIERS = {"MO", "TG", "TT"}

def parse_keyfile(path:str)->None:
    if path in FILES:
        return []

    try:
        with open(path, "r") as file:
            FILES[path] = file
            
            for line_number, line in enumerate(file, start=1):
                split_line = line.split()
                for token_number, item in enumerate(split_line):
                    if token_number == 0 and item in Sentences:
                        #HANDLE new line starting
                        SENTENCES_ARR.append(Sentences[item](item))
                    else:
                        #CONTINUE old line consumption
                        SENTENCES_ARR[-1].consume(item)

        return SENTENCES_ARR
    except FileNotFoundError as e:
        if PATH in path:
            raise ParserException(f"File Not Found: {path}")
        else:
            return parse_keyfile(os.path.join(PATH, "misc", path))
    except ParserException as e:
        ERROR_STACK.append(f"{line_number} | {line}")
        ERROR_STACK.append(f"{path}")
        raise e


def _declare(word:str, sentence_type):
    if word in SENTENCES:
        raise ParserException(f"Duplicate Declaration: '{word}' has already been declared")

    if not hasattr(Token, sentence_type):
        raise ParserException(f"Bad Token: {sentence_type} not a valid token")
    
    SENTENCES[word] = sentence_type
    
def _initialize(word:str, sentence):
    if word not in SENTENCES:
        raise ParserException(f"Not Defined: {word} is used before being declared")

    if SENTENCES[word] != sentence.type and SENTENCES[word].type != sentence.type:
        raise ParserException(f"Invalid Type: {sentence.type} is not {SENTENCES[word].type} for {word}")
    
    SENTENCES[word] = sentence

def _is_initialized(word:str, token:str):
    if word in SENTENCES:
        if isinstance(SENTENCES[word], str):
            return SENTENCES[word] == token
        else:
            return SENTENCES[word].type == token

def _is_keycode(word:str):
    if _is_initialized(word, Token.KEY):
        return True

    return word.startswith("KC_")

def _is_layer_modifier(word:str) -> bool:
    return word in LAYER_MODIFIERS

def _is_key_modifier(word:str) -> bool:
    return word in KEY_MODIFIERS

def _is_modifier(word: str) -> bool:
    return _is_key_modifier(word) or _is_layer_modifier(word)

class BaseSentence():
    def __init__(self, sentence_type, grammer):
        self.type = sentence_type
        self.grammer = grammer
        self.words = []

    def is_complete(self):
        if len(self.grammer) == 0:
            return True
        else:
            return False

    def consume(self, word:str):

        if self.is_complete():
            raise ParserException("Syntax Error: Expected new token")
        
        res = getattr(self, f"consume_{self.grammer.pop(0)}")(word)
        self.words.append(word)

        return res

    def consume_token(self, word:str):
        if self.type != word:
            raise ParserException("Syntax Error: Not a supported token")

    def consume_initialize(self, word:str):
        if word not in SENTENCES:
            _declare(word, self.type)
        _initialize(word, self)
    
    def consume_path(self, word:str):
        #This is an Exception because it will occur only when there is an issue with the parsing
        raise Exception("Usage Error: Path is supported for this sentence")
    
    def consume_color(self, word:str):
        if not (0 <= int(word) <= 255):
            raise ParserException("Value Error: Not a valid uint, must be between 0 to 255 (inclusive)")
        
    def consume_uint(self, word:str):
        if not (0 <= int(word)):
            raise ParserException("Value Error: Not a uint")

    def consume_ref(self, token_type:str, word:str):
        if token_type not in Token.__dict__.values():
            raise ParserException("Syntax Error: Not a supported token")

        if word not in SENTENCES:
            raise ParserException(f"Not Defined: {token_type} {word} is used before being declared")

    def consume_color_ref(self, word:str):
        self.consume_ref(Token.COLOR, word)

    def consume_key_ref(self, word:str):
        if not _is_keycode(word):
            self.consume_ref(Token.KEY, word)

    def consume_layer_ref(self, word:str):
        self.consume_ref(Token.LAYER, word)

    def consume_declare(self, sentence_type, word):
        _declare(word, sentence_type)

    def consume_declare_layer(self, word:str):
        self.consume_declare(Token.LAYER, word)

    def consume_keycode(self, word:str):
        if _is_modifier(word):
            if _is_key_modifier(word):
                self.grammer.insert(0, Words.KEY_REF)
                self.grammer.insert(0, Words.KEY_MODIFIER)
            elif _is_layer_modifier(word):
                self.grammer.insert(0, Words.LAYER_REF)


    def consume_key_modifier(self, word: str):
        if not _is_key_modifier(word):
            if _is_keycode(word):
                # Turns to nothing
                return
            raise ParserException(f"Syntax Error: {word} is not a valid KEY_MODIFIER")
        
        self.grammer.insert(0, Words.KEY_MODIFIER)
    
    def consume_layer_modifier(self, word:str):
        if not _is_layer_modifier(word):
            raise ParserException(f"Syntax Error: {word} is not a valid LAYER_MODIFIER")

    def consume_comment(self, word:str):
        self.grammer.append(Words.COMMENT)

    def consume_macro(self, word:str):
        return

class ColorSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.COLOR, [Words.TOKEN, Words.INITIALIZE, Words.COLOR, Words.COLOR, Words.COLOR])
        self.consume(token)

    def color(self):
        return "{" + ",".join(self.words[2:]) + "}"

class KeySentence(BaseSentence):
    _dual_keys = 0

    def __init__(self, token):
        super().__init__(Token.KEY, [Words.TOKEN, Words.INITIALIZE])
        # it will be trailed by either this
        # Words.MODIFIER, Words.KEYCODE, Words.COLOR_REF
        # or
        # Words.LAYER_REF Words.LAYER_REF Words.LAYER_REF
        self.consume(token)

    def consume_initialize(self, word: str):
        if word == GlobalDefinitions.DUAL:
            KeySentence._dual_keys += 1
            word = f"{GlobalDefinitions.DUAL}_{KeySentence._dual_keys}"
            self.grammer += [Words.LAYER_REF, Words.LAYER_REF, Words.LAYER_REF]
        else:
            self.grammer += [Words.KEYCODE, Words.COLOR_REF]

        super().consume_initialize(word)

    def name(self):
        return self.words[1]
    
    def layers(self):
        if not self.name().startswith(GlobalDefinitions.DUAL):
            raise ParserException("Usage error: trying to get layers on a normal key")
    
        return self.words[2:]

    def keycode(self):
        if self.name().startswith(GlobalDefinitions.DUAL):
            raise ParserException("Usage error: trying to get keycode on a dual key")
        
        code = self.words[-2]
        modifiers = self.words[2:-2]
        keycode = ""

        for modifier in modifiers:
            keycode+=f"{modifier}("
        
        #TODO
        if code in SENTENCES and SENTENCES[code].type == Token.KEY:
            keycode += SENTENCES[code].keycode()
        else:
            keycode += code

        for i in range(len(modifiers)):
            keycode+=")"

        return keycode


    def color(self):
        if self.name().startswith(GlobalDefinitions.DUAL):
            raise ParserException("Usage error: trying to get color on a dual key")
        
        return SENTENCES[self.words[-1]].color()

    # def translate_color(self):
    #     color = self.words[-1]
    #     return SENTENCES[color].words[-3:]

class LayerSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.LAYER, [Words.TOKEN, Words.INITIALIZE, Words.KEY_REF]) #...Words.KEY_REF

        if GlobalDefinitions.KEYBOARD not in SENTENCES:
            raise ParserException("Syntax Error: KEYBOARD must be initialized before LAYERS")

        self.consume(token)

    def consume_key_ref(self, word: str):
        self.grammer.append(Words.KEY_REF)
        super().consume_key_ref(word)

    def name(self):
        return self.words[1]

    def keys(self):
        return [SENTENCES[key_ref].keycode() for key_ref in self.words[2:]]

    def leds(self):
        leds = []
        for key_ref in self.words[2:]:
            if SENTENCES[key_ref].name() == GlobalDefinitions.SKIP:
                continue
            leds.append(SENTENCES[key_ref].color()) 
        return leds


class InjectSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.INJECT, [Words.TOKEN, Words.PATH])
        self.consume(token)
    
    def consume_path(self, word:str):
        parse_keyfile(word)

class CommentSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.COMMENT, [Words.TOKEN, Words.COMMENT])
        self.consume(token)

    def is_complete(self):
        return False

class KeyboardSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.KEYBOARD, [Words.TOKEN, Words.INITIALIZE, Words.MACRO, Words.MACRO, Words.MACRO, Words.MACRO, Words.DECLARE_LAYER]) #...Words.DECLARE_LAYER
        self.consume(token)
        self.consume(GlobalDefinitions.KEYBOARD)

    def rows(self):
        return self.words[3]

    def cols(self):
        return self.words[4]

    def leds(self):
        return self.words[5]

    def macro(self):
        return self.words[2] 
    
    def layers(self):
        return self.words[6:]

    def consume(self, word: str):
        res = super().consume(word)
        if self.is_complete():
            self.grammer.append(Words.DECLARE_LAYER)
        return res

Sentences={
    Token.COMMENT:CommentSentence,
    Token.INJECT:InjectSentence,
    Token.COLOR:ColorSentence,
    Token.KEY:KeySentence,
    Token.LAYER:LayerSentence,
    Token.KEYBOARD:KeyboardSentence
}
