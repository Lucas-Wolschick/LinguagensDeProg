"""Gera/compila ANTLR4 e registra a análise léxica, sem invocar parsers."""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import urllib.request
from collections import Counter
from pathlib import Path
from grammar_rules import ROOT, TARGETS, make_probes

VERSION = "4.13.2"
JAR_SHA256 = "eae2dfa119a64327444672aff63e9ec35a20180dc5b8090b7a6ab85125df4d76"


def run(command, **kwargs):
    return subprocess.run(command, cwd=ROOT, check=True, encoding="utf-8", **kwargs)


def single_token(result, source, kind):
    tokens = result["tokens"]
    return (not result["errors"] and len(tokens) == 2 and tokens[-1]["type"] == "EOF"
            and tokens[0]["type"] == kind and tokens[0]["text"] == source
            and tokens[0]["start"] == 0 and tokens[0]["stop"] == len(source) - 1)


def code(value):
    return "`" + json.dumps(value, ensure_ascii=False).replace("|", "&#124;") + "`"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, help="JAR oficial já baixado (opcional)")
    parser.add_argument("--check", action="store_true", help="Confere resultados versionados sem sobrescrevê-los")
    args = parser.parse_args()
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    jar = args.jar.resolve() if args.jar else build / f"antlr-{VERSION}-complete.jar"
    if not jar.exists():
        if args.jar:
            raise SystemExit(f"JAR não encontrado: {jar}")
        urllib.request.urlretrieve(f"https://www.antlr.org/download/antlr-{VERSION}-complete.jar", jar)
    if hashlib.sha256(jar.read_bytes()).hexdigest() != JAR_SHA256:
        raise SystemExit("SHA-256 do JAR não corresponde à versão fixada.")
    lock = json.loads((ROOT / "vendor/sources.json").read_text(encoding="utf-8"))
    for filename, digest in lock["sha256"].items():
        if hashlib.sha256((ROOT / "vendor" / filename).read_bytes()).hexdigest() != digest:
            raise SystemExit(f"Fonte original alterada: {filename}")
    original_c = (ROOT / "vendor/C.g4").read_text(encoding="utf-8")
    original_java = (ROOT / "vendor/Java20Lexer.g4").read_text(encoding="utf-8")
    assert (ROOT / "C.g4").read_text(encoding="utf-8") == original_c
    assert (ROOT / "Java.g4").read_text(encoding="utf-8") == original_java.replace(
        "lexer grammar Java20Lexer;", "lexer grammar Java;")
    generated = build / "generated"
    generated.mkdir(exist_ok=True)
    classes = build / "classes"
    classes.mkdir(exist_ok=True)
    make_probes(generated)
    # C.g4 é combinada; seu parser é gerado, mas nunca instanciado nos testes.
    grammars = [ROOT / "C.g4", ROOT / "Java.g4", *sorted(generated.glob("Probe*.g4"))]
    run(["java", "-jar", str(jar), "-Dlanguage=Java", "-encoding", "UTF-8",
         "-no-listener", "-no-visitor", "-Xexact-output-dir", "-o", str(generated),
         *map(str, grammars)])
    sources = sorted(generated.glob("*.java")) + [ROOT / "tools/LexerProbe.java"]
    run(["javac", "-encoding", "UTF-8", "-cp", str(jar), "-d", str(classes), *map(str, sources)])
    cases = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8"))
    assert len({c["id"] for c in cases}) == len(cases), "IDs repetidos"
    coverage = Counter((c["language"], c["rule"], c["accepted"]) for c in cases if c["group"] == "principal")
    for language, targets in TARGETS.items():
        for target in targets:
            for accepted in (False, True):
                assert coverage[language, target, accepted] == 2, "São exigidos 2 aceitos e 2 rejeitados por regra"
    requests = []
    for c in cases:
        assert c["rule"] in TARGETS[c["language"]]
        if c["group"] == "principal":
            assert len(c["input"]) >= 5
        encoded = base64.b64encode(c["input"].encode()).decode()
        full = "CLexer" if c["language"] == "C" else "Java"
        for mode, name in [("isolated", f"Probe{c['language']}{c['rule']}"), ("full", full)]:
            requests.append(f"{c['id']}:{mode}\t{name}\t{encoded}")
    process = run(["java", "-Dfile.encoding=UTF-8", "-cp", os.pathsep.join([str(classes), str(jar)]),
                   "LexerProbe"], input="\n".join(requests) + "\n", capture_output=True)
    responses = {r["id"]: r for r in map(json.loads, process.stdout.splitlines())}
    results = []
    for case in cases:
        isolated = responses[case["id"] + ":isolated"]
        full = responses[case["id"] + ":full"]
        actual = single_token(isolated, case["input"], "Selected")
        assert actual == case["accepted"], f"Resultado inesperado: {case['id']}: {isolated}"
        kind = "Constant" if case["language"] == "C" and case["rule"] != "StringLiteral" else case["rule"]
        if actual:
            assert single_token(full, case["input"], kind), f"Lexer completo divergiu: {case['id']}"
        if "full_types" in case:
            assert [t["type"] for t in full["tokens"]] == case["full_types"] + ["EOF"], case["id"]
        results.append({**case, "actual": actual, "isolated": isolated, "full": full})
    data = {"antlr": VERSION, "jar_sha256": JAR_SHA256, "source_commit": lock["commit"], "results": results}
    serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    evidence = ROOT / "docs/resultados.json"
    lines = ["# Saídas reais do ANTLR4", "", f"ANTLR {VERSION}; {len(cases)} casos, duas execuções por caso.", "",
             "Gerado por `python tools/run_tests.py`. Entradas e textos usam a notação JSON: `\\n` é uma quebra de linha; `\\\\n` é barra seguida de n.", "",
             "Aceita = um único token da regra isolada cobrindo toda a entrada, sem erros, seguido de EOF. Todos os tokens, inclusive ocultos, entram na verificação.", "",
             "O lexer completo de C emite `Constant` tanto para inteiro quanto para real. A sonda isolada distingue os fragmentos. Não se executa parser.", ""]
    for c in results:
        lines += [f"## {c['id']} — {c['language']} / {c['rule']}", "",
                  f"Entrada: {code(c['input'])} · **{'Aceita' if c['actual'] else 'Rejeitada'}** · {c['group']}", "", c["reason"], ""]
        for mode, label in [("full", "Lexer completo"), ("isolated", "Regra isolada (Selected)")]:
            r = c[mode]
            stream = "; ".join(f"`{t['type']}` {code(t['text'])} [{t['start']}..{t['stop']}; canal {t['channel']}]" for t in r["tokens"])
            lines += [f"**{label}:** {stream}", ""]
            lines += ["Erros: nenhum" if not r['errors'] else "Erros:", ""]
            lines += [f"- linha {e['line']}, coluna {e['column']}: {code(e['message'])}" for e in r["errors"]]
            lines += [""]
    markdown = "\n".join(lines)
    tables = []
    for language, targets in TARGETS.items():
        for target in targets:
            tables += [f"### {language} — {target}", "",
                       "| ID | Entrada | Resultado | Tokens do lexer completo (antes de EOF) | Erros léxicos | Explicação |",
                       "|---|---|---|---|---|---|"]
            for c in results:
                if c['group'] != 'principal' or c['language'] != language or c['rule'] != target:
                    continue
                stream = '; '.join(f"`{t['type']}` (`{t['text']}`)" for t in c['full']['tokens'] if t['type'] != 'EOF') or 'nenhum'
                tables.append(f"| {c['id']} | `{c['input']}` | {'Aceita' if c['actual'] else 'Rejeitada'} | {stream} | {len(c['full']['errors'])} | {c['reason']} |")
            tables.append("")
    report_path = ROOT / "docs/RELATORIO.md"
    report = report_path.read_text(encoding="utf-8")
    start, end = '<!-- TABELAS_INICIO -->', '<!-- TABELAS_FIM -->'
    before, remainder = report.split(start)
    _, after = remainder.split(end)
    updated_report = before + start + '\n\n' + '\n'.join(tables) + '\n' + end + after
    if args.check:
        assert evidence.read_text(encoding="utf-8") == serialized, "Resultados JSON desatualizados"
        assert (ROOT / "docs/RESULTADOS.md").read_text(encoding="utf-8") == markdown, "Resultados Markdown desatualizados"
        assert report == updated_report, "Tabelas do relatório desatualizadas"
    else:
        evidence.write_text(serialized, encoding="utf-8")
        (ROOT / "docs/RESULTADOS.md").write_text(markdown, encoding="utf-8")
        report_path.write_text(updated_report, encoding="utf-8")
    print(f"OK: {len(cases)} casos; {len(requests)} execuções; 6 regras; fontes e JAR verificados.")


if __name__ == "__main__":
    main()
