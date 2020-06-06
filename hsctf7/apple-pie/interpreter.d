import std;
import core.stdc.stdlib : exit;

enum long INF = long.max/5;

// https://esolangs.org/wiki/Apple_Pie

void main(string[] args) {
  if (args.length != 2) exit(1);

  string[] code = File(args[1]).byLine.map!strip.map!(to!string).array;

  string output = "";
  long[string] variables;

  void answer() {
    output.writeln;
    long n = output.length/3;
    foreach(i; 0..n) {
      output[i*3..(i+1)*3].find!"a!='0'".to!string.to!long.to!char.write;
    }
    writeln;
  }

  void eat(ref string[] chunks) {
    chunks = chunks[1..$];
  }

  long eval(ref string[] chunks) {
    // chunks.writeln;
    if (chunks.front == "FXFXFX") {
      eat(chunks);
      long x = eval(chunks);
      string op = chunks.front;
      eat(chunks);
      long y = eval(chunks);
      if (op == "+") return x + y;
      if (op == "-") return x - y;
      if (op == "*") return x * y;
      if (op == "/") return x / y;
      if (op == "^") return x ^^ y;
      assert(false);
    } else if (chunks.front == "$XF") {
      eat(chunks);
      string name = chunks.front;
      eat(chunks);
      return variables[name];
    } else {
      string value = chunks.front;
      eat(chunks);
      return value.to!long;
    }
  }

  void exec(ref string[] chunks) {
    // chunks.writeln;
    if (chunks.front == "AX") {
      eat(chunks);
      long x;
      if (chunks.front.isNumeric) {
        x = chunks.front.to!long - 1;
        eat(chunks);
      } else {
        x = eval(chunks);
      }
      output ~= x.to!string.retro.to!string;
    } else if (chunks.front == "BX") {
      eat(chunks);
      long x = eval(chunks);
      // comment (ignored)
    } else if (chunks.front == "DXDX") {
      eat(chunks);
      string name = chunks.front;
      eat(chunks);
      long value = eval(chunks);
      variables[name] = value;
    } else if (chunks.front == "EepbeepQX") {
      eat(chunks);
      long[] ts = chunks.front.map!(to!string).map!(to!long).array;
      eat(chunks);
      long x = 0;
      foreach(t; ts) {
        x *= 3;
        x += t;
      }
      string[] repeatedChunks = chunks.until("C").array;
      chunks = chunks.find("C").drop(1).array;
      foreach(i; 0..x) {
        string[] tmp = repeatedChunks.dup;
        while(!tmp.empty) exec(tmp);
      }
    } else if (chunks.front == "C") {
      assert(false);
    } else if (chunks.front == "!!!") {
      eat(chunks);
      answer();
      exit(0);
    } else {
      assert(false);
    }
  }

  while(true) {
    exec(code);
  }
}
