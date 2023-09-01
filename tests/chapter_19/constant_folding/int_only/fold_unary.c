int target_negate(void) {
  return -3;
}

int target_negate_zero(void) {
  return -0;
}

int target_not(void) {
    return !1024;
}

int target_not_zero(void) {
    return !0;
}

int target_complement(void) {
    return ~1;
}

int main(void) {
    int three = 3;
    if (target_negate() != -three)
        return 1;

    if (target_negate_zero() != 0) {
        return 2;
    }

    if (target_not() != 0) {
        return 3;
    }

    if (target_not_zero() != 1) {
        return 2;
    }

    if (target_complement() != -2) {
        return 3;
    }

    return 0;

}