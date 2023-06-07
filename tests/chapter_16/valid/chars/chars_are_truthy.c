// use chars in contexts that treat them as boolean values (&&, ||, controlling expressions)

int main(void)
{
    char c = 0;
    if (c)
        return 1;
    unsigned char uc = 100;
    if (!(c || uc))
        return 2;

    char signed s = -1;
    if (!(uc && s))
        return 3;

    int count = 0;
    // note: even if s - 1 < -128, this behavior is well-defined,
    // b/c we promote to int, subtract, then truncate to char
    for (; s; s = s - 1)
        count = count + 1;

    if (count != 255 || s != 0)
        return 4;

    return 0;
}