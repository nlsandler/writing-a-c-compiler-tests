// make sure we include null byte on end of char array initialized from string
// both nested and not, static and automatic, when we have enough space

int strcmp(char *s1, char *s2);

unsigned char flat[4] = "dog";
char nested[2][4] = {"yes", "yup"};

int main(void)
{
    if (flat[0] != 'd' || flat[1] != 'o' || flat[2] != 'g' || flat[3])
        return 1;

    if (strcmp(nested[0], "yes") || strcmp(nested[1], "yup"))
        return 2;

    // define some with automatic storage duration
    char flat_auto[2] = "x";
    if (strcmp(flat_auto, "x"))
        return 3;
    char nested_auto[2][2][2] = {{"a", "b"}, {"c", "d"}};
    for (int i = 0; i < 1; i = i + 1)
        for (int j = 0; j < 1; j = j + 1)
        {

            char expected = 'a' + i * 2 + j;
            if (nested_auto[i][j][0] != expected)
                return 4;
            if (nested_auto[i][j][1])
                return 5;
        }
    return 0;
}