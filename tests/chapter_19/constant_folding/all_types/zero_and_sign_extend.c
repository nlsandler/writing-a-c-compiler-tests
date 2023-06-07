/* Test that we can constant-fold conversions from shorter to longer ints
 * NOTE we can get better coverage of this once we implement copy propagation,
 * so we can look at conversions of chars and negative numbers,
 * and can look for instructions of the form mov $const, %eax
 * or mov whatever(%rip), %xmm0.
 * With constant folding alone the assembly is indistinguishable between folded and non-folded
 * zero-extended conversions.
 */

long target_uint_to_long(void) {
    return (long) 4294967295U;
}

unsigned long target_uint_to_ulong(void) {
    return (unsigned long) 4294967295U;
}

unsigned long target_int_to_ulong(void) {
    return (unsigned long) 2147483647;
}

long target_int_to_long(void) {
    return (long) 1;
}

int main(void) {
    if (target_uint_to_long() != 4294967295l) {
        return 1;
    }

    if (target_uint_to_ulong() != 4294967295ul) {
        return 2;
    }

    if (target_int_to_ulong() != 2147483647l) {
        return 3;
    }

    if (target_int_to_long() != 1l) {
        return 4;
    }

    return 0;
}