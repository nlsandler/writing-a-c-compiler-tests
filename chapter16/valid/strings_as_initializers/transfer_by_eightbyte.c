int strcmp(char *s1, char *s2);

// if you initialize arrays 4 or 8 bytes at a time,
// make sure you don't overrrun neighboring memory

int main()
{
    char strings[2][13] = {"abcdefghijkl", "z"};
    if (strcmp(strings[0], "abcdefghijkl"))
        return 1;

    if (strings[1][0] != 'z')
        return 2;
    for (int i = 1; i < 13; i = i + 1)
    {
        if (strings[1][i])
            return 3;
    }
    return 0;
}