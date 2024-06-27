int main(void) {

    // bitwise compound operations on long integers
    long l1 = 71777214294589695l;  // 0x00ff00ff00ff00ff
    long l2 = -4294967296;  // -2^32; upper 32 bits are 1, lower 32 bits are 0

    l1 &= l2;
    if (l1 != 71777214277877760l) {
        return 1; // fail
    }

    l2 |= 100l;
    if (l2 != -4294967196) {
        return 2;
    }

    l1 ^= -9223372036854775807l;
    if (l1 != -9151594822576898047l /* 0x80ff00ff00000001 */ ) {
        return 3;
    }

    // if rval is int, convert to common type
    l1 = 4611686018427387903l;  // 0x3fffffffffffffff
    int i =  -1073741824;  // 0b1100....0, or 0xc0000000
    // 1. sign-extend i to 64 bits; upper 32 bits are all 1s
    // 2. take bitwise AND of sign-extended value with l1
    // 3. result (stored in l1) is 3fffffffc0000000;
    //    upper bits match l1, lower bits match i
    l1 &= i;
    if (l1 != 4611686017353646080l) {
        return 4;
    }

    // if lval is int, convert to common type, perform operation, then convert back
    i = -2147483648l; // 0x80000000
    // check result and side effect
    // 1. sign extend 0x80000000 to 0x0000000080000000
    // 2. calculate 0x0000000080000000 | 0x00ff00ff00ff00ff = 0x000ff00ff80ff00ff
    // 3. truncate to 0x80ff00ff on assignment
    if ((i |= 71777214294589695l) != -2130771713) {
        return 5;
    }
    if (i != -2130771713) {
        return 6;
    }

    return 0; // success

}