#include <stdio.h>
#include <stdlib.h>

void final(int x) {
  x = x * 10;

  printf("In Final X is %d\n", x);
}

void final2_1(int x) {
  x = x * 10;

  printf("In Final2_1 X is %d\n", x);
}

void final2_2(int x) {
  x = x * 10;

  printf("In Final2_2 X is %d\n", x);
}
void final2_3(int x) {
  x = x * 10;

  printf("In Final2_3 X is %d\n", x);
}

void f1_1(int x) { final(x); }

void f1_2(int x) { final(x); }

void f1_3(int x) { final(x); }

void f2_1(int x) { final2_1(x); }

void f2_2(int x) { final2_2(x); }

void f2_3(int x) { final2_3(x); }

void f2_4(int x) { final2_3(x); }

void f1(int x) {
  int a = 22;
  int b = 33;
  int c = 44;

  if (x > a && x < c)
    f1_1(c * x - (a + x));
  else if (x < 0)
    f1_2(0);
  else
    f1_3(a + b + c + x);
}

void f2(int x, int y) {
  int a = 2;
  int b = 3;
  int c = 44;

  if (x > 10 && x < 100)
    f2_1(c - a);
  else if (x > 100)
    f2_2(0);
  else if (x + y - 10 > 0)
    f2_3(y + 10);
  else
    f2_4(a + b + c + x);
}

void bbb1_1(int x) {
  x = x * 10;

  printf("In BBB1_1 X is %d\n", x);
}

void bbb1_2(int x, int y) {
  x = x * 10;

  printf("In BBB1_2 X is %d\n", x);
}

void bbb2_1(int x) {
  x = x * 10;

  printf("In BBB2_1 X is %d\n", x);
}

void bbb2_2(int x, int y) {
  x = x * 10;

  printf("In BBB2_2 X is %d\n", x);
}

void bb2(int x, int y) {
  int a = 2;
  int b = 3;

  if (x < 10) {
    bbb2_1(a + 2 * x);
  } else
    bbb2_2(b, y + x);
}

void bb1(int x) {
  int a = 2;
  int b = 3;
  int c = 4;

  if (x < 10) {
    bbb1_1(a + 2 * x);
  } else
    bbb1_2(b - x, c + 2 * x);
}

void b1(int x) { bb1(x); }

void b2(int x, int y) { bb2(x, y); }

void bar(int x) {
  int a = 22;
  int b = 33;
  int c = 44;

  if (x < 10)
    b1(a + x);
  else
    b2(x - b, c + x);
}

void foo(int x) {
  int a = 222;
  int b = 333;
  int c = 444;

  if (x < 100) {
    f1(a + x);
  } else
    f2(x - b, c + x);
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    puts("Please just add one arbitrary integer as a command line argument");
    exit(-1);
  }

  int x = atoi(argv[1]);

  if (x == 392)
    bar(x);
  else { // x != 392
    foo(x);
  }
  return 0;
}
