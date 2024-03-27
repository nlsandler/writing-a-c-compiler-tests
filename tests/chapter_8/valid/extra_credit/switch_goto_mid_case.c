int main(void) {
    int a = 0;
    goto mid_case;
    switch(4) {
        case 4:
            a = 5;
            mid_case:
            a = a + 1;
            return a;
    }
    return 100;
}