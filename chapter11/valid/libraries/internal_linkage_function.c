/* A function with internal linkage can be declared multiple times */
static int my_fun();

int call_static_my_fun() {
    return my_fun();
}

int call_static_my_fun_2() {
    /* when you declare a function at block scope,
     * it takes on the linkage of already-visible declaration
     */
    int my_fun();
    return my_fun();
}

extern int my_fun();

static int my_fun();

int my_fun() {
    static int i = 0;
    i = i + 1;
    return i;
}