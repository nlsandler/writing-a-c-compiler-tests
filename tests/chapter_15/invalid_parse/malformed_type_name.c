int main(void) {
    int a = 4;
    int *foo = &a;
    int *bar[3] = (*[3]) foo;
    return 0;
}