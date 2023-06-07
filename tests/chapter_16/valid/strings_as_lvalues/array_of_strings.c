int strcmp(char *s1, char *s2);

int main(void)
{
    char *strings[3] = {"yes", "no", "maybe"};
    return strcmp(strings[0], "yes") && strcmp(strings[1], "no") && strcmp(strings[2], "maybe");
}