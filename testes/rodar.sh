#!/usr/bin/env bash
# Gera os lexers com ANTLR 4.13.2 e tokeniza todas as entradas de entradas.txt.
# Uso (Git Bash, na pasta testes/):  ./rodar.sh > resultado.txt
# Requer Java 11+ e curl.
set -e
cd "$(dirname "$0")"
JAR=antlr-4.13.2-complete.jar
SEP=":"; case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) SEP=";";; esac

[ -f "$JAR" ] || curl -sfLO "https://www.antlr.org/download/$JAR"

mkdir -p build/java build/c
cp ../Java20Lexer.g4 build/java/
cp ../C.g4 build/c/
(cd build/java && java -jar "../../$JAR" Java20Lexer.g4 && javac -cp "../../$JAR" *.java)
(cd build/c    && java -jar "../../$JAR" C.g4          && javac -cp "../../$JAR" *.java)
javac -cp "$JAR" -d build Tokens.java

java -Dstdout.encoding=UTF-8 -cp "$JAR${SEP}build${SEP}build/java${SEP}build/c" Tokens entradas.txt
