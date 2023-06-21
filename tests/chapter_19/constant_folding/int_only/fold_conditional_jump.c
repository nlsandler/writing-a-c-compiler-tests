#if defined SUPPRESS_WARNINGS && defined __clang__
#pragma clang diagnostic ignored "-Wconstant-logical-operand"
#endif

// test constant folding of JumpIfZero and JumpIfNotZero
// optimized target functions should have no conditional jump or set instructions,
// just jumps and moves
int target_jz_to_jmp(void) {
    return 0 && 0;
}

int target_remove_jz(void) {
    return 1 && 1;
}

int target_jnz_to_jmp(void) {
    return 3 || 99;
}

int target_remove_jnz(void) {
    return 0 || 1;
}


int main(void) {
    if (target_jz_to_jmp() != 0) {
        return 1;
    }
    if (target_remove_jz() != 1) {
        return 2;
    }
    if (target_jnz_to_jmp() != 1) {
        return 3;
    }
    if (target_remove_jnz() != 1) {
        return 4;
    }
    return 0;
}