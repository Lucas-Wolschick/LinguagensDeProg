# Entradas de teste — Java 20 × C

Todas as entradas abaixo foram **executadas no ANTLR 4.13.2** com as gramáticas desta pasta
(`Java20Lexer.g4` e `C.g4`, grammars-v4 commit `25ad11e`). A saída completa está em
[`testes/resultado.txt`](testes/resultado.txt).

**Critério de "rejeitada":** o lexer do ANTLR não recusa a entrada inteira, então "rejeitada" quer
dizer que a entrada **não** é reconhecida como **um único token** da regra. Isso acontece de dois jeitos:

- **erro de reconhecimento** (`token recognition error`): nenhuma regra casa aquele trecho;
- **divisão em vários tokens**: o lexer reconhece só um prefixo pela regra (maior casamento possível) e
  o resto vira outro(s) token(s), como identificador ou operador.

Todas as entradas têm 5 caracteres ou mais, como pede o enunciado.

---

## Como rodar

### Opção A — linha de comando (reproduz exatamente `resultado.txt`)

No Git Bash, dentro de `testes/`:

```bash
./rodar.sh > resultado.txt
```

O script baixa o ANTLR 4.13.2 (se faltar), gera os dois lexers, compila e tokeniza cada bloco de
`entradas.txt`. Para testar outra entrada, adicione no `entradas.txt`:

```
@@@ J nome-do-teste
sua entrada aqui
```

(`J` = Java, `C` = C. A entrada pode ter várias linhas; vai até o próximo `@@@`.)

> Cuidado ao editar `entradas.txt`: alguns editores/ferramentas convertem `A` em `A`.
> Confira se a barra invertida continua lá.

### Opção B — ANTLR Lab (para as capturas de tela do relatório)

Acesse http://lab.antlr.org/.

**Java:**
1. Na aba **Lexer**, apague o conteúdo e cole o arquivo `Java20Lexer.g4` inteiro.
2. Na aba **Parser**, apague o conteúdo e cole:
   ```antlr
   parser grammar Java20Parser;
   options { tokenVocab = Java20Lexer; }
   trabalholingdeprog : .*? EOF ;
   ```
3. Em **Start rule**, coloque `trabalholingdeprog`.
4. Cole **uma entrada por vez** em **Input** e clique em **Run**. Capture a lista de tokens e o
   console (os erros de reconhecimento aparecem lá).

**C** (a gramática é *combinada*, com lexer e parser no mesmo arquivo):
1. Na aba **Lexer**, apague todo o conteúdo.
2. Na aba **Parser**, cole o `C.g4` inteiro e acrescente no final:
   ```antlr
   trabalholingdeprog : .*? EOF ;
   ```
3. Em **Start rule**, coloque `trabalholingdeprog`, e siga como no Java.

> Os passos do Lab não foram testados por mim (a interface pode mudar). Se o Lab reclamar da
> gramática combinada, use a Opção A e, para as capturas, um print do terminal com o resultado.
> Os nomes dos tokens devem ser idênticos aos da tabela.

---

## 1. TEXTO

### C — `StringLiteral`

| | Entrada | Saída do ANTLR4 | Por quê |
|---|---|---|---|
| ✅ | `u8"Olá, mundo!\n"` | `StringLiteral` | prefixo `u8` + escape `\n` |
| ✅ | `L"tab\there \x41\101"` | `StringLiteral` | prefixo `L`, escape hex `\x41` e octal `\101` |
| ❌ | `"texto sem fim` | `token recognition error at: '"texto sem fim'` | falta a aspa de fechamento |
| ❌ | `"escape \q inválido"` | erro em `'"escape \q'`, `Identifier inv`, erro em `'á'`, `Identifier lido`, erro em `'"'` | `\q` não é escape válido; e `Identifier` de C não aceita `á` |

Extras interessantes:
- `"linha um \⏎linha dois"` (barra + quebra de linha real) → **`StringLiteral`** (continuação de linha aceita)
- `R"(raw string)"` → `Identifier R` + `StringLiteral "(raw string)"` (raw string é C++, não C)

### Java — `StringLiteral` / `TextBlock`

| | Entrada | Saída do ANTLR4 | Por quê |
|---|---|---|---|
| ✅ | `"Olá, \"mundo\"\tA"` | `StringLiteral` | aspas escapadas, `\t` e escape Unicode |
| ✅ | `"octal \101 e \uuu0042"` | `StringLiteral` | octal e Unicode com vários `u` (permitido pela regra `'u'+`) |
| ❌ | `"espaco\sJava15"` | erro em `'"espaco\s'`, `Identifier Java15`, erro em `'"'` | `\s` existe desde o Java 15, mas **falta na gramática** |
| ❌ | text block normal (3 linhas):<br>`"""`<br>`    Olá mundo`<br>`    """` | `StringLiteral ""`, erro em `'"\n'`, `Identifier Olá`, `Identifier mundo`, `StringLiteral ""`, erro em `'"'` | **bug da gramática**: `[.\r\b]*` só aceita `.`, CR e backspace |

Extras interessantes:
- `"""⏎....."""` → **`TextBlock`**: prova do bug, pois só com pontos o text block é aceito
- `u8"prefixo C"` → `Identifier u8` + `StringLiteral`: Java não tem prefixo de codificação
- `"texto sem fim` → mesmo erro do C

---

## 2. INTEIRO

### C — `Constant` (fragment `IntegerConstant`)

| | Entrada | Saída do ANTLR4 | Por quê |
|---|---|---|---|
| ✅ | `0x7FFFFFFFULL` | `Constant` | hexadecimal + sufixo `ULL` |
| ✅ | `1234567890lu` | `Constant` | decimal + sufixo `lu` (ordem livre) |
| ❌ | `1_000_000` | `Constant 1` + `Identifier _000_000` | C não tem separador `_` |
| ❌ | `0b1010u` | `Constant 0b1010` + `Identifier u` | `BinaryConstant` não aceita sufixo |

Extras interessantes:
- `0b10100101` → `Constant` (binário aceito)
- `01289` → **`DigitSequence`** (não é `Constant`, nem erro): `Constant` só casaria `012`, e o token `DigitSequence` casa os 5 caracteres, então vence o maior casamento
- `100lL` → `Constant 100l` + `Identifier L` (`lL` misturado não vale)

### Java — `IntegerLiteral`

| | Entrada | Saída do ANTLR4 | Por quê |
|---|---|---|---|
| ✅ | `1_000_000L` | `IntegerLiteral` | separador `_` + sufixo `L` |
| ✅ | `0x7FFF_FFFF` | `IntegerLiteral` | hexadecimal com `_` |
| ❌ | `100ULL` | `IntegerLiteral 100` + `Identifier ULL` | Java não tem `U` nem `LL` |
| ❌ | `0x_FFFF` | `IntegerLiteral 0` + `Identifier x_FFFF` | `_` não pode vir logo após o prefixo |

Extras interessantes:
- `0b1010_0101` → `IntegerLiteral`
- `01289` → `IntegerLiteral 012` + `IntegerLiteral 89` (compare com o `DigitSequence` do C)
- `1_000_` → `IntegerLiteral 1_000` + `UNDER_SCORE _` (`_` não pode terminar o número)

---

## 3. REAL

### C — `Constant` (fragment `FloatingConstant`)

| | Entrada | Saída do ANTLR4 | Por quê |
|---|---|---|---|
| ✅ | `6.022e+23L` | `Constant` | expoente com sinal + sufixo `L` (long double) |
| ✅ | `0x1.8p3f` | `Constant` | hex float com expoente binário `p` |
| ❌ | `10_000.00` | `Constant 10` + `Identifier _000` + `Constant .00` | sem separador `_` |
| ❌ | `0x1.8F` | `Constant 0x1` + `Constant .8F` | hex float exige o expoente `p` |

Extras interessantes:
- `.5e-10F` → `Constant`
- `1000f` → `Constant 1000` + `Identifier f` (em C, `f` só vale com ponto ou expoente)
- `1.5e+f` → `Constant 1.5` + `Identifier e` + `Plus` + `Identifier f`

### Java — `FloatingPointLiteral`

| | Entrada | Saída do ANTLR4 | Por quê |
|---|---|---|---|
| ✅ | `10_000.000_1` | `FloatingPointLiteral` | `_` nas duas partes do número |
| ✅ | `0x1.8p3f` | `FloatingPointLiteral` | hex float, igual ao C |
| ❌ | `3.1415L` | `FloatingPointLiteral 3.1415` + `Identifier L` | Java não tem sufixo `L` para real |
| ❌ | `0x1.8F` | `IntegerLiteral 0x1` + `FloatingPointLiteral .8F` | hex float exige `p` |

Extras interessantes:
- `1000f` → **`FloatingPointLiteral`** (em Java, inteiro + `f`/`d` vira real; em C não)
- `6.022e+23d` → `FloatingPointLiteral`
- `1_000._5` → `FloatingPointLiteral 1_000.` + `Identifier _5`
- `1.5e+f` → `FloatingPointLiteral 1.5` + `Identifier e` + `ADD` + `Identifier f`

---

## Pares para a comparação (mesma entrada, resultado diferente)

| Entrada | C | Java |
|---|---|---|
| `1_000_000` / `10_000.00` | divide em vários tokens | um token só (com `L` / `.000_1`) |
| `01289` | `DigitSequence` (1 token) | `IntegerLiteral 012` + `IntegerLiteral 89` |
| `1000f` | `Constant` + `Identifier` | `FloatingPointLiteral` |
| `6.022e+23L` / `3.1415L` | `Constant` (long double) | real + `Identifier L` |
| `u8"..."` | `StringLiteral` | `Identifier` + `StringLiteral` |
| `0x1.8F` | `Constant` + `Constant` | `IntegerLiteral` + `FloatingPointLiteral` |
| Inteiro × real | ambos saem como `Constant` | `IntegerLiteral` × `FloatingPointLiteral` |
