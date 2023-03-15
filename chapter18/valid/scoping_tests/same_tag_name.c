struct pair1 {
    int x;
    int *y;
};

struct pair2 {
    void *x;
    double y[4];
};

int main(void) {
    struct pair1 p1 = { 3, &(p1.x) };
    struct pair2 p2 = { &p1, {1.0, 2.0, 3.0, 4.0} };
    return *p1.y + p2.y[1] + ((struct pair1 *)p2.x)->x;
}