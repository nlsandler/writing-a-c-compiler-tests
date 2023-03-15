int main(void) {
    int x = 10;
    // shouldn't corrupt anything if we add a null byte here,
    // so this is just to make sure it type checks
    static char letters[4] = "abcd";
    int y = 12;
    return x == 10 && y == 12 && letters[0] == 'a' && letters[1] == 'b'
        && letters[2] == 'c' && letters[3] == 'd';
}