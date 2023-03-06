int main() {
    int x = 10;
    // make sure null byte here doesn't corrupt ints on either side
    char letters[4] = "abcd";
    int y = 12;
    return x == 10 && y == 12 && letters[0] == 'a' && letters[1] == 'b'
        && letters[2] == 'c' && letters[3] == 'd';
}