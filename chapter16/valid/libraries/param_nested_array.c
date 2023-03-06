int foo(int arg[1][2]) {
    int elem[2] = {3, 9};
    arg[0][1] = elem[1];
    arg[0][0] = elem[0];
    return 0;
}