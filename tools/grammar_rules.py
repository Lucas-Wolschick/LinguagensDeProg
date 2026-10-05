"""Leitura das produções usadas no estudo; não é um parser geral de ANTLR."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "C": ["StringLiteral", "IntegerConstant", "FloatingConstant"],
    "Java": ["StringLiteral", "IntegerLiteral", "FloatingPointLiteral"],
}
# Preserva literais/classes antes de descartar comentários, inclusive '\\' e '\''.
TOKEN = re.compile(r"\s+|//[^\n]*|/\*[\s\S]*?\*/|'(?:\\.|[^'\\])*'|\[(?:\\.|[^\]\\])*\]|[A-Za-z_][A-Za-z_0-9]*|.")


def tokens(source):
    return [m.group() for m in TOKEN.finditer(source)
            if not m.group().isspace() and not m.group().startswith(("//", "/*"))]


def rules(language):
    stream = tokens((ROOT / f"{language}.g4").read_text(encoding="utf-8"))
    result = {}
    for i in range(len(stream) - 1):
        name = stream[i]
        if name[0].isupper() and name.isidentifier() and stream[i + 1] == ":":
            end = stream.index(";", i + 2)
            result[name] = stream[i + 2:end]
    return result


def dependencies(all_rules, root):
    found = []

    def visit(name):
        if name in found:
            return
        found.append(name)
        for token in all_rules[name]:
            if token in all_rules:
                visit(token)

    visit(root)
    return found


def make_probes(output):
    """Expõe cada regra/fragmento isolado sem alterar seu corpo ou dependências."""
    for language, targets in TARGETS.items():
        all_rules = rules(language)
        for root in targets:
            name = f"Probe{language}{root}"
            lines = [f"lexer grammar {name};", f"Selected : {root};"]
            for dependency in dependencies(all_rules, root):
                lines.append(f"fragment {dependency} : {' '.join(all_rules[dependency])};")
            (output / f"{name}.g4").write_text("\n".join(lines) + "\n", encoding="utf-8")
