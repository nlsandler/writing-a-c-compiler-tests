int i = 0;

void foo() {
    i = 100;
}

int main() {
    for (foo(); ;)
        return i;
    return 0;
}