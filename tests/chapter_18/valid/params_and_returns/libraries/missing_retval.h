struct big {
    char arr[25];
};

// make sure we correctly handle calls to functions with return values
// passed on stack, even if return statement is missing,
// as long as caller doesn't use return value
struct big missing_return_value(int *i);