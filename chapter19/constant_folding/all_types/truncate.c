/* Test constant folding of all conversions from longer to shorter integer types
 * NOTE we can get better coverage of this once we implement copy propagation,
 * so we can look at conversions of chars and negative numbers,
 * and can look for instructions of the form mov $const, %eax
 * or mov whatever(%rip), %xmm0.
 * With constant folding alone the assembly is indistinguishable between folded and non-folded
 * zero-extended conversions.
 */

// truncate long
int target_long_to_int(void) {
    // 2^45 + 2^35 + 1234
    return (int)35218731828434l;
}

unsigned int target_long_to_uint(void) {
    // 2^45 + 2^35 + 1234
    return (unsigned int)35218731828434l;
}

char target_long_to_char(void) {
    // LONG_MAX
    return (char)9223372036854775807l;
}

signed char target_long_to_schar(void) {
    // 2^62 + 128
    return (signed char)4611686018427388032l;
}

unsigned char target_long_to_uchar(void) {
    // UINT_MAX
    return (unsigned char)4294967295UL;
}

// truncate unsigned long
int target_ulong_to_int(void) {
    // ULONG_MAX
    return (int)18446744073709551615UL;
}

unsigned int target_ulong_to_uint(void) {
   return (unsigned int)18446744073709551615UL;
}

char target_ulong_to_char(void) { return (char)4294967295UL; }

signed char target_ulong_to_schar(void) { return (signed char)4611686018427388032ul; }

unsigned char target_ulong_to_uchar(void) {
    // 2^63 + 255
    return (unsigned char)9223372036854776063ul;
}

// truncate int
char target_int_to_char(void) { return (char)1274; }

signed char target_int_to_schar(void) {
    // INT_MAX
    return (signed char)2147483647;
}

unsigned char target_int_to_uchar(void) { return (unsigned char)1274; }

// truncate unsigned int
char target_uint_to_char(void) {
    return (char)2147483901u; // 2^31 + 253
}

signed char target_uint_to_schar(void) {
    return (signed char)2147483660u; // 2^31 + 12
}

unsigned char target_uint_to_uchar(void) { return (unsigned char)2147483901u; }

int main(void) {

    // truncate longs

    // 0x00002008000004d2 --> 0x000004d2
    if (target_long_to_int() != 1234) {
        return 1;
    }
    if (target_long_to_uint() != 1234u) {
        return 2;
    }

    // 0x7fffffffffffffff --> 0xff
    if (target_long_to_char() != -1) {
        return 3;
    }

    // 0x4000000000000080 --> 0x80
    if (target_long_to_schar() != -128) {
        return 4;
    }

    // 0x00000000ffffffff -> 0xff
    if (target_long_to_uchar() != 255) {
        return 5;
    }

    // truncate ulongs

    // 0xffffffffffffffff --> 0xffffffff
    if (target_ulong_to_int() != -1) {
        return 6;
    }
    if (target_ulong_to_uint() != 4294967295U) {
        return 7;
    }

    // 0x7fffffffffffffff --> 0xff
    if (target_ulong_to_char() != -1) {
        return 8;
    }

    // 0x4000000000000080 --> 0x80
    if (target_ulong_to_schar() != -128) {
        return 9;
    }

    // 0x00000000ffffffff -> 0xff
    if (target_ulong_to_uchar() != 255) {
        return 10;
    }

    // truncate ints

    // 0x000004fa -> 0xfa
    if (target_int_to_char() != -6) {
        return 11;
    }

    // 0x7fffffff -> 0xff
    if (target_int_to_schar() != -1) {
        return 12;
    }

    // 0x000004fa -> 0xfa
    if (target_int_to_uchar() != 250) {
        return 13;
    }

    // truncate uints

    // 0x800000fd --> 0xfd
    if (target_uint_to_char() != -3) {
        return 14;
    }

    // 0x8000000c -> 0x0c
    if (target_uint_to_schar() != 12) {
        return 15;
    }
    // 0x800000fd --> 0xfd
    if (target_uint_to_uchar() != 253) {
        return 16;
    }
    return 0;
}