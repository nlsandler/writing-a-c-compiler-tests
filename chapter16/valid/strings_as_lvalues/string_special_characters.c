int main(void)
{
    char *c = "\a\b";
    return c[0] == 7 && c[1] == 8 && c[2] == 0;
}