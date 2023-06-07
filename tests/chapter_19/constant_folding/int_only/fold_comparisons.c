int target_eq(void) {
    return 2147483647 == 2147483647;
}

int target_neq(void) {
    return 1111 != 1112;
}

int target_gt(void) {
    return 10 > 10;
}

int target_ge(void) {
    return 123456 >= 123456;
}

int target_lt(void) {
    return 256 < 0;
}

int target_le(void) {
    return 123456 <= 123457;
}

int main(void) {
    if (!target_eq())
        return 1;
    if (!target_neq())
        return 2;
    if (target_gt())
        return 3;
    if (!target_ge())
        return 4;        
    if (target_lt())
        return 5;
    if (!target_le())
        return 6;
    return 0;
}