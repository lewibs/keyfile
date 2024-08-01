# Keyfile Documentation
Keyfile is a DSL for defining a keyboard and how it will opperate.

There are three goals targeted in the creation of this format.
1. It must be clear to understand.
2. It must be easy to modify.
3. It must be as verbose as pure C and as easy to use as a GUI.

## Tokens
All instructions will start with a token. The parser will read the lines in as though they belong to the last used token, until a line starts with a new token. This means, that a command can extend upon many lines, so long as the lines do not start with a token.

| Token    | Description                                           | Syntax                                           |
|----------|-------------------------------------------------------|--------------------------------------------------|
| INJECT   | Include external files or paths                       | `INJECT FILE`                                    |
| COLOR    | Define a color with the name and RGB values (0-255)   | `COLOR NAME R G B`                               |
| KEY      | Define a key with its name, key code, and color       | `KEY NAME ...MODIFYER KEY_CODE COLOR`            |
| COMMENT  | Add comments to your code                             | `COMMENT ANYTHING`                               |
| LAYER    | Define a layer with its name, layout macros, and keys | `LAYER NAME ...KEY`                              |
| KEYBOARD | Defines the keyboard that will be created             | `KEYBOARD ROWS COLS ...LAYER`                    |

## Grammar


## TODO
todo
set it up to run with QMK so it can make the .bin right away and delete the keymap files

update readme

remove hardcoded IDX values from transpiler and have the sentenes output them. since you have tokens from picking them up just make rules for converting them to c and them make a translate function

add skip modifier for keys to skip color?

NUMBER_OF_LED_LIGHTS

add error checkign for C_code things where it looks at things like declared sicze and checks if that is correct 

doing
make transpiler

