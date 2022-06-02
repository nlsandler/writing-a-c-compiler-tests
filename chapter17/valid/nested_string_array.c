int strcmp(char *s1, char *s2);

int main() {
    char nested[3][3] = { "yes", "no", "ok"};

    return strcmp(nested[0], "yesno");
}