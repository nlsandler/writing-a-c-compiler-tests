int i = 0;

void foo() {
    i = 100;
}

int main() {
    for (; i < 10; foo())
        ;
    return i;
}