void foo() {
    return;
}

int main() {
    for (int i = 0; foo(); )
        ;
    return 0;
}