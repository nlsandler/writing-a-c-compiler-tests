void foo(void) {
    return;
}

int main(void) {
    int a = 3;
    int flag = 4;
    flag ? foo() : (a = 3);
    return 0;
}