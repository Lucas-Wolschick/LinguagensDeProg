import java.nio.charset.StandardCharsets;
import java.util.*;
import org.antlr.v4.runtime.*;

/** Uma entrada por linha: id, classe, base64. Saída JSONL com tokens e erros reais. */
public class LexerProbe {
    static String quote(String s) {
        StringBuilder b = new StringBuilder("\"");
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"': b.append("\\\""); break;
                case '\\': b.append("\\\\"); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:
                    if (c < 32) b.append(String.format("\\u%04x", (int)c));
                    else b.append(c);
            }
        }
        return b.append('"').toString();
    }

    public static void main(String[] args) throws Exception {
        System.setOut(new java.io.PrintStream(System.out, true, StandardCharsets.UTF_8));
        Scanner input = new Scanner(System.in, StandardCharsets.UTF_8);
        while (input.hasNextLine()) {
            String[] fields = input.nextLine().split("\t", -1);
            String source = new String(Base64.getDecoder().decode(fields[2]), StandardCharsets.UTF_8);
            Lexer lexer = (Lexer) Class.forName(fields[1]).getConstructor(CharStream.class)
                .newInstance(CharStreams.fromString(source));
            List<String> errors = new ArrayList<>();
            lexer.removeErrorListeners();
            lexer.addErrorListener(new BaseErrorListener() {
                @Override public void syntaxError(Recognizer<?, ?> recognizer, Object symbol,
                        int line, int column, String message, RecognitionException exception) {
                    errors.add("{\"line\":" + line + ",\"column\":" + column
                        + ",\"message\":" + quote(message) + "}");
                }
            });
            List<String> output = new ArrayList<>();
            Token token;
            do {
                token = lexer.nextToken();
                String type = token.getType() == Token.EOF ? "EOF"
                    : lexer.getVocabulary().getSymbolicName(token.getType());
                if (type == null) type = lexer.getVocabulary().getDisplayName(token.getType());
                output.add("{\"type\":" + quote(type) + ",\"text\":" + quote(token.getText())
                    + ",\"start\":" + token.getStartIndex() + ",\"stop\":" + token.getStopIndex()
                    + ",\"channel\":" + token.getChannel() + "}");
            } while (token.getType() != Token.EOF);
            System.out.println("{\"id\":" + quote(fields[0]) + ",\"tokens\":["
                + String.join(",", output) + "],\"errors\":[" + String.join(",", errors) + "]}");
        }
    }
}
