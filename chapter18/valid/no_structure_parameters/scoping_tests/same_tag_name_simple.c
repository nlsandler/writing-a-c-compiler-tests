struct pair1 {
    int x;
    int y;
};

struct pair2 {
    double x;
    char y;
};

int main(void) {
    struct pair1 p1 = { 1, 2};
    struct pair2 p2 = { 3.0, 4};
    return p1.x + p2.x;
}