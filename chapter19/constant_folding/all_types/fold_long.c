/* Test constant folding of operations on long ints.
 * Make sure we correctly handle operations that require all 64 bits.
 * Tests do not involve any overflow, since that's undefined behavior.
 */
long target_add(void) {
    // we can add longs when the result exceeds INT_MAX
    return 2147483647l + 1000l;
}

long target_sub(void) {
    // we can subtract longs when the result is smaller than INT_MIN
    // and upper 32 bits aren't all 1s
    return 1000l - 9223372036854773807l;
}

long target_mult(void) {
    // can multiply longs when the result exceeds INT_MAX
    return 35184372088832l * 4l;
}

long target_div(void) {
    // both operands are larger than INT_MAX
    return 9223372036854775807l / 3147483647l;
}

long target_rem(void) { // both operands are larger than INT_MAX
    return 9223372036854775807l % 3147483647l;
}

long target_complement(void) { // alternating 1s and 0s
    return ~6148914691236517206l;
}

long target_neg(void) {
    // except for most significant bit, upper 32 bits of negated value are all
    // zeros
    return -(9223372036854775716l);
}

int target_not(void) {
    // 2^56 + 2^45 + 2^44
    // lower 32 bits are all zeros
    return !72110370596061184l;
}

int target_eq(void) { return 9223372036854775716l == 9223372036854775716l; }

int target_neq(void) {
    // lower 32 bits of 72110370596061184l are all zeros
    return 72110370596061184l != 0l;
}

int target_gt(void) {
    // compare two values whose lower 32 bits are identical
    return 17592186044416l > 549755813888l; // 2^44 > 2^39
}

int target_ge(void) {
    return 400l >= 399l;
}

int target_lt(void) {
    // compare two values whose lower 32 bits are identical
    return 17592186044416l < 549755813888l; // 2^44 < 2^39
}

int target_le(void) {
    // if we interpreted this as a signed int it would be negative
    return 2147483648l <= 0l; }

int main(void) {

    // binary arithmetic
    if (target_add() != 2147484647l) {
        return 1;
    }
    if (target_sub() != -9223372036854772807) {
        return 2;
    }
    if (target_mult() != 140737488355328l) {
        return 3;
    }
    if (target_div() != 2930395538l) {
        return 4;
    }
    if (target_rem() != 1758008721l) {
        return 5;
    }

    // unary operators
    if (target_complement() != -6148914691236517207l) {
        return 6;
    }

    if (target_neg() + 9223372036854775716l != 0) {
        return 7;
    }

    if (target_not() != 0) {
        return 8;
    }

    // comparisons
    if (!target_eq()) {
        return 9;
    }
    if (!target_neq()) {
        return 10;
    }
    if (!target_gt()) {
        return 11;
    }
    if (!target_ge()) {
        return 12;
    }
    if (target_lt()) {
        return 13;
    }
    if (target_le()) {
        return 14;
    }

    return 0;
}
