int strcmp(char *s1, char *s2);

int main(void)
{
    char nested[3][3] = {"yes", "no", "ok"};
    char *whole_array = (char *)nested;
    char *word1 = (char *)nested[0];
    char *word2 = (char *)nested[1];
    char *word3 = (char *)nested[2];
    // all strcmp calls should return 0
    return strcmp(whole_array, "yesno") || strcmp(word1, "yesno") || strcmp(word2, "no") || strcmp(word3, "ok");
}