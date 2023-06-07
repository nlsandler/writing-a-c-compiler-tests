/* Test comparing pointers with == and != */

int main(void) {
    int a;
    int b;

    int *a_ptr = &a;
    int *a_ptr2 = &a;
    int *b_ptr = &b;

    int eq_true = a_ptr == a_ptr2;
    int eq_false = a_ptr == b_ptr;


    int neq_true = a_ptr != b_ptr;
    int neq_false = a_ptr != a_ptr2;

    // if you assign dereferenced value of one pointer to another, the pointers
    // themselves are still not equal
    *b_ptr = *a_ptr;
    int neq_after_deref_assignment = a_ptr != b_ptr;

    // if you assign one pointer to another, they will be equal afterwards,
    // just like any other variable
    b_ptr = a_ptr;
    int eq_after_assignment = b_ptr == a_ptr;

    return eq_true && !eq_false && neq_true && !neq_false
        && eq_after_assignment && neq_after_deref_assignment;
}