char nested[3][3] = {"yes", "no", "ok"};

int main() {
    char *expected = "yesno";
    for (int i = 0; i < 2; i = i + 1)
        for (int j = 0; j < 3; j = j + 1) {
            if (i*3 + j > 5)
                continue;
            if (nested[i][j] != expected[i*3+j])
                return 0;
        }
    return 1;
}