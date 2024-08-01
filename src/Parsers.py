from env import PATH
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
    DECLARE_LAYER="declare_layer"

class GlobalDefinitions:
    KEYBOARD="keyboard"

SENTENCES = {}
FILES = {}

def parse_keyfile(path:str)->None:
    if path in FILES:
        return

    try:
        with open(path, "r") as file:
            FILES[path] = file
            sentence = None
            
            for line_number, line in enumerate(file, start=1):
                line = line.split()
                for token_number, item in enumerate(line):
                    if token_number == 0 and item in Sentences:
                        #HANDLE new line starting
                        sentence = Sentences[item](item)
                    else:
                        #CONTINUE old line consumption
                        sentence.consume(item)
    except FileNotFoundError as e:
        if PATH in path:
            raise e
        else:
            parse_keyfile(os.path.join(PATH, "misc", path))


def _declare(word:str, sentence_type):
    if word in SENTENCES:
        raise Exception(f"ERROR: {word} already declared")

    if not hasattr(Token, sentence_type):
        print(sentence_type)
        raise Exception(f"ERROR: {sentence_type} not a valid sentence")
    
    SENTENCES[word] = sentence_type
    
def _initialize(word:str, sentence):
    if word not in SENTENCES:
        raise Exception(f"ERROR: {word} not yet declared")

    if SENTENCES[word] != sentence.type and SENTENCES[word].type != sentence.type:
        raise Exception(f"ERROR: {sentence.type} is not {SENTENCES[word].type} for {word}")
    
    SENTENCES[word] = sentence

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

    def consume(self, word:str)->None:
        if self.is_complete():
            raise Exception("ERROR: expected new token")
        
        getattr(self, f"consume_{self.grammer.pop(0)}")(word)
        self.words.append(word)

    def consume_token(self, word:str):
        if self.type != word:
            raise Exception("ERROR: not a valid token")

    def consume_initialize(self, word:str):
        if word not in SENTENCES:
            _declare(word, self.type)
        _initialize(word, self)
    
    def consume_path(self, word:str):
        raise Exception("ERROR: path not supported for this sentence")
    
    def consume_color(self, word:str):
        if not (0 <= int(word) <= 255):
            raise Exception("ERROR: not a valid color")
        
    def consume_uint(self, word:str):
        if not (0 <= int(word)):
            raise Exception("ERROR: not a valid uint")

    def consume_ref(self, token_type:str, word:str):
        if word not in SENTENCES:
            raise Exception(f"ERROR: {token_type} {word} not defined")
        
        if word in SENTENCES and not isinstance(SENTENCES[word], Sentences[token_type]):
            raise Exception(f'ERROR: {word} is not a {token_type}')

    def consume_color_ref(self, word:str):
        self.consume_ref(Token.COLOR, word)

    def consume_key_ref(self, word:str):
        self.consume_ref(Token.KEY, word)

    def consume_declare(self, sentence_type, word):
        _declare(word, sentence_type)

    def consume_declare_layer(self, word:str):
        self.consume_declare(Token.LAYER, word)

    def consume_keycode(self, word:str):
        #TODO
        pass

    def consume_comment(self, word:str):
        self.grammer.append(Words.COMMENT)

class ColorSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.COLOR, [Words.TOKEN, Words.INITIALIZE, Words.COLOR, Words.COLOR, Words.COLOR])
        self.consume(token)

class KeySentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.KEY, [Words.TOKEN, Words.INITIALIZE, Words.KEYCODE, Words.COLOR_REF])
        self.consume(token)

class LayerSentence(BaseSentence):
    def __init__(self, token):
        super().__init__(Token.LAYER, [Words.TOKEN, Words.INITIALIZE]) #...Words.KEY_REF

        if GlobalDefinitions.KEYBOARD not in SENTENCES:
            raise Exception("ERROR: KEYBOARD must be defined before LAYERS")

        keyboard_token = SENTENCES[GlobalDefinitions.KEYBOARD]

        for i in range(keyboard_token.rows() * keyboard_token.cols()):
            self.grammer.append(Words.KEY_REF)

        self.consume(token)

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
        super().__init__(Token.KEYBOARD, [Words.TOKEN, Words.INITIALIZE, Words.UINT, Words.UINT, Words.DECLARE_LAYER]) #...Words.DECLARE_LAYER
        self.consume(token)
        self.consume(GlobalDefinitions.KEYBOARD)

    def rows(self):
        return int(self.words[2])

    def cols(self):
        return int(self.words[3])

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
