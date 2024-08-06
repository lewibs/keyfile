# Keyfile Documentation
Keyfile is a DSL for defining a keyboard and how it will opperate.

This could directly compile to binary, however, that is more complicated then I want to deal with so it goes to C and then you can utilize QMK to compile it to binary.

There are three goals targeted in the creation of this format.
1. It must be clear to understand.
2. It must be easy to modify.
3. It must be as verbose as pure C and as easy to use as a GUI.

## Tokens

All instructions start with a token. The parser will read subsequent lines as belonging to the last used token until a new token is encountered. This allows commands to span multiple lines as long as they do not begin with a new token.

| Token       | Description                                            | Syntax                                        |
|-------------|--------------------------------------------------------|-----------------------------------------------|
| `INJECT`    | Includes external files or paths                       | `INJECT file_path`                            |
| `COLOR`     | Defines a color with the name and HSV values (0-255)   | `COLOR identifier number number number`       |
| `KEY`       | Defines a key with its name, key code, and color       | `KEY identifier modifier keycode color_ref`   |
| `KEY DUAL`  | Defines a dual key action using layer references       | `KEY DUAL layer_ref layer_ref layer_ref`      |
| `KEY SKIP`  | Indicates a key to be skipped if it does not exist     | `KEY SKIP` (Reserved, not to be initialized)  |
| `KEY TRANS` | Defines a transparent layer                            | `KEY TRANS` (Reserved, not to be initialized) |
| `KEY MACRO` | Defines a macro with a `SEND_STRING` call              | `KEY MACRO identifier string_ref color_ref`   |
| `STRING`    | Defines a string                                       | `STRING word+`                                |
| `COMMENT`   | Adds comments to the code                              | `COMMENT word+`                               |
| `LAYER`     | Defines a layer with its name, layout macros, and keys | `LAYER identifier key_ref+`                   |
| `KEYBOARD`  | Defines the keyboard configuration                     | `KEYBOARD macro macro macro macro layer_ref+` |

### Syntax Rules

- **Sentence**: A sequence of one of the following elements:
  ```ebnf
  sentence ::= (inject | comment | keyboard | key | string | color | layer)
  ```

- **Inject**: Includes an external file or path.
  ```ebnf
  inject ::= INJECT file_path
  ```

- **Keyboard**: Defines the keyboard configuration, including macros, rows, columns, LEDs, and layer names.
  ```ebnf
  keyboard ::= KEYBOARD macro macro macro layer_ref+
  ```

- **Key**: Defines different types of keys.
  ```ebnf
  key ::= KEY MACRO identifier string_ref color_ref
  key ::= KEY DUAL layer_ref layer_ref layer_ref
  key ::= KEY TRANS
  key ::= KEY SKIP
  key ::= KEY identifier modifier key_ref color_ref
  ```

- **String**: A string that is stored as a variable 
  ```ebnf
  string ::= STRING word+
  ```

- **Comment**: A string that is not read by the machine at runtime
  ```ebnf
  comment ::= COMMENT word+
  ```

- **Color**: A color in HSV
  ```ebnf
  color ::= COLOR identifier number number number
  ```

- **Layer**: A layer on the keyboard that can be accessed
  ```ebnf
  layer ::= LAYER identifier key_ref+
  ```

### Modifiers

- **Modifier**: Includes both key modifiers and layer modifiers.
  ```ebnf
  modifier ::= (key_modifier | layer_modifier)
  ```

- **Key Modifier**: A modifier that can be included onto a key such as Alt
  ```ebnf
  key_modifier ::= (LSFT | RSFT | LCTL | RCTL | LALT | RALT)*
  ```

- **Layer Modifier**: A modifier that will define how a layer is accessed
  ```ebnf
  layer_modifier ::= (MO | TG | TT)?
  ```

### Referances
- **Key Reference**: An identifier that is reffering to a key
  ```ebnf
  key_ref ::= (identifier | keycode)
  ```

- **String Reference**: An identifier that is reffering to a string 
  ```ebnf
  string_ref ::= identifier
  ```

- **Layer Reference**: An identifier that is reffering to a layer 
  ```ebnf
  layer_ref ::= identifier
  ```

- **Color Reference**: An identifier that is reffering to a color
  ```ebnf
  color_ref ::= identifier
  ```

- **File Path**: A path to a file on the machine
  ```ebnf
  file_path ::= non_whitespace
  ```

- **Identifier**: An identifier that is reffering to some saved variable
  ```ebnf
  identifier ::= non_whitespace
  ```

- **Key Code**: A code macro that is native to QMK 
  ```ebnf
  keycode ::= word
  ```

- **Macro**: A macro that is native to QMK 
  ```ebnf
  macro ::= word
  ```

- **Word**: A sequence of non-whitespace characters.
  ```ebnf
  word ::= (non_whitespace)+
  ```

- **Non-Whitespace**: Represents any character except whitespace.
  ```ebnf
  non_whitespace ::= ? [^\s]+ ?
  ```

- **Number**: Can be an integer or a floating-point number.
  ```ebnf
  number ::= integer | float
  ```

- **Integer**: A sequence of digits.
  ```ebnf
  integer ::= digit+
  ```

- **Float**: A sequence of digits with a decimal point.
  ```ebnf
  float ::= digit+ "." digit+
  ```

- **Digit**: Any single digit from 0 to 9.
  ```ebnf
  digit ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
  ```

## TODO
* set it up to run with QMK so it can make the .bin right away and delete the keymap files
* need to make config.h generate