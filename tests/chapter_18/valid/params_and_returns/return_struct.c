struct pair {
    char x;
    long y;
};

struct pair return_pair(void) {
    struct pair ret = { 1, 11l };
    return ret;
}

int main(void) {
    return return_pair().y;
}