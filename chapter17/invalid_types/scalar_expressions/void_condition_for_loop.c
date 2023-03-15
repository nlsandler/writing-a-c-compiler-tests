void foo(void) {
    return;
}

int main(void) {
    for (int i = 0; foo(); )
        ;
    return 0;
}