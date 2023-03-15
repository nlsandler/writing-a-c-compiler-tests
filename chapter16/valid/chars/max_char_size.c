int rand(void);

int main(void) {
    for (int i = 0; i < 10; i = i + 1) {
        unsigned char c = rand();
        int casted = (int) c;
        if (casted >= 256) {
            return 1;
        }
    }
    return 0;
}