# Contexto do trabalho — TP1 Lexers

## Do que se trata

Trabalho Prático 1 de **Linguagens de Programação** (PUCRS, Escola Politécnica). Enunciado completo em
[`enunciado-tp1-lexers-2026-2.pdf`](enunciado-tp1-lexers-2026-2.pdf).

O grupo escolhe **dois lexers feitos em ANTLR4** e, focando só nas regras léxicas:

1. **Analisa e compara** 3 regras de cada lexer (aqui: TEXTO, INTEIRO e REAL);
2. **Demonstra entradas:** 2 aceitas e 2 rejeitadas por regra, com o resultado gerado pelo ANTLR4;
3. **Faz diagramas de sintaxe** (railroad) das regras e compara os diagramas.

Entregas: **relatório escrito** + **vídeo de ~10 min** com todos os integrantes, enviados no fórum do Moodle.

Lexers escolhidos: **Java 20** e **C**, do [antlr/grammars-v4](https://github.com/antlr/grammars-v4)
(commit `25ad11e`). Trabalho antigo reaproveitado e refeito em 2026-10.

### Peso na nota

| Componente | Peso |
|---|---|
| Comparação entre os lexers | 30% |
| Demonstração de entradas aceitas/rejeitadas | 25% |
| Diagramas de sintaxe e análise comparativa | 15% |
| Resultados do ANTLR4 para as entradas | 10% |
| Metodologia e fontes | 10% |

Orientações do enunciado: entradas com pelo menos 5 caracteres, nada trivial (ex.: `10_000.00` em vez de `1`),
não usar palavras-reservadas como exemplo, usar ANTLR4.

---

## Arquivos

| Arquivo / pasta | Conteúdo |
|---|---|
| `enunciado-tp1-lexers-2026-2.pdf` | Enunciado do trabalho |
| `C.g4`, `Java20Lexer.g4` | Gramáticas originais do grammars-v4 |
| `REGRAS.md` | As 3 regras de cada lexer, completas, com observações |
| `ENTRADAS.md` | Entradas aceitas/rejeitadas com a saída do ANTLR4 + como rodar |
| `RELATORIO.md` | **Conteúdo do relatório**, para colar no modelo do grupo |
| `testes/` | Script e entradas para reproduzir os resultados (`rodar.sh` → `resultado.txt`) |
| `diagramas/plantuml/` | Diagramas gerados (PNG) + fontes `.puml` |
| `diagramas/bottlecaps/` | Regras em EBNF para colar em bottlecaps.de/rr/ui |
| `diagramas/vscode/` | (a criar) diagramas da extensão ANTLR4 do VS Code |
| `CHANGELOG.md` | Rascunho antigo — **desatualizado e com erros**, não usar |

---

## Em que passo estamos

**Passo atual: gerar os diagramas que faltam e tirar os prints.**

### Feito
- [x] Gramáticas reais baixadas e regras completas extraídas (`REGRAS.md`)
- [x] 43 entradas testadas no ANTLR 4.13.2 (`ENTRADAS.md`, `testes/resultado.txt`)
- [x] Diagramas PlantUML gerados (6 PNGs)
- [x] Arquivos EBNF para o BottleCaps
- [x] Conteúdo do relatório escrito (`RELATORIO.md`)

### Falta
- [ ] Confirmar no Moodle que Java e C estão reservados para o grupo
- [ ] Diagramas da extensão VS Code (8: `StringLiteral`, `Constant`, `IntegerConstant`, `FloatingConstant` em `C.g4`;
      `StringLiteral`, `TextBlock`, `IntegerLiteral`, `FloatingPointLiteral` em `Java20Lexer.g4`) → `diagramas/vscode/`
- [ ] Diagramas do BottleCaps (colar os `.ebnf` no site e salvar as imagens)
- [ ] Escrever a "Comparação entre ferramentas" de diagramas no `RELATORIO.md`
- [ ] Prints das entradas no ANTLR Lab (ou do terminal)
- [ ] Passar o `RELATORIO.md` para o modelo do grupo e preencher os [colchetes] (nomes, matrículas, link do vídeo, aprendizados)
- [ ] Gravar o vídeo (~10 min: intro 1 · demonstração 5 · diagramas 2 · conclusões 2), todos os integrantes falando
- [ ] Subir o vídeo na nuvem e enviar link + relatório no fórum do Moodle

### Quando estiver pronto (antes de entregar / publicar o repositório)
- [ ] **Excluir as pastas e arquivos de IA**, se existirem: `.claude/`, `.qodo/`, `.embold/`, `CLAUDE.md`
- [ ] Excluir `.antlr/` (cache gerado pela extensão do VS Code) e `testes/build/`, `testes/*.jar`
- [ ] Apagar ou atualizar o `CHANGELOG.md` antigo
