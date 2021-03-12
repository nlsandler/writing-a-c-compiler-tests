int main() {
    int i = 2147483642;
    do ; while ((i = i - 5) >= 256);

    return i;
}
