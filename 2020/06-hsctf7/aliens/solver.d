import std;

void main() {
  long H = 500;
  long W = 500;
  long[][] xss = H.iota.array.map!(_ => readln.split.to!(long[]).array).array;

  long[][] yss = new long[][](H+1, W+1);
  foreach(i; 0..H) {
    foreach(j; 0..W) {
      yss[i+1][j+1] += xss[i][j];
      yss[i+1][j+1] += yss[i+1][j];
    }
    foreach(j; 0..W) {
      yss[i+1][j+1] += yss[i][j+1];
    }
  }

  long[][] zss = new long[][](H+1, W+1);
  foreach(i; 0..H) {
    foreach(j; 0..W) {
      if (xss[i][j] == -1) zss[i+1][j+1] += -xss[i][j];
      zss[i+1][j+1] += zss[i+1][j];
    }
    foreach(j; 0..W) {
      zss[i+1][j+1] += zss[i][j+1];
    }
  }

  long f(long i1, long j1, long i2, long j2) {
    return yss[i2][j2] - yss[i1][j2] - yss[i2][j1] + yss[i1][j1];
  }
  long g(long i1, long j1, long i2, long j2) {
    return zss[i2][j2] - zss[i1][j2] - zss[i2][j1] + zss[i1][j1];
  }

  long h(long i1, long j1, long i2, long j2) {
    long x = f(i1, j1, i2, j2);
    if (g(i1, j1, i2, j2)%2 == 1) x *= -1;
    return x;
  }

  BigInt x = 0;
  foreach(i1; 0..H) {
    i1.writeln;
    foreach(j1; 0..W) foreach(i2; i1+1..H+1) foreach(j2; j1+1..W+1) {
      BigInt y = h(i1, j1, i2, j2);
      if (y % 13 == 0) {
         x += y;
      }
    }
  }
  x.writeln;
}
