int main(void) {

    // test that character constants have integer type, not character type;
    // we test this here because we couldn't in the previous chapter
    if (sizeof 'a' != 4) {
        return 1;
    }
    char c;
    if (sizeof c != 1) {
        return 2;
    }
    // TODO finish
    return 0;
}