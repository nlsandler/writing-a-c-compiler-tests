int return_pointer_val(int *arg)
{
    static int *static_ptr = 0;
    if (!static_ptr)
        static_ptr = arg;

    return *static_ptr;
}

int main(void)
{
    int x = 1;
    int *null = 0;
    int result1 = return_pointer_val(&x);   // result1 is 1
    x = 4;                                  // not dead b/c x is aliased, and is used in fun call below
    int result2 = return_pointer_val(null); // return 4 (we ignore null, return value of x)
    return result1 + result2;
}