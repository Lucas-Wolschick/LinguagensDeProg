# TP1 — Comparação de lexers C e Java 20

Implementação dos pontos **1 (análise e comparação), 2 (demonstração de entradas) e 3 (diagramas de sintaxe)** do enunciado `t-pratico1-lexers-2026-2.pdf`.

A escolha de C e Java 20 e das categorias texto, inteiro e real foi preservada da base do trabalho. As gramáticas vêm da revisão de `antlr/grammars-v4` já citada no repositório: `25ad11e4ff672b1eca69d6eeff109ce11bbb663d`.

## Leitura

- **[Relatório dos pontos 1, 2 e 3](docs/RELATORIO.md)** — análise, 24 exemplos principais, seis imagens de diagramas e conclusões.
- [Evidências completas](docs/RESULTADOS.md) — tokens, posições, canais e erros reais de 46 casos, na regra isolada e no lexer completo.
- [Resultados em JSON](docs/resultados.json) e [casos de teste](tests/cases.json).
- [Atlas de ferrovias](docs/diagramas/atlas.html) — abra o HTML localmente no navegador para navegar por todas as regras auxiliares. No GitHub, as seis imagens SVG estão incorporadas ao relatório.
- [Fontes e adaptações](vendor/README.md).

## Executar as demonstrações

Requisitos: **JDK 17 ou superior**, com `java` e `javac` no PATH, e **Python 3.10 ou superior**. A execução de referência utilizou JDK 21.0.7, Python 3.12 e ANTLR **4.13.2**. Execute na raiz do repositório:

```sh
python tools/run_tests.py
```

Na primeira execução, o script baixa o JAR oficial para `build/` e verifica seu SHA-256. Não há dependências Python externas para os testes. Para usar um JAR já baixado:

```sh
python tools/run_tests.py --jar /caminho/antlr-4.13.2-complete.jar
```

O script gera os analisadores Java, compila, verifica as expectativas e atualiza as evidências em `docs/`. São **46 casos / 92 execuções**, incluindo duas entradas aceitas e duas rejeitadas por regra e linguagem, todas as principais com pelo menos cinco caracteres. Para conferir também que as evidências versionadas estão atualizadas:

```sh
python tools/run_tests.py --check
```

`C.g4` é a gramática combinada original: o parser é gerado pelo ANTLR, mas **não é executado**. `Java.g4` contém o lexer Java 20, renomeado para coincidir com o arquivo. O foco é exclusivamente léxico. Nenhum lexer foi simplificado para forçar os resultados.

## Recriar os diagramas

```sh
python -m pip install -r requirements-diagrams.txt
python tools/generate_diagrams.py
python tools/generate_diagrams.py --check
```

Os SVGs e o atlas são gerados dos corpos das regras em `.g4`. As referências a fragmentos são navegáveis no atlas; a ferramenta recusa construções que não sabe converter.

## Escopo acadêmico

O relatório documenta as fontes e corrige o rascunho anterior, mantido em [histórico](docs/RASCUNHO_ORIGINAL.md). A identificação de todos os integrantes deve ser preenchida pelo grupo no relatório. A reserva das linguagens no Moodle, a gravação do vídeo e a submissão são etapas externas aos pontos 1–3 e não foram realizadas aqui.
