int strcmp(char *s1, char *s2);

int main() {
    char *strings[3] = { "yes", "no", "maybe"};
    return strcmp(strings[1],"no");
}