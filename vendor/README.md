# Proveniência das gramáticas

As cópias nesta pasta são os arquivos originais de `antlr/grammars-v4` na revisão **25ad11e4ff672b1eca69d6eeff109ce11bbb663d**, preservando a referência já adotada pelo trabalho.

| Arquivo | Origem fixa | Uso local |
|---|---|---|
| `C.g4` | [c/C.g4](https://github.com/antlr/grammars-v4/blob/25ad11e4ff672b1eca69d6eeff109ce11bbb663d/c/C.g4) | Copiado integralmente para a raiz; gramática combinada, testes usam apenas `CLexer`. |
| `Java20Lexer.g4` | [java/java20/Java20Lexer.g4](https://github.com/antlr/grammars-v4/blob/25ad11e4ff672b1eca69d6eeff109ce11bbb663d/java/java20/Java20Lexer.g4) | Copiado para `Java.g4`; única alteração: `lexer grammar Java20Lexer;` → `lexer grammar Java;`. |

Os hashes SHA-256 dos originais estão em [sources.json](sources.json) e são verificados durante os testes, assim como a equivalência das cópias da raiz. A licença BSD e os avisos existentes no arquivo C foram preservados. O arquivo Java original não contém cabeçalho de licença; sua origem permanece explicitamente atribuída aqui.

As sondas são geradas em `build/generated/`: uma regra emissora `Selected` referencia a regra estudada, cujo corpo e dependências são copiados sem alteração de expressão. Todas as dependências tornam-se `fragment` nessa sonda, inclusive `DigitSequence` de C, para evitar concorrência de outras regras. O lexer completo também é executado e sua saída é documentada separadamente. As sondas são instrumentos de medição, não substitutos das gramáticas originais.

Ferramenta de execução: [ANTLR 4.13.2](https://www.antlr.org/download.html). Gerador de ferrovias: [railroad-diagrams 3.0.1](https://github.com/tabatkins/railroad-diagrams). O conversor local atende às construções presentes nas seis regras e suas dependências; não pretende aceitar toda a metalinguagem ANTLR.
