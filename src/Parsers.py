from typing import Dict, List, Callable
from Tokens import Token, BaseToken, ColorToken, KeyToken, LayerToken
from env import PATH

TOKENS = {}
FILES = {}

# Define the type for functions in TOKEN_PARSERS
ParserFunction = Callable[[List[str]], List[BaseToken]]

def get_tokens_from_lines(lines:List[str], injected=True)->List[BaseToken]:
    tokens = []

    for line in lines:
        res = Token_Parsers.get(line[0])(line)
        for token in res:
            if token.name in TOKENS:
                raise Exception(f"{token.name} already defined")
            
            if injected == False:
                TOKENS[token.name] = token
            
            tokens.append(token)

    return tokens

def make_line_consumer()->Callable[[str],str|None]:
    FLUSH = "FLUSH"
    args = None

    def consume_line(line:str) -> List[str]|None:
        nonlocal args

        if line == FLUSH:
            return args
        
        ret = None
        line = line.split()
        
        if len(line) == 0:
            return ret

        if line[0] in Token.__members__:
            ret = args
            args = line
        else:
            ret = None
            args += line 

        return ret
    
    return consume_line, FLUSH

def get_lines_from_keyfile(path:str)->List[str]:
    consume_line, FLUSH = make_line_consumer()

    with open(path, "r") as file:
        lines = []
        for line in file:
            line = consume_line(line)
            if line:
                lines.append(line)
        
        #We have hit the end of the file but there is a line that needs to be flushed from consume line
        line = consume_line(FLUSH)
        if line:
            lines.append(line)

    return lines

def parse_INJECT(items:List[str])->List[BaseToken]:
    path = f"{PATH}/misc/{items[1]}"
    if path in FILES:
        return []
    else:
        FILES[path] = True
        lines = get_lines_from_keyfile(path)
        tokens = get_tokens_from_lines(lines)
        return tokens

def parse_COLOR(items:List[str])->List[ColorToken]:
    tokens = [ColorToken(
        name=items[1],
        r=items[2],
        g=items[3],
        b=items[4],
    )]
    return tokens

def parse_KEY(items:List[str])->List[BaseToken]:
    if items[3] not in TOKENS:
        raise Exception(f"COLOR {items[3]} not defined for KEY {items[1]}")

    tokens = [KeyToken(
        name=items[1],
        keycode=items[2],
        color=items[3],
    )]
    return tokens

def parse_LAYER(items:List[str])->List[BaseToken]:
    for key in items[3:]:
        if key not in TOKENS:
            raise Exception(f"KEY {key} not defined for LAYER {items[1]}")

    tokens = [
        LayerToken(
            name=items[1],
            layout=items[2],
            keys=items[3:]
        )
    ]
    return tokens

def parse_COMMENT(items:List[str])->List[BaseToken]:
    return []

# Create a dictionary mapping tokens to parsing functions
Token_Parsers: Dict[Token, ParserFunction] = {
    Token.INJECT.name: parse_INJECT,
    Token.COLOR.name: parse_COLOR,
    Token.KEY.name: parse_KEY,
    Token.LAYER.name: parse_LAYER,
    Token.COMMENT.name: parse_COMMENT,
}