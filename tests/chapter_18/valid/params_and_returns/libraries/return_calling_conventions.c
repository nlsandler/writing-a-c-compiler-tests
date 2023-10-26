#include "return_calling_conventions.h"

struct one_int return_int_struct(void) {
    struct one_int retval = {1, 2};
    return retval;
}

struct twelve_bytes return_two_int_struct(void) {
    struct twelve_bytes retval = {10, "12345678"};
    return retval;
}

struct one_xmm return_double_struct(void) {
    struct one_xmm retval = {100.625};
    return retval;
}
struct two_xmm return_two_double_struct(void) {
    struct two_xmm retval = {{8.8, 7.8}};
    return retval;
}
struct xmm_and_int return_mixed(void) {
    struct xmm_and_int retval = {{10.0}, "ab"};
    return retval;
}
struct int_and_xmm return_mixed2(void) {
    struct int_and_xmm retval = {127, 34e43};
    return retval;
}
struct memory return_on_stack(void) {
    struct memory retval = {1.25, "xy", 100l, 44};
    return retval;
}

int f(char c, double d) {
    if (c == 'p' && d == 4.56)
        return 0;
    return 1;
}

struct memory pass_and_return_regs(int i, double d, struct int_and_xmm strct,
                                   char c, struct two_ints t_i, long l,
                                   struct one_int_exactly o_i_e, char c2) {
    // include stack variables to make sure they don't overwrite return value
    // pointer or vice versa
    int local1 = i * 2;
    double local2 = d * 2;
    struct memory retval = {0, {0, 0, 0}, 0, 0};

    if (local1 != 12 || local2 != 8.0) {
        retval.i = 1;
        return retval;
    }
    int local3 = f(strct.c, strct.d);
    if (local3) {
        retval.i = 2;
        return retval;
    }
    if (c != 5) {
        retval.i = 3;
        return retval;
    }
    if (t_i.c != '_' || t_i.arr[0] != 5 || t_i.arr[1] != 6 || t_i.arr[2] != 7) {
        retval.i = 4;
        return retval;
    }
    if (l != 77) {
        retval.i = 5;
        return retval;
    }
    if (o_i_e.l != 567890) {
        retval.i = 6;
        return retval;
    }
    if (c2 != 99) {
        retval.i = 7;
        return retval;
    }
    retval.l = 100;
    return retval;
}