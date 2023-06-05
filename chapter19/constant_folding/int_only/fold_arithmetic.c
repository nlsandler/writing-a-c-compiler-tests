int target_add(void) {
  return 100 + 200;
}

int target_sub(void) { return 2 - 2147483647; }

int target_mult(void) { return 1000 * 1000; }

int target_div(void) {
    return 1111 / 4;
}

int target_rem(void) { return 10 % 3; }

int main(void) {
    if (target_add() != 300) {        
        return 1;
    }
    if (target_sub() != -2147483645) {        
        return 2;
    }
    if (target_mult() != 1000000) {        
        return 3;
    }
    if (target_div() != 277) {        
        return 4;
    }
    if (target_rem() != 1) {        
        return 5;
    }
    return 0;
}