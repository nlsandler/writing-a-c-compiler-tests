struct pair {
    int a;
    int b;
};

struct pair return_pair() {
    struct pair result = {1, 2};
    return result;
}

int main() {
    return_pair().a = 5;
    return 0;
}