# Saídas reais do ANTLR4

ANTLR 4.13.2; 46 casos, duas execuções por caso.

Gerado por `python tools/run_tests.py`. Entradas e textos usam a notação JSON: `\n` é uma quebra de linha; `\\n` é barra seguida de n.

Aceita = um único token da regra isolada cobrindo toda a entrada, sem erros, seguido de EOF. Todos os tokens, inclusive ocultos, entram na verificação.

O lexer completo de C emite `Constant` tanto para inteiro quanto para real. A sonda isolada distingue os fragmentos. Não se executa parser.

## C01 — C / StringLiteral

Entrada: `"u8\"Olá, mundo!\""` · **Aceita** · principal

Prefixo u8 permitido antes das aspas.

**Lexer completo:** `StringLiteral` `"u8\"Olá, mundo!\""` [0..14; canal 0]; `EOF` `"<EOF>"` [15..14; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"u8\"Olá, mundo!\""` [0..14; canal 0]; `EOF` `"<EOF>"` [15..14; canal 0]

Erros: nenhum


## C02 — C / StringLiteral

Entrada: `"\"linha\\x41\""` · **Aceita** · principal

Escape hexadecimal com um ou mais dígitos hexadecimais.

**Lexer completo:** `StringLiteral` `"\"linha\\x41\""` [0..10; canal 0]; `EOF` `"<EOF>"` [11..10; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"linha\\x41\""` [0..10; canal 0]; `EOF` `"<EOF>"` [11..10; canal 0]

Erros: nenhum


## C03 — C / StringLiteral

Entrada: `"\"texto\\q\""` · **Rejeitada** · principal

Não existe escape \q: o lexer informa erro léxico.

**Lexer completo:** `EOF` `"<EOF>"` [9..8; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"texto\\q'"`
- linha 1, coluna 8: `"token recognition error at: '\"'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [9..8; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"texto\\q'"`
- linha 1, coluna 8: `"token recognition error at: '\"'"`

## C04 — C / StringLiteral

Entrada: `"\"sem fechamento"` · **Rejeitada** · principal

Falta a aspa final: nenhum literal completo.

**Lexer completo:** `EOF` `"<EOF>"` [15..14; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"sem fechamento'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [15..14; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"sem fechamento'"`

## J05 — Java / StringLiteral

Entrada: `"\"Olá\\nmundo\""` · **Aceita** · principal

A sequência barra+n é um escape permitido, não uma quebra física de linha.

**Lexer completo:** `StringLiteral` `"\"Olá\\nmundo\""` [0..11; canal 0]; `EOF` `"<EOF>"` [12..11; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"Olá\\nmundo\""` [0..11; canal 0]; `EOF` `"<EOF>"` [12..11; canal 0]

Erros: nenhum


## J06 — Java / StringLiteral

Entrada: `"\"valor\\u0041\""` · **Aceita** · principal

A gramática inclui UnicodeEscape no próprio lexer.

**Lexer completo:** `StringLiteral` `"\"valor\\u0041\""` [0..12; canal 0]; `EOF` `"<EOF>"` [13..12; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"valor\\u0041\""` [0..12; canal 0]; `EOF` `"<EOF>"` [13..12; canal 0]

Erros: nenhum


## J07 — Java / StringLiteral

Entrada: `"u8\"texto\""` · **Rejeitada** · principal

O prefixo vira Identifier e o restante StringLiteral; não há um único literal.

**Lexer completo:** `Identifier` `"u8"` [0..1; canal 0]; `StringLiteral` `"\"texto\""` [2..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"texto\""` [2..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: 'u'"`
- linha 1, coluna 1: `"token recognition error at: '8'"`

## J08 — Java / StringLiteral

Entrada: `"\"texto\\x41\""` · **Rejeitada** · principal

Escape hexadecimal \x não é alternativa desta regra Java.

**Lexer completo:** `IntegerLiteral` `"41"` [8..9; canal 0]; `EOF` `"<EOF>"` [11..10; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"texto\\x'"`
- linha 1, coluna 10: `"token recognition error at: '\"'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [11..10; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"texto\\x'"`
- linha 1, coluna 8: `"token recognition error at: '4'"`
- linha 1, coluna 9: `"token recognition error at: '1'"`
- linha 1, coluna 10: `"token recognition error at: '\"'"`

## C09 — C / IntegerConstant

Entrada: `"0xCAFEuLL"` · **Aceita** · principal

Inteiro hexadecimal com sufixo unsigned long long.

**Lexer completo:** `Constant` `"0xCAFEuLL"` [0..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0xCAFEuLL"` [0..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


## C10 — C / IntegerConstant

Entrada: `"0b101101"` · **Aceita** · principal

Esta versão do lexer C inclui explicitamente BinaryConstant.

**Lexer completo:** `Constant` `"0b101101"` [0..7; canal 0]; `EOF` `"<EOF>"` [8..7; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0b101101"` [0..7; canal 0]; `EOF` `"<EOF>"` [8..7; canal 0]

Erros: nenhum


## C11 — C / IntegerConstant

Entrada: `"10_000"` · **Rejeitada** · principal

Sublinhado não pertence aos numerais desta gramática C.

**Lexer completo:** `Constant` `"10"` [0..1; canal 0]; `Identifier` `"_000"` [2..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"10"` [0..1; canal 0]; `Selected` `"000"` [3..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 2: `"token recognition error at: '_'"`

## C12 — C / IntegerConstant

Entrada: `"12345lL"` · **Rejeitada** · principal

LongLongSuffix admite ll ou LL, não a mistura lL.

**Lexer completo:** `Constant` `"12345l"` [0..5; canal 0]; `Identifier` `"L"` [6..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345l"` [0..5; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros:

- linha 1, coluna 6: `"token recognition error at: 'L'"`

## J13 — Java / IntegerLiteral

Entrada: `"10_000L"` · **Aceita** · principal

Separador interno entre dígitos e sufixo long.

**Lexer completo:** `IntegerLiteral` `"10_000L"` [0..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"10_000L"` [0..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros: nenhum


## J14 — Java / IntegerLiteral

Entrada: `"0b1010_0101"` · **Aceita** · principal

Base binária com separador interno.

**Lexer completo:** `IntegerLiteral` `"0b1010_0101"` [0..10; canal 0]; `EOF` `"<EOF>"` [11..10; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0b1010_0101"` [0..10; canal 0]; `EOF` `"<EOF>"` [11..10; canal 0]

Erros: nenhum


## J15 — Java / IntegerLiteral

Entrada: `"12345UL"` · **Rejeitada** · principal

Java não possui sufixo unsigned; UL vira Identifier.

**Lexer completo:** `IntegerLiteral` `"12345"` [0..4; canal 0]; `Identifier` `"UL"` [5..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345"` [0..4; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros:

- linha 1, coluna 5: `"token recognition error at: 'U'"`
- linha 1, coluna 6: `"token recognition error at: 'L'"`

## J16 — Java / IntegerLiteral

Entrada: `"01289"` · **Rejeitada** · principal

O prefixo octal 012 e o decimal 89 viram tokens separados.

**Lexer completo:** `IntegerLiteral` `"012"` [0..2; canal 0]; `IntegerLiteral` `"89"` [3..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"012"` [0..2; canal 0]; `Selected` `"89"` [3..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


## C17 — C / FloatingConstant

Entrada: `"12.50e-03L"` · **Aceita** · principal

Fração decimal, expoente com sinal e sufixo long double.

**Lexer completo:** `Constant` `"12.50e-03L"` [0..9; canal 0]; `EOF` `"<EOF>"` [10..9; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12.50e-03L"` [0..9; canal 0]; `EOF` `"<EOF>"` [10..9; canal 0]

Erros: nenhum


## C18 — C / FloatingConstant

Entrada: `"0x1.Ap+4f"` · **Aceita** · principal

Real hexadecimal exige expoente binário p/P; aceita sufixo f.

**Lexer completo:** `Constant` `"0x1.Ap+4f"` [0..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0x1.Ap+4f"` [0..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


## C19 — C / FloatingConstant

Entrada: `"10_000.50"` · **Rejeitada** · principal

Sublinhado divide a entrada em Constant, Identifier e Constant.

**Lexer completo:** `Constant` `"10"` [0..1; canal 0]; `Identifier` `"_000"` [2..5; canal 0]; `Constant` `".50"` [6..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"000.50"` [3..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '10_'"`

## C20 — C / FloatingConstant

Entrada: `"12.5e+"` · **Rejeitada** · principal

O expoente precisa de dígitos após o sinal; a entrada é tokenizada em partes.

**Lexer completo:** `Constant` `"12.5"` [0..3; canal 0]; `Identifier` `"e"` [4..4; canal 0]; `Plus` `"+"` [5..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12.5"` [0..3; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 4: `"token recognition error at: 'e'"`
- linha 1, coluna 5: `"token recognition error at: '+'"`

## J21 — Java / FloatingPointLiteral

Entrada: `"10_000.50D"` · **Aceita** · principal

Separador interno e sufixo double aceitos.

**Lexer completo:** `FloatingPointLiteral` `"10_000.50D"` [0..9; canal 0]; `EOF` `"<EOF>"` [10..9; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"10_000.50D"` [0..9; canal 0]; `EOF` `"<EOF>"` [10..9; canal 0]

Erros: nenhum


## J22 — Java / FloatingPointLiteral

Entrada: `"0x1.Ap+4f"` · **Aceita** · principal

Mesma estrutura hexadecimal de C neste exemplo.

**Lexer completo:** `FloatingPointLiteral` `"0x1.Ap+4f"` [0..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0x1.Ap+4f"` [0..8; canal 0]; `EOF` `"<EOF>"` [9..8; canal 0]

Erros: nenhum


## J23 — Java / FloatingPointLiteral

Entrada: `"12.50L"` · **Rejeitada** · principal

L é sufixo inteiro, não sufixo de ponto flutuante Java.

**Lexer completo:** `FloatingPointLiteral` `"12.50"` [0..4; canal 0]; `Identifier` `"L"` [5..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12.50"` [0..4; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 5: `"token recognition error at: 'L'"`

## J24 — Java / FloatingPointLiteral

Entrada: `"0x1.8"` · **Rejeitada** · principal

Falta o expoente binário obrigatório p/P.

**Lexer completo:** `IntegerLiteral` `"0x1"` [0..2; canal 0]; `FloatingPointLiteral` `".8"` [3..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `EOF` `"<EOF>"` [5..4; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '0x1.8'"`

## C25 — C / IntegerConstant

Entrada: `"01289"` · **Rejeitada** · complementar

DigitSequence pode consumir todos os dígitos, mas isso não comprova IntegerConstant.

**Lexer completo:** `DigitSequence` `"01289"` [0..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"012"` [0..2; canal 0]; `Selected` `"89"` [3..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


## C26 — C / IntegerConstant

Entrada: `"0b1010L"` · **Rejeitada** · complementar

BinaryConstant não tem IntegerSuffix nesta versão.

**Lexer completo:** `Constant` `"0b1010"` [0..5; canal 0]; `Identifier` `"L"` [6..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0b1010"` [0..5; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros:

- linha 1, coluna 6: `"token recognition error at: 'L'"`

## C27 — C / FloatingConstant

Entrada: `"12345f"` · **Rejeitada** · complementar

Em C, apenas dígitos e f não bastam para formar real.

**Lexer completo:** `Constant` `"12345"` [0..4; canal 0]; `Identifier` `"f"` [5..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '12345f'"`

## J28 — Java / FloatingPointLiteral

Entrada: `"12345f"` · **Aceita** · complementar

Java admite Digits FloatTypeSuffix, sem ponto ou expoente.

**Lexer completo:** `FloatingPointLiteral` `"12345f"` [0..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345f"` [0..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


## C29 — C / IntegerConstant

Entrada: `"12345.0"` · **Rejeitada** · complementar

Constant único pode ser real; a sonda do fragmento inteiro rejeita.

**Lexer completo:** `Constant` `"12345.0"` [0..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345"` [0..4; canal 0]; `Selected` `"0"` [6..6; canal 0]; `EOF` `"<EOF>"` [7..6; canal 0]

Erros:

- linha 1, coluna 5: `"token recognition error at: '.'"`

## C30 — C / FloatingConstant

Entrada: `"12345"` · **Rejeitada** · complementar

Constant único pode ser inteiro; a sonda de real rejeita.

**Lexer completo:** `Constant` `"12345"` [0..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `EOF` `"<EOF>"` [5..4; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '12345'"`

## J31 — Java / IntegerLiteral

Entrada: `"12345_"` · **Rejeitada** · complementar

Sublinhado final não faz parte do numeral.

**Lexer completo:** `IntegerLiteral` `"12345"` [0..4; canal 0]; `UNDER_SCORE` `"_"` [5..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345"` [0..4; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 5: `"token recognition error at: '_'"`

## J32 — Java / IntegerLiteral

Entrada: `"0x_FF"` · **Rejeitada** · complementar

Sublinhado logo após o prefixo hexadecimal não é permitido.

**Lexer completo:** `IntegerLiteral` `"0"` [0..0; canal 0]; `Identifier` `"x_FF"` [1..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"0"` [0..0; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros:

- linha 1, coluna 1: `"token recognition error at: 'x'"`
- linha 1, coluna 2: `"token recognition error at: '_'"`
- linha 1, coluna 3: `"token recognition error at: 'F'"`
- linha 1, coluna 4: `"token recognition error at: 'F'"`

## J33 — Java / IntegerLiteral

Entrada: `"1__000"` · **Aceita** · complementar

Múltiplos sublinhados internos são admitidos.

**Lexer completo:** `IntegerLiteral` `"1__000"` [0..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"1__000"` [0..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


## C34 — C / StringLiteral

Entrada: `"\"linha\\\nseguinte\""` · **Aceita** · complementar

SChar admite barra seguida de quebra física LF.

**Lexer completo:** `StringLiteral` `"\"linha\\\nseguinte\""` [0..16; canal 0]; `EOF` `"<EOF>"` [17..16; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"linha\\\nseguinte\""` [0..16; canal 0]; `EOF` `"<EOF>"` [17..16; canal 0]

Erros: nenhum


## J35 — Java / StringLiteral

Entrada: `"\"linha\\\nseguinte\""` · **Rejeitada** · complementar

StringCharacter não admite continuação por barra e LF.

**Lexer completo:** `Identifier` `"seguinte"` [8..15; canal 0]; `EOF` `"<EOF>"` [17..16; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"linha\\\\n'"`
- linha 2, coluna 8: `"token recognition error at: '\"'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [17..16; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"linha\\\\n'"`
- linha 2, coluna 0: `"token recognition error at: 's'"`
- linha 2, coluna 1: `"token recognition error at: 'e'"`
- linha 2, coluna 2: `"token recognition error at: 'g'"`
- linha 2, coluna 3: `"token recognition error at: 'u'"`
- linha 2, coluna 4: `"token recognition error at: 'i'"`
- linha 2, coluna 5: `"token recognition error at: 'n'"`
- linha 2, coluna 6: `"token recognition error at: 't'"`
- linha 2, coluna 7: `"token recognition error at: 'e'"`
- linha 2, coluna 8: `"token recognition error at: '\"'"`

## C36 — C / StringLiteral

Entrada: `"R\"texto\""` · **Rejeitada** · complementar

Esta gramática não tem raw string de C++.

**Lexer completo:** `Identifier` `"R"` [0..0; canal 0]; `StringLiteral` `"\"texto\""` [1..7; canal 0]; `EOF` `"<EOF>"` [8..7; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"texto\""` [1..7; canal 0]; `EOF` `"<EOF>"` [8..7; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: 'R'"`

## C37 — C / StringLiteral

Entrada: `"\"linha\nseguinte\""` · **Rejeitada** · complementar

Quebra física sem barra é excluída de SChar.

**Lexer completo:** `Identifier` `"seguinte"` [7..14; canal 0]; `EOF` `"<EOF>"` [16..15; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"linha\\n'"`
- linha 2, coluna 8: `"token recognition error at: '\"'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [16..15; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"linha\\n'"`
- linha 2, coluna 0: `"token recognition error at: 's'"`
- linha 2, coluna 1: `"token recognition error at: 'e'"`
- linha 2, coluna 2: `"token recognition error at: 'g'"`
- linha 2, coluna 3: `"token recognition error at: 'ui'"`
- linha 2, coluna 5: `"token recognition error at: 'n'"`
- linha 2, coluna 6: `"token recognition error at: 't'"`
- linha 2, coluna 7: `"token recognition error at: 'e'"`
- linha 2, coluna 8: `"token recognition error at: '\"'"`

## J38 — Java / StringLiteral

Entrada: `"\"linha\nseguinte\""` · **Rejeitada** · complementar

Quebra física sem barra é excluída de StringCharacter.

**Lexer completo:** `Identifier` `"seguinte"` [7..14; canal 0]; `EOF` `"<EOF>"` [16..15; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"linha\\n'"`
- linha 2, coluna 8: `"token recognition error at: '\"'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [16..15; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"linha\\n'"`
- linha 2, coluna 0: `"token recognition error at: 's'"`
- linha 2, coluna 1: `"token recognition error at: 'e'"`
- linha 2, coluna 2: `"token recognition error at: 'g'"`
- linha 2, coluna 3: `"token recognition error at: 'u'"`
- linha 2, coluna 4: `"token recognition error at: 'i'"`
- linha 2, coluna 5: `"token recognition error at: 'n'"`
- linha 2, coluna 6: `"token recognition error at: 't'"`
- linha 2, coluna 7: `"token recognition error at: 'e'"`
- linha 2, coluna 8: `"token recognition error at: '\"'"`

## C39 — C / IntegerConstant

Entrada: `"12345 "` · **Rejeitada** · complementar

Espaço oculto ainda é entrada adicional; não é um único literal exato.

**Lexer completo:** `Constant` `"12345"` [0..4; canal 0]; `Whitespace` `" "` [5..5; canal 1]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345"` [0..4; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 5: `"token recognition error at: ' '"`

## J40 — Java / IntegerLiteral

Entrada: `"12345 "` · **Rejeitada** · complementar

WS é descartado, mas o token não cobre toda a entrada.

**Lexer completo:** `IntegerLiteral` `"12345"` [0..4; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345"` [0..4; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 5: `"token recognition error at: ' '"`

## J41 — Java / IntegerLiteral

Entrada: `"-12345"` · **Rejeitada** · complementar

Sinal unário é um token separado; não integra IntegerLiteral.

**Lexer completo:** `SUB` `"-"` [0..0; canal 0]; `IntegerLiteral` `"12345"` [1..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"12345"` [1..5; canal 0]; `EOF` `"<EOF>"` [6..5; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '-'"`

## C42 — C / FloatingConstant

Entrada: `"0x1.8"` · **Rejeitada** · complementar

Real hexadecimal sem expoente binário também é rejeitado em C.

**Lexer completo:** `Constant` `"0x1"` [0..2; canal 0]; `Constant` `".8"` [3..4; canal 0]; `EOF` `"<EOF>"` [5..4; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `EOF` `"<EOF>"` [5..4; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '0x1.8'"`

## C43 — C / StringLiteral

Entrada: `"\"valor\\u0041\""` · **Aceita** · complementar

UniversalCharacterName aceita \u seguido de quatro hexadecimais.

**Lexer completo:** `StringLiteral` `"\"valor\\u0041\""` [0..12; canal 0]; `EOF` `"<EOF>"` [13..12; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"valor\\u0041\""` [0..12; canal 0]; `EOF` `"<EOF>"` [13..12; canal 0]

Erros: nenhum


## J44 — Java / StringLiteral

Entrada: `"\"valor\\uu0041\""` · **Aceita** · complementar

UnicodeEscape Java aceita uma ou mais letras u.

**Lexer completo:** `StringLiteral` `"\"valor\\uu0041\""` [0..13; canal 0]; `EOF` `"<EOF>"` [14..13; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"valor\\uu0041\""` [0..13; canal 0]; `EOF` `"<EOF>"` [14..13; canal 0]

Erros: nenhum


## C45 — C / StringLiteral

Entrada: `"\"valor\\uu0041\""` · **Rejeitada** · complementar

UniversalCharacterName C exige apenas uma letra u.

**Lexer completo:** `Constant` `"0041"` [9..12; canal 0]; `EOF` `"<EOF>"` [14..13; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"valor\\uu'"`
- linha 1, coluna 13: `"token recognition error at: '\"'"`

**Regra isolada (Selected):** `EOF` `"<EOF>"` [14..13; canal 0]

Erros:

- linha 1, coluna 0: `"token recognition error at: '\"valor\\uu'"`
- linha 1, coluna 9: `"token recognition error at: '0'"`
- linha 1, coluna 10: `"token recognition error at: '0'"`
- linha 1, coluna 11: `"token recognition error at: '4'"`
- linha 1, coluna 12: `"token recognition error at: '1'"`
- linha 1, coluna 13: `"token recognition error at: '\"'"`

## J46 — Java / StringLiteral

Entrada: `"\"texto\"/*comentário*/"` · **Rejeitada** · complementar

Um comentário oculto não pode ser ignorado no critério de literal exato.

**Lexer completo:** `StringLiteral` `"\"texto\""` [0..6; canal 0]; `COMMENT` `"/*comentário*/"` [7..20; canal 1]; `EOF` `"<EOF>"` [21..20; canal 0]

Erros: nenhum


**Regra isolada (Selected):** `Selected` `"\"texto\""` [0..6; canal 0]; `EOF` `"<EOF>"` [21..20; canal 0]

Erros:

- linha 1, coluna 7: `"token recognition error at: '/'"`
- linha 1, coluna 8: `"token recognition error at: '*'"`
- linha 1, coluna 9: `"token recognition error at: 'c'"`
- linha 1, coluna 10: `"token recognition error at: 'o'"`
- linha 1, coluna 11: `"token recognition error at: 'm'"`
- linha 1, coluna 12: `"token recognition error at: 'e'"`
- linha 1, coluna 13: `"token recognition error at: 'n'"`
- linha 1, coluna 14: `"token recognition error at: 't'"`
- linha 1, coluna 15: `"token recognition error at: 'á'"`
- linha 1, coluna 16: `"token recognition error at: 'r'"`
- linha 1, coluna 17: `"token recognition error at: 'i'"`
- linha 1, coluna 18: `"token recognition error at: 'o'"`
- linha 1, coluna 19: `"token recognition error at: '*'"`
- linha 1, coluna 20: `"token recognition error at: '/'"`
