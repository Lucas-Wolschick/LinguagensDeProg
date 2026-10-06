import org.antlr.v4.runtime.*;
import java.nio.file.*; import java.util.*;
public class Tokens {
  public static void main(String[] a) throws Exception {
    List<String> lines = Files.readAllLines(Paths.get(a[0]), java.nio.charset.StandardCharsets.UTF_8);
    String hdr=null; StringBuilder sb=null;
    for (String ln : lines) {
      if (ln.startsWith("@@@")) { if (hdr!=null) go(hdr, sb.toString()); hdr=ln.substring(4); sb=new StringBuilder(); }
      else { if (sb.length()>0) sb.append("\n"); sb.append(ln); }
    }
    if (hdr!=null) go(hdr, sb.toString());
  }
  static void go(String hdr, String txt) throws Exception {
    String lang = hdr.substring(0,1);
    System.out.println("### " + hdr + "   input: " + txt.replace("\n","⏎"));
    Lexer lx = (Lexer)Class.forName(lang.equals("J")?"Java20Lexer":"CLexer").getConstructor(CharStream.class).newInstance(CharStreams.fromString(txt));
    lx.removeErrorListeners();
    lx.addErrorListener(new BaseErrorListener(){ public void syntaxError(Recognizer<?,?> r,Object o,int l,int c,String m,RecognitionException e){ System.out.println("    line " + l+":"+c+" "+m.replace("\n","\n"));} });
    for (Token t : lx.getAllTokens()) { if (t.getChannel()!=0) continue;
      System.out.println("    " + lx.getVocabulary().getSymbolicName(t.getType()) + "  " + t.getText().replace("\n","\n")); }
  }
}
