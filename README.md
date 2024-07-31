# Keyfile Documentation
Keyfile is a method for defining a keyboard and how it will opperate.

There are three goals targeted in the creation of this format.
1. It must be clear to understand.
2. It must be easy to modify.
3. It must be as verbose as pure C.

## Tokens
All instructions will start with a token. The parser will read the lines in as though they belong to the last used token, until a line starts with a new token. This means, that a command can extend upon many lines, so long as the lines do not start with a token.

| Token   | Description                                           | Syntax                                           |
|---------|-------------------------------------------------------|--------------------------------------------------|
| INJECT  | Include external files or paths                       | `INJECT FILE`                                    |
| COLOR   | Define a color with the name and RGB values (0-255)   | `COLOR NAME R G B`                               |
| KEY     | Define a key with its name, key code, and color       | `KEY NAME KEY_CODE COLOR`                        |
| COMMENT | Add comments to your code                             | `COMMENT ANYTHING`                               |
| LAYER   | Define a layer with its name, layout macros, and keys | `LAYER NAME ROWS COLS ...KEYS`                   |
