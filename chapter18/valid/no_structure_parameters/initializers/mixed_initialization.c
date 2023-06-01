struct triple {
    long one;
    double two;
    char three;
};

int main(void) {
    struct triple example = {1l, 2.0, 3};
    struct triple array[3] = { {4l, 5.0, 6}, example, example};
    return array[0].one + array[2].three;
}