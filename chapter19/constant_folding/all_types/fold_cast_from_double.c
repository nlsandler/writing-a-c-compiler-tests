// Test constant folding casts from double to integer types

char target_to_char(void) { return (char)126.5; }

unsigned char target_to_uchar(void) { return (unsigned char)254.9; }

int target_to_int(void) { return (int)5.9; }

unsigned target_to_uint(void) { return (unsigned)2147483750.5; }

long target_to_long(void) {
    // nearest representable double is 9223372036854774784.0,
    // which will be converted to long int 9223372036854774784
    return (long)9223372036854774783.1;
}

unsigned long target_to_ulong(void) {
    // same constant from chapter13/valid/explicit_casts/double_to_ulong.c
    return (unsigned long) 3458764513821589504.0;
}

int main(void) {
    if (target_to_char() != 126) {
        return 1;
    }
    if (target_to_uchar() != 254) {
        return 2;
    }
    if (target_to_int() != 5) {
        return 3;
    }
    if (target_to_uint() != 2147483750u) {
        return 4;
    }
    if (target_to_long() != 9223372036854774784l) {
        return 5;
    }
    if (target_to_ulong() != 3458764513821589504ul) {
        return 6;
    }
    return 0;
}