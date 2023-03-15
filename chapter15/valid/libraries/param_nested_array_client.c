int foo(int arg[1][2]);

int main(void) {
    int arg[1][2] = {{1, 2}};
    foo(arg);
    return arg[0][1] + arg[0][0];
}