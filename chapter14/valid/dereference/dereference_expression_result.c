/* Make sure we can dereference any expression of pointer type,
 * not just variables */

int *return_pointer() {
    static int var = 10;
    return &var;
}

int main() {
    int val = 100;
    int *ptr_var = &val;

    // First try reading pointers that result from function calls or ternary expressions
    // return_pointer() evaluates to 10, the ternary expression evaluates to 100
    if (*return_pointer() + *(0 ? return_pointer() : ptr_var) != 110)
        return 0;

    // Now try to update values through these pointers
    *return_pointer() = 20;
    *(1 ? ptr_var : return_pointer()) = 30;

    // Validate that the values of the pointed-to objects were updated
    if (*return_pointer() != 20 || *ptr_var != 30)
        return 0;

    return 1;
}