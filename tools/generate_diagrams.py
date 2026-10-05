"""Gera ferrovias diretamente dos corpos ANTLR e um atlas dos fragmentos."""
import argparse
import html
import io
from grammar_rules import ROOT, TARGETS, rules, dependencies
from railroad import Diagram, Terminal, NonTerminal, Sequence, Choice, Optional, OneOrMore, ZeroOrMore


class Expression:
    def __init__(self, stream, language, all_rules):
        self.stream, self.language, self.all_rules = stream, language, all_rules
        self.position = 0

    def peek(self):
        return self.stream[self.position] if self.position < len(self.stream) else None

    def take(self):
        token = self.peek()
        if token is None:
            raise ValueError("Expressão incompleta")
        self.position += 1
        return token

    def choice(self):
        alternatives = [self.sequence()]
        while self.peek() == "|":
            self.take()
            alternatives.append(self.sequence())
        return alternatives[0] if len(alternatives) == 1 else Choice(0, *alternatives)

    def sequence(self):
        elements = []
        while self.peek() not in (None, ")", "|"):
            token = self.take()
            if token == "(":
                node = self.choice()
                assert self.take() == ")"
            elif token == "~":
                value = self.take()
                assert value.startswith(("[", "'"))
                node = Terminal("~" + value, title="Qualquer caractere fora do conjunto indicado")
            elif token.startswith(("[", "'")):
                node = Terminal(token)
            elif token in self.all_rules:
                node = NonTerminal(token, href=f"atlas.html#{self.language}-{token}")
            else:
                raise ValueError(f"Construção não suportada: {token!r}")
            if self.peek() in ("?", "*", "+"):
                suffix = self.take()
                node = {"?": Optional, "*": ZeroOrMore, "+": OneOrMore}[suffix](node)
            elements.append(node)
        if not elements:
            raise ValueError("Alternativa vazia inesperada")
        return elements[0] if len(elements) == 1 else Sequence(*elements)


def svg(stream, language, all_rules):
    expression = Expression(stream, language, all_rules)
    diagram = Diagram(expression.choice())
    assert expression.peek() is None
    output = io.StringIO()
    diagram.writeStandalone(output.write)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    folder = ROOT / "docs/diagramas"
    folder.mkdir(parents=True, exist_ok=True)
    outputs = {}
    atlas = ['<!doctype html><html lang="pt-BR"><meta charset="utf-8">',
             '<title>TP1 — Atlas das regras léxicas</title>',
             '<style>body{font:16px system-ui;margin:40px;color:#172b42}h1,h2,h3{color:#173f69}article{border-top:1px solid #ccd6e0;padding:16px 0;overflow:auto}pre{background:#f3f5f8;padding:14px;white-space:pre-wrap}a{color:#17549c}svg{max-width:none}nav a{margin-right:20px}</style>',
             '<h1>TP1 · C e Java 20</h1><p>Ferrovias geradas das gramáticas fixadas. Leia da esquerda para a direita. ',
             'Bifurcações são alternativas; desvios vazios são opcionais; retornos representam repetição. ',
             'Caixas arredondadas representam literais/conjuntos; caixas retangulares referenciam outras regras. ',
             '<code>~[... ]</code> significa qualquer caractere fora do conjunto. As barras e aspas seguem ANTLR, não são uma nova sintaxe.</p>',
             '<p>Os fragmentos são expandidos abaixo, uma vez por linguagem. Clique no nome de uma referência para navegar.</p><nav>']
    for language, targets in TARGETS.items():
        for target in targets:
            atlas.append(f'<a href="#{language}-{target}">{language} · {target}</a>')
    atlas.append('</nav>')
    for language, targets in TARGETS.items():
        all_rules = rules(language)
        names = list(targets)
        for target in targets:
            for name in dependencies(all_rules, target):
                if name not in names:
                    names.append(name)
        atlas.append(f'<h2>{language}</h2>')
        for name in names:
            drawing = svg(all_rules[name], language, all_rules)
            if name in targets:
                outputs[folder / f'{language}-{name}.svg'] = drawing
            atlas += [f'<article id="{language}-{name}"><h3>{name}</h3>', drawing,
                      '<pre>' + html.escape(name + ' : ' + ' '.join(all_rules[name]) + ';') + '</pre></article>']
    atlas.append('</html>')
    outputs[folder / 'atlas.html'] = '\n'.join(line.rstrip() for line in '\n'.join(atlas).splitlines()) + '\n'
    for path, content in outputs.items():
        if args.check:
            assert path.read_text(encoding="utf-8") == content, f"Diagrama desatualizado: {path.name}"
        else:
            path.write_text(content, encoding="utf-8")
    print("OK: seis diagramas principais e atlas completo de dependências.")


if __name__ == '__main__':
    main()
