# Conteúdo do relatório — TP1 Lexers (Java 20 × C)

> Texto para colar no modelo do grupo. Trechos entre [colchetes] devem ser preenchidos.

---

## Identificação

PUCRS · Escola Politécnica · Linguagens de Programação · Trabalho Prático 1 (TP1) – Lexer

Integrantes: [nome – matrícula] · [nome – matrícula] · [nome – matrícula] · [nome – matrícula]

Vídeo da apresentação: [URL]

---

## 1. Introdução

Este trabalho compara dois analisadores léxicos escritos para o ANTLR4: o lexer de **Java 20** e o lexer de **C**, ambos do repositório antlr/grammars-v4. O foco está exclusivamente nas regras léxicas; o parser só é usado como apoio para executar os testes.

Foram analisadas três regras equivalentes em cada lexer:

| Categoria | Lexer C | Lexer Java 20 |
|---|---|---|
| TEXTO | `StringLiteral` | `StringLiteral` e `TextBlock` |
| INTEIRO | `Constant` (fragment `IntegerConstant`) | `IntegerLiteral` |
| REAL | `Constant` (fragment `FloatingConstant`) | `FloatingPointLiteral` |

A principal diferença estrutural aparece logo na tabela: em C, inteiros e reais são fragments de um único token, `Constant`; em Java, cada categoria gera seu próprio token.

---

## 2. Metodologia

As gramáticas foram fixadas no commit `25ad11e` do grammars-v4, e todas as entradas foram executadas no ANTLR 4.13.2.

| Item | Versão / ferramenta |
|---|---|
| Gramática Java | `java/java20/Java20Lexer.g4` (lexer grammar) |
| Gramática C | `c/C.g4` (gramática combinada: lexer + parser) |
| Gerador | ANTLR 4.13.2, alvo Java, executado com Java 22 |
| Execução das entradas | programa `testes/Tokens.java` e ANTLR Lab |
| Diagramas de sintaxe | PlantUML (EBNF), BottleCaps Railroad Diagram Generator e extensão ANTLR4 para VS Code |

Procedimento:

1. Ler as regras de cada lexer e os fragments de que dependem.
2. Escolher, para cada regra, duas entradas aceitas e duas rejeitadas, todas com pelo menos 5 caracteres e explorando recursos específicos (prefixos, sufixos, separadores, bases numéricas).
3. Tokenizar cada entrada isoladamente e registrar o tipo e o texto de cada token, além dos erros de reconhecimento.
4. Gerar os diagramas das regras e comparar as duas implementações.

**Critério de rejeição.** Um lexer ANTLR raramente recusa a entrada inteira. Ele aplica a regra do *maior casamento* (longest match) e, quando a regra analisada só cobre parte da entrada, o restante vira outros tokens. Por isso, consideramos **rejeitada** a entrada que não é reconhecida como um único token da regra, seja por `token recognition error`, seja por divisão em vários tokens.

Todos os resultados podem ser reproduzidos com `testes/rodar.sh`; a saída completa está em `testes/resultado.txt`.

---

## 3. Regra TEXTO

As duas regras reconhecem texto entre aspas duplas sem quebra de linha. O lexer C acrescenta prefixos de codificação e continuação de linha. O lexer Java acrescenta o `TextBlock`, mas sua implementação na gramática está incorreta.

### 3.1 Lexer C — `StringLiteral`

```antlr
StringLiteral
    : EncodingPrefix? '"' SCharSequence? '"'
    ;
fragment EncodingPrefix : 'u8' | 'u' | 'U' | 'L' ;
fragment SCharSequence  : SChar+ ;
fragment SChar
    : ~["\\\r\n]
    | EscapeSequence
    | '\\\n'   // Added line
    | '\\\r\n' // Added line
    ;
fragment EscapeSequence
    : SimpleEscapeSequence        // '\\' ['"?abfnrtv\\]
    | OctalEscapeSequence         // '\\' OctalDigit OctalDigit? OctalDigit?
    | HexadecimalEscapeSequence   // '\\x' HexadecimalDigit+
    | UniversalCharacterName      // '\\u' HexQuad | '\\U' HexQuad HexQuad
    ;
```

A string pode ter um prefixo opcional (`u8`, `u`, `U`, `L`), seguido de aspas. Dentro delas vale qualquer caractere exceto `"`, `\` e quebra de linha, ou uma sequência de escape. As duas alternativas marcadas `Added line` permitem continuar a string na linha seguinte com `\` no fim da linha.

| Resultado | Entrada | Saída do ANTLR4 |
|---|---|---|
| Aceita | `u8"Olá, mundo!\n"` | `StringLiteral` |
| Aceita | `L"tab\there \x41\101"` | `StringLiteral` |
| Rejeitada | `"texto sem fim` | `token recognition error at: '"texto sem fim'` |
| Rejeitada | `"escape \q inválido"` | erro em `'"escape \q'`, `Identifier inv`, erro em `'á'`, `Identifier lido`, erro em `'"'` |

Na segunda entrada aceita, o lexer reconhece um escape hexadecimal (`\x41`) e um octal (`\101`) no mesmo token. Na última rejeitada, `\q` não é escape válido; o lexer descarta o início e retoma depois. O `á` também gera erro porque `Identifier` em C só aceita ASCII.

### 3.2 Lexer Java — `StringLiteral` e `TextBlock`

```antlr
StringLiteral: '"' StringCharacters? '"';
fragment StringCharacters: StringCharacter+;
fragment StringCharacter: ~["\\\r\n] | EscapeSequence;
TextBlock: '"""' [ \t]* [\n\r] [.\r\b]* '"""';
fragment EscapeSequence:
    '\\' [btnfr"'\\]
    | OctalEscape     // \0 a \377
    | UnicodeEscape   // '\\' 'u'+ HexDigit HexDigit HexDigit HexDigit
;
```

A string comum segue a mesma estrutura do C, sem prefixo nem continuação de linha. O `TextBlock` deveria aceitar texto de várias linhas, mas `[.\r\b]*` é um *conjunto de caracteres*: aceita apenas ponto, CR e backspace, e nem sequer a quebra de linha.

| Resultado | Entrada | Saída do ANTLR4 |
|---|---|---|
| Aceita | `"Olá, \"mundo\"\tA"` | `StringLiteral` |
| Aceita | `"octal \101 e \uuu0042"` | `StringLiteral` |
| Rejeitada | `"espaco\sJava15"` | erro em `'"espaco\s'`, `Identifier Java15`, erro em `'"'` |
| Rejeitada | text block de 3 linhas: `"""` / `    Olá mundo` / `    """` | `StringLiteral ""`, erro em `'"\n'`, `Identifier Olá`, `Identifier mundo`, `StringLiteral ""`, erro em `'"'` |

O escape `\s` existe em Java desde a versão 15, mas falta na gramática, então uma string válida para o compilador é rejeitada pelo lexer. O text block comum também é rejeitado; como prova do defeito, `"""` + quebra de linha + `....."""` é aceito como `TextBlock`.

### 3.3 Comparação

| Aspecto | C | Java 20 |
|---|---|---|
| Delimitador | `"..."` | `"..."` e `"""..."""` |
| Prefixo de codificação | `u8`, `u`, `U`, `L` | não tem (`u8"x"` vira `Identifier` + `StringLiteral`) |
| Texto em várias linhas | `\` + quebra de linha | `TextBlock` (defeituoso na gramática) |
| Escapes exclusivos | `\a`, `\v`, `\?`, `\xHH…`, `\UXXXXXXXX` | `\uXXXX` com vários `u` |
| Fidelidade à especificação | segue o padrão C | falta `\s` e o `TextBlock` não funciona |

O núcleo das duas regras é idêntico: `~["\\\r\n] | EscapeSequence`. A diferença está no que cada linguagem põe em volta desse núcleo, e as entradas mostram que a gramática de Java ficou atrás da linguagem real.

---

## 4. Regra INTEIRO

As duas regras reconhecem decimal, octal, hexadecimal e binário. Java permite o separador `_` entre dígitos e só tem o sufixo `L`; C não tem separador, mas tem sufixos de sinal e tamanho (`U`, `L`, `LL`).

### 4.1 Lexer C — `Constant` / `IntegerConstant`

```antlr
Constant
    : IntegerConstant
    | FloatingConstant
    | CharacterConstant
    ;
fragment IntegerConstant
    : DecimalConstant IntegerSuffix?
    | OctalConstant IntegerSuffix?
    | HexadecimalConstant IntegerSuffix?
    | BinaryConstant
    ;
fragment BinaryConstant      : '0' [bB] [0-1]+ ;
fragment DecimalConstant     : NonzeroDigit Digit* ;
fragment OctalConstant       : '0' OctalDigit* ;
fragment HexadecimalConstant : HexadecimalPrefix HexadecimalDigit+ ;
fragment IntegerSuffix
    : UnsignedSuffix LongSuffix?
    | UnsignedSuffix LongLongSuffix
    | LongSuffix UnsignedSuffix?
    | LongLongSuffix UnsignedSuffix?
    ;
fragment UnsignedSuffix : [uU] ;
fragment LongSuffix     : [lL] ;
fragment LongLongSuffix : 'll' | 'LL' ;

DigitSequence : Digit+ ;   // token próprio (não é fragment)
```

`IntegerConstant` é um fragment: o token emitido é sempre `Constant`, o mesmo de reais e caracteres. Os sufixos podem vir em qualquer ordem (`ULL`, `lu`), mas `ll` precisa ter as duas letras do mesmo caso. O binário não aceita sufixo.

| Resultado | Entrada | Saída do ANTLR4 |
|---|---|---|
| Aceita | `0x7FFFFFFFULL` | `Constant` |
| Aceita | `1234567890lu` | `Constant` |
| Rejeitada | `1_000_000` | `Constant 1` + `Identifier _000_000` |
| Rejeitada | `0b1010u` | `Constant 0b1010` + `Identifier u` |

Um caso curioso é `01289`. Como `8` e `9` não são dígitos octais, `Constant` só cobriria `012`. Mas o token `DigitSequence` (`Digit+`) cobre os 5 caracteres e vence pela regra do maior casamento: a saída é **`DigitSequence 01289`**, nem `Constant` nem erro. Outro: `100lL` vira `Constant 100l` + `Identifier L`, pois `lL` misturado não é sufixo válido.

### 4.2 Lexer Java — `IntegerLiteral`

```antlr
IntegerLiteral:
    DecimalIntegerLiteral
    | HexIntegerLiteral
    | OctalIntegerLiteral
    | BinaryIntegerLiteral
;
fragment DecimalIntegerLiteral: DecimalNumeral IntegerTypeSuffix?;
fragment IntegerTypeSuffix: [lL];
fragment DecimalNumeral: '0' | NonZeroDigit (Digits? | Underscores Digits);
fragment Digits: Digit (DigitsAndUnderscores? Digit)?;
fragment DigitsAndUnderscores: DigitOrUnderscore+;
fragment DigitOrUnderscore: Digit | '_';
fragment HexNumeral: '0' [xX] HexDigits;
fragment HexDigits: HexDigit (HexDigitsAndUnderscores? HexDigit)?;
fragment OctalNumeral: '0' Underscores? OctalDigits;
fragment BinaryNumeral: '0' [bB] BinaryDigits;
// HexIntegerLiteral, OctalIntegerLiteral e BinaryIntegerLiteral seguem o mesmo padrão
```

O padrão `Digit (DigitsAndUnderscores? Digit)?` aparece em todas as bases: o número começa e termina com dígito, e no meio pode haver `_`. O único sufixo é `l`/`L`, comum às quatro bases.

| Resultado | Entrada | Saída do ANTLR4 |
|---|---|---|
| Aceita | `1_000_000L` | `IntegerLiteral` |
| Aceita | `0x7FFF_FFFF` | `IntegerLiteral` |
| Rejeitada | `100ULL` | `IntegerLiteral 100` + `Identifier ULL` |
| Rejeitada | `0x_FFFF` | `IntegerLiteral 0` + `Identifier x_FFFF` |

Na última, o `_` logo após `0x` impede o `HexNumeral`; o lexer fica só com o `0` e o resto vira identificador. Outros casos: `1_000_` vira `IntegerLiteral 1_000` + `UNDER_SCORE _`, e `01289` vira `IntegerLiteral 012` + `IntegerLiteral 89`.

### 4.3 Comparação

| Aspecto | C | Java 20 |
|---|---|---|
| Token emitido | `Constant` (compartilhado com real e caractere) | `IntegerLiteral` |
| Bases | decimal, octal, hexadecimal, binário | decimal, octal, hexadecimal, binário |
| Separador de dígitos | não tem | `_` entre dígitos |
| Sufixos | `u`, `l`, `ll` e combinações | só `l` / `L` |
| Sufixo em binário | não aceita | aceita (`0b1010L`) |
| `01289` | `DigitSequence` (1 token) | `IntegerLiteral 012` + `IntegerLiteral 89` |

Java é mais rico na *forma* do número (separadores) e C, nos *tipos* (unsigned, long long). A escolha de C de emitir `Constant` para tudo simplifica o lexer, mas empurra para o parser a tarefa de saber se a constante é inteira ou real. O token `DigitSequence` mostra um efeito colateral: uma regra pensada como apoio para reais acaba capturando inteiros mal formados.

---

## 5. Regra REAL

As duas regras têm quase a mesma estrutura: parte inteira, ponto, parte fracionária, expoente decimal (`e`) e o formato hexadecimal com expoente binário obrigatório (`p`). A diferença está nos sufixos e no separador `_`.

### 5.1 Lexer C — `Constant` / `FloatingConstant`

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
fragment ExponentPart       : [eE] Sign? DigitSequence ;
fragment BinaryExponentPart : [pP] Sign? DigitSequence ;
fragment FloatingSuffix     : [flFL] ;
DigitSequence : Digit+ ;
```

Um real decimal precisa de ponto ou de expoente; o sufixo `f` indica `float` e `l` indica `long double`. Também é emitido como `Constant`.

| Resultado | Entrada | Saída do ANTLR4 |
|---|---|---|
| Aceita | `6.022e+23L` | `Constant` |
| Aceita | `0x1.8p3f` | `Constant` |
| Rejeitada | `10_000.00` | `Constant 10` + `Identifier _000` + `Constant .00` |
| Rejeitada | `0x1.8F` | `Constant 0x1` + `Constant .8F` |

Sem o `p`, `0x1.8F` não é um real hexadecimal: o lexer fecha um inteiro hexadecimal em `0x1` e começa um novo real decimal em `.8F`. Outro caso: `1000f` vira `Constant 1000` + `Identifier f`, porque em C o sufixo `f` exige ponto ou expoente.

### 5.2 Lexer Java — `FloatingPointLiteral`

```antlr
FloatingPointLiteral: DecimalFloatingPointLiteral | HexadecimalFloatingPointLiteral;
fragment DecimalFloatingPointLiteral:
    Digits '.' Digits? ExponentPart? FloatTypeSuffix?
    | '.' Digits ExponentPart? FloatTypeSuffix?
    | Digits ExponentPart FloatTypeSuffix?
    | Digits FloatTypeSuffix
;
fragment ExponentPart: ExponentIndicator SignedInteger;
fragment SignedInteger: Sign? Digits;
fragment FloatTypeSuffix: [fFdD];
fragment HexadecimalFloatingPointLiteral: HexSignificand BinaryExponent FloatTypeSuffix?;
fragment HexSignificand: HexNumeral '.'? | '0' [xX] HexDigits? '.' HexDigits;
fragment BinaryExponent: BinaryExponentIndicator SignedInteger;
```

A quarta alternativa (`Digits FloatTypeSuffix`) não existe em C: um inteiro seguido de `f` ou `d` já é real. Como reaproveita `Digits`, o separador `_` também vale aqui.

| Resultado | Entrada | Saída do ANTLR4 |
|---|---|---|
| Aceita | `10_000.000_1` | `FloatingPointLiteral` |
| Aceita | `0x1.8p3f` | `FloatingPointLiteral` |
| Rejeitada | `3.1415L` | `FloatingPointLiteral 3.1415` + `Identifier L` |
| Rejeitada | `0x1.8F` | `IntegerLiteral 0x1` + `FloatingPointLiteral .8F` |

`3.1415L` é aceito em C como `long double`, mas Java não tem esse sufixo. `0x1.8F` falha pelo mesmo motivo do C, só que aqui os dois pedaços recebem tokens diferentes. Outros casos: `1000f` é `FloatingPointLiteral` e `1_000._5` vira `FloatingPointLiteral 1_000.` + `Identifier _5`.

### 5.3 Comparação

| Aspecto | C | Java 20 |
|---|---|---|
| Token emitido | `Constant` | `FloatingPointLiteral` |
| Formatos | `12.5`, `.5`, `12.`, `1e10`, hexadecimal com `p` | os mesmos |
| Sufixos | `f`/`F` (float), `l`/`L` (long double) | `f`/`F` (float), `d`/`D` (double) |
| Inteiro + sufixo (`1000f`) | não é real | é real |
| Separador `_` | não tem | aceito (`10_000.000_1`) |
| `0x1.8F` (sem `p`) | `Constant` + `Constant` | `IntegerLiteral` + `FloatingPointLiteral` |

Esta é a regra em que os dois lexers mais se parecem: as alternativas de C e Java têm praticamente a mesma ordem. As diferenças vêm da linguagem (sufixos e separador), não de escolhas de projeto da gramática.

---

## 6. Diagramas de sintaxe

[Inserir as imagens de `diagramas/plantuml/*.png` e as geradas pelo BottleCaps e pela extensão do VS Code.]

Os diagramas foram gerados a partir de arquivos EBNF escritos à mão com base nas regras ANTLR: `diagramas/plantuml/*.puml` para o PlantUML e `diagramas/bottlecaps/*.ebnf` para o BottleCaps. Como os fragments mais simples (`Digit`, `HexDigit`, `OctalDigit`) foram mantidos como caixas, cada diagrama corresponde de perto à estrutura da gramática original.

| Regra | C | Java 20 |
|---|---|---|
| TEXTO | `C_StringLiteral` | `Java_StringLiteral` |
| INTEIRO | `C_IntegerConstant` | `Java_IntegerLiteral` |
| REAL | `C_FloatingConstant` | `Java_FloatingPointLiteral` |

**Comparação entre os diagramas das duas linguagens:**

- **TEXTO.** Os dois diagramas têm o mesmo eixo principal (aspa, laço de caracteres, aspa). O de C tem um desvio opcional antes da aspa (o prefixo) e dois caminhos extras com `\` + quebra de linha. No de Java, o laço do `TextBlock` mostra visualmente o defeito: o caminho só passa por ponto, CR e backspace.
- **INTEIRO.** O diagrama de C é largo e raso: uma escolha entre quatro bases e uma caixa de sufixo com quatro caminhos. O de Java é mais profundo: cada base repete o mesmo laço "dígito, (dígito ou `_`)*, dígito", o que deixa claro onde o `_` pode e não pode aparecer. O sufixo aparece uma vez só, no final, comum a todas as bases.
- **REAL.** Os diagramas são quase iguais em formato. O de Java tem uma alternativa a mais (dígitos + sufixo, sem ponto) e o caminho de sufixo termina em `d`/`D` em vez de `l`/`L`.

**Como as diferenças afetam a interpretação visual:**

- Fragments desenhados como caixas deixam o diagrama principal curto, mas obrigam o leitor a procurar a definição em outro diagrama. Expandir tudo (como no laço de `_` em Java) torna o diagrama maior, porém mais direto de ler.
- Repetições com separador, como `Digit (DigitOrUnderscore* Digit)?`, viram um laço com volta que é muito mais fácil de entender no desenho do que no texto da gramática.
- O diagrama não mostra o comportamento do maior casamento entre tokens diferentes. Por exemplo, o `DigitSequence` de C capturando `01289` não aparece em nenhum diagrama isolado; só os testes revelam essa interação.

**Comparação entre ferramentas:** [preencher depois de gerar com as três ferramentas — ex.: o PlantUML desenha caracteres especiais e classes como caixas tracejadas, o BottleCaps aceita classes de caracteres como `[0-9]` diretamente, a extensão do VS Code lê o `.g4` sem conversão manual.]

---

## 7. Conclusões

- **Token único × tokens separados.** C concentra inteiros, reais e caracteres no token `Constant`; Java separa cada categoria. A abordagem de Java facilita o trabalho do parser e torna a saída do lexer mais informativa.
- **A gramática pode divergir da linguagem.** O lexer Java não aceita `\s` e tem um `TextBlock` que não reconhece text blocks reais. Uma gramática pronta precisa ser testada antes de ser usada.
- **O lexer quase nunca recusa a entrada; ele a divide.** Entradas inválidas como `1_000_000` em C ou `100ULL` em Java viram vários tokens válidos. O erro, nesses casos, só seria detectado pelo parser.
- **A regra do maior casamento tem efeitos inesperados.** O token `DigitSequence` de C, criado como apoio, captura `01289` inteiro e muda o resultado esperado.
- **Diferenças da linguagem aparecem diretamente nas regras.** O separador `_` de Java e os sufixos `U`/`LL` de C são as principais diferenças entre as regras numéricas.

[Acrescentar aprendizados próprios do grupo.]

---

## 8. Referências

- ANTLR. *grammars-v4*, commit 25ad11e4ff672b1eca69d6eeff109ce11bbb663d. Gramática Java 20: https://github.com/antlr/grammars-v4/blob/25ad11e4ff672b1eca69d6eeff109ce11bbb663d/java/java20/Java20Lexer.g4 . Gramática C: https://github.com/antlr/grammars-v4/blob/25ad11e4ff672b1eca69d6eeff109ce11bbb663d/c/C.g4
- PARR, Terence. *The Definitive ANTLR 4 Reference*. 2. ed. Pragmatic Bookshelf, 2013.
- ANTLR 4.13.2: https://www.antlr.org/
- ANTLR Lab: http://lab.antlr.org/
- GOSLING, J. et al. *The Java Language Specification, Java SE 20 Edition*. Oracle, 2023. Cap. 3 (Lexical Structure): https://docs.oracle.com/javase/specs/jls/se20/html/jls-3.html
- ISO/IEC 9899:2011 — *Programming languages — C* (C11), seção 6.4 (Lexical elements).
- PlantUML — EBNF: https://plantuml.com/ebnf
- RADEMACHER, Gunther. *Railroad Diagram Generator* (BottleCaps): https://www.bottlecaps.de/rr/ui
- LISCHKE, Mike. *ANTLR4 grammar syntax support* (extensão VS Code): https://marketplace.visualstudio.com/items?itemName=mike-lischke.vscode-antlr4
