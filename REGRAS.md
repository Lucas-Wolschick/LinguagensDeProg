# Regras léxicas analisadas — Java 20 × C

Fonte: [antlr/grammars-v4](https://github.com/antlr/grammars-v4) no commit `25ad11e4ff672b1eca69d6eeff109ce11bbb663d`

- Java 20: [`java/java20/Java20Lexer.g4`](https://github.com/antlr/grammars-v4/blob/25ad11e4ff672b1eca69d6eeff109ce11bbb663d/java/java20/Java20Lexer.g4) → cópia local `Java20Lexer.g4` (regras nas linhas 81–215)
- C: [`c/C.g4`](https://github.com/antlr/grammars-v4/blob/25ad11e4ff672b1eca69d6eeff109ce11bbb663d/c/C.g4) → cópia local `C.g4` (regras nas linhas 899–1081)

Regras escolhidas: **TEXTO** (string), **INTEIRO** e **REAL** (ponto flutuante).

> As observações marcadas com **[confirmado]** foram deduzidas lendo a gramática e
> depois confirmadas rodando o ANTLR 4.13.2 (ver `ENTRADAS.md` e `testes/resultado.txt`).

---

## 1. TEXTO

### C — `StringLiteral`

```antlr
StringLiteral
    : EncodingPrefix? '"' SCharSequence? '"'
    ;

fragment EncodingPrefix
    : 'u8'
    | 'u'
    | 'U'
    | 'L'
    ;

fragment SCharSequence
    : SChar+
    ;

fragment SChar
    : ~["\\\r\n]
    | EscapeSequence
    | '\\\n'   // Added line
    | '\\\r\n' // Added line
    ;

fragment EscapeSequence
    : SimpleEscapeSequence
    | OctalEscapeSequence
    | HexadecimalEscapeSequence
    | UniversalCharacterName
    ;

fragment SimpleEscapeSequence
    : '\\' ['"?abfnrtv\\]
    ;

fragment OctalEscapeSequence
    : '\\' OctalDigit OctalDigit? OctalDigit?
    ;

fragment HexadecimalEscapeSequence
    : '\\x' HexadecimalDigit+
    ;

fragment UniversalCharacterName
    : '\\u' HexQuad
    | '\\U' HexQuad HexQuad
    ;

fragment HexQuad
    : HexadecimalDigit HexadecimalDigit HexadecimalDigit HexadecimalDigit
    ;
```

### Java — `StringLiteral` e `TextBlock`

```antlr
StringLiteral: '"' StringCharacters? '"';

fragment StringCharacters: StringCharacter+;

fragment StringCharacter: ~["\\\r\n] | EscapeSequence;

TextBlock: '"""' [ \t]* [\n\r] [.\r\b]* '"""';

fragment EscapeSequence:
    '\\' [btnfr"'\\]
    | OctalEscape
    | UnicodeEscape // This is not in the spec but prevents having to preprocess the input
;

fragment OctalEscape:
    '\\' OctalDigit
    | '\\' OctalDigit OctalDigit
    | '\\' ZeroToThree OctalDigit OctalDigit
;

fragment ZeroToThree: [0-3];

fragment UnicodeEscape: '\\' 'u'+ HexDigit HexDigit HexDigit HexDigit;
```

### Observações

- **Prefixos:** C aceita `u8`, `u`, `U` e `L` antes das aspas (`u8"Olá"`); Java não tem prefixos.
- **Continuação de linha:** em C, `\` seguido de quebra de linha é aceito dentro da string (linhas "Added line"); em Java não.
- **Escapes:** C tem `\a`, `\v`, `\?` e `\xHH…` (hex com quantos dígitos quiser), além de `\uXXXX`/`\UXXXXXXXX`. Java tem `\b \t \n \f \r \" \' \\`, octal até `\377` e `\uXXXX` com um ou mais `u` (`\uuu0041`).
- **Escape `\s` ausente em Java:** o Java 15+ aceita `\s` (espaço), mas a gramática não o inclui → `"a\sb"` deve falhar **[confirmado — ver ENTRADAS.md]**.
- **Bug no `TextBlock`:** `[.\r\b]*` é um *conjunto de caracteres*, ou seja, aceita apenas `.`, CR e backspace literais, e não "qualquer caractere". Um text block real como
  ```
  """
      Olá mundo
      """
  ```
  não deve ser reconhecido como `TextBlock` **[confirmado — ver ENTRADAS.md]**. Ótimo exemplo de entrada "rejeitada" e de discussão no relatório.
- **Raw strings `R"..."`** são do C++, não do C; a gramática de C corretamente não as tem (o rascunho antigo no CHANGELOG mencionava isso por engano).

---

## 2. INTEIRO

### C — `Constant` → `IntegerConstant`

> Em C, `IntegerConstant` é **fragment**: o token que aparece na saída do ANTLR é `Constant`
> (o mesmo token usado para reais e caracteres).

```antlr
Constant
    : IntegerConstant
    | FloatingConstant
    //|   EnumerationConstant
    | CharacterConstant
    ;

fragment IntegerConstant
    : DecimalConstant IntegerSuffix?
    | OctalConstant IntegerSuffix?
    | HexadecimalConstant IntegerSuffix?
    | BinaryConstant
    ;

fragment BinaryConstant
    : '0' [bB] [0-1]+
    ;

fragment DecimalConstant
    : NonzeroDigit Digit*
    ;

fragment OctalConstant
    : '0' OctalDigit*
    ;

fragment HexadecimalConstant
    : HexadecimalPrefix HexadecimalDigit+
    ;

fragment HexadecimalPrefix
    : '0' [xX]
    ;

fragment NonzeroDigit
    : [1-9]
    ;

fragment Digit
    : [0-9]
    ;

fragment OctalDigit
    : [0-7]
    ;

fragment HexadecimalDigit
    : [0-9a-fA-F]
    ;

fragment IntegerSuffix
    : UnsignedSuffix LongSuffix?
    | UnsignedSuffix LongLongSuffix
    | LongSuffix UnsignedSuffix?
    | LongLongSuffix UnsignedSuffix?
    ;

fragment UnsignedSuffix
    : [uU]
    ;

fragment LongSuffix
    : [lL]
    ;

fragment LongLongSuffix
    : 'll'
    | 'LL'
    ;

// Token NÃO-fragment, definido depois de Constant — interfere nos inteiros:
DigitSequence
    : Digit+
    ;
```

### Java — `IntegerLiteral`

```antlr
IntegerLiteral:
    DecimalIntegerLiteral
    | HexIntegerLiteral
    | OctalIntegerLiteral
    | BinaryIntegerLiteral
;

fragment DecimalIntegerLiteral: DecimalNumeral IntegerTypeSuffix?;

fragment HexIntegerLiteral: HexNumeral IntegerTypeSuffix?;

fragment OctalIntegerLiteral: OctalNumeral IntegerTypeSuffix?;

fragment BinaryIntegerLiteral: BinaryNumeral IntegerTypeSuffix?;

fragment IntegerTypeSuffix: [lL];

fragment DecimalNumeral: '0' | NonZeroDigit (Digits? | Underscores Digits);

fragment Digits: Digit (DigitsAndUnderscores? Digit)?;

fragment Digit: '0' | NonZeroDigit;

fragment NonZeroDigit: [1-9];

fragment DigitsAndUnderscores: DigitOrUnderscore+;

fragment DigitOrUnderscore: Digit | '_';

fragment Underscores: '_'+;

fragment HexNumeral: '0' [xX] HexDigits;

fragment HexDigits: HexDigit (HexDigitsAndUnderscores? HexDigit)?;

fragment HexDigit: [0-9a-fA-F];

fragment HexDigitsAndUnderscores: HexDigitOrUnderscore+;

fragment HexDigitOrUnderscore: HexDigit | '_';

fragment OctalNumeral: '0' Underscores? OctalDigits;

fragment OctalDigits: OctalDigit (OctalDigitsAndUnderscores? OctalDigit)?;

fragment OctalDigit: [0-7];

fragment OctalDigitsAndUnderscores: OctalDigitOrUnderscore+;

fragment OctalDigitOrUnderscore: OctalDigit | '_';

fragment BinaryNumeral: '0' [bB] BinaryDigits;

fragment BinaryDigits: BinaryDigit (BinaryDigitsAndUnderscores? BinaryDigit)?;

fragment BinaryDigit: [01];

fragment BinaryDigitsAndUnderscores: BinaryDigitOrUnderscore+;

fragment BinaryDigitOrUnderscore: BinaryDigit | '_';
```

### Observações

- **Separador de dígitos:** Java aceita `_` entre dígitos (`1_000_000`, `0xFF_FF`, `0b1010_0101`), nunca no início/fim; C não tem separador (o `'` do C23 não está na gramática).
- **Sufixos:** C tem `u`/`U`, `l`/`L`, `ll`/`LL` e combinações (`100ULL`, `42lu`); `lL` misturado não vale. Java só tem `l`/`L`.
- **Binário em C não aceita sufixo:** `BinaryConstant` não tem `IntegerSuffix?` → `0b1010u` deve virar `Constant(0b1010)` + `Identifier(u)` **[confirmado — ver ENTRADAS.md]**.
- **Token único em C:** inteiros e reais saem como `Constant`; em Java saem como `IntegerLiteral` ou `FloatingPointLiteral`. Isso muda bastante a "documentação dos resultados do ANTLR4".
- **`DigitSequence` em C (efeito da regra do maior casamento):** para `01289`, `Constant` só casa `012` (octal), mas `DigitSequence` casa os 5 caracteres → o ANTLR deve emitir **`DigitSequence`**, e não erro **[confirmado — ver ENTRADAS.md]**. Para `12345` os dois casam o mesmo tamanho e vence `Constant` (definido antes).
- **Mesmo caso em Java:** `01289` → `OctalNumeral` casa `012`, e não há regra equivalente a `DigitSequence` → deve virar `IntegerLiteral(012)` + `IntegerLiteral(89)` **[confirmado — ver ENTRADAS.md]**.
- **O lexer não "rejeita", ele divide:** `123abc` vira número + identificador nos dois lexers. Erro de token só aparece quando nenhum token casa o caractere.

---

## 3. REAL

### C — `Constant` → `FloatingConstant`

```antlr
fragment FloatingConstant
    : DecimalFloatingConstant
    | HexadecimalFloatingConstant
    ;

fragment DecimalFloatingConstant
    : FractionalConstant ExponentPart? FloatingSuffix?
    | DigitSequence ExponentPart FloatingSuffix?
    ;

fragment HexadecimalFloatingConstant
    : HexadecimalPrefix (HexadecimalFractionalConstant | HexadecimalDigitSequence) BinaryExponentPart FloatingSuffix?
    ;

fragment FractionalConstant
    : DigitSequence? '.' DigitSequence
    | DigitSequence '.'
    ;

fragment ExponentPart
    : [eE] Sign? DigitSequence
    ;

fragment Sign
    : [+-]
    ;

DigitSequence
    : Digit+
    ;

fragment HexadecimalFractionalConstant
    : HexadecimalDigitSequence? '.' HexadecimalDigitSequence
    | HexadecimalDigitSequence '.'
    ;

fragment BinaryExponentPart
    : [pP] Sign? DigitSequence
    ;

fragment HexadecimalDigitSequence
    : HexadecimalDigit+
    ;

fragment FloatingSuffix
    : [flFL]
    ;
```

### Java — `FloatingPointLiteral`

```antlr
FloatingPointLiteral: DecimalFloatingPointLiteral | HexadecimalFloatingPointLiteral;

fragment DecimalFloatingPointLiteral:
    Digits '.' Digits? ExponentPart? FloatTypeSuffix?
    | '.' Digits ExponentPart? FloatTypeSuffix?
    | Digits ExponentPart FloatTypeSuffix?
    | Digits FloatTypeSuffix
;

fragment ExponentPart: ExponentIndicator SignedInteger;

fragment ExponentIndicator: [eE];

fragment SignedInteger: Sign? Digits;

fragment Sign: [+-];

fragment FloatTypeSuffix: [fFdD];

fragment HexadecimalFloatingPointLiteral: HexSignificand BinaryExponent FloatTypeSuffix?;

fragment HexSignificand: HexNumeral '.'? | '0' [xX] HexDigits? '.' HexDigits;

fragment BinaryExponent: BinaryExponentIndicator SignedInteger;

fragment BinaryExponentIndicator: [pP];
```

### Observações

- **Estrutura quase idêntica:** as duas aceitam `12.5`, `.5`, `12.`, `1e10`, `6.02e+23` e hexadecimal com expoente binário obrigatório (`0x1.8p3`).
- **Sufixos diferentes:** C usa `f`/`F` (float) e `l`/`L` (long double); Java usa `f`/`F` e `d`/`D` (double). `3.14L` é real em C, mas em Java deve virar `FloatingPointLiteral(3.14)` + `Identifier(L)` **[confirmado — ver ENTRADAS.md]**.
- **Inteiro com sufixo vira real só em Java:** `Digits FloatTypeSuffix` → `1000f` e `1000d` são `FloatingPointLiteral`; em C, `1000f` deve virar `Constant(1000)` + `Identifier(f)` **[confirmado — ver ENTRADAS.md]**.
- **Underscore:** Java aceita `10_000.000_1` (o `Digits` permite `_`); em C, a mesma entrada se quebra em vários tokens **[confirmado — ver ENTRADAS.md]**. É exatamente o tipo de exemplo que o enunciado pede ("reconheça 10_000.00 em vez de 1").
- **Expoente incompleto:** `1.5e` → em ambos deve virar real `1.5` + identificador `e` **[confirmado — ver ENTRADAS.md]**.
- **Hex float sem `p`:** `0x1.8F` não é reconhecido como real nos dois lexers: vira `0x1` + `.8F` (inteiro hex + real) **[confirmado — ver ENTRADAS.md]**.
