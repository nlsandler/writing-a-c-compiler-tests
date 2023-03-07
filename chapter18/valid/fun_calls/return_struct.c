struct pair {
    char x;
    long y;
};

struct pair return_pair() {
    struct pair ret = { 1, 11l };
    return ret;
}

int main() {
    return return_pair().y;
}