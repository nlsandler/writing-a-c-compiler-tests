int main(void) {
    unsigned int ui = 10u;

    switch(ui) {
        case 4294967295u: // 2^32 - 1
            return 0;
        case -1l: // this will be converted to 2^32 - 1
            return 1;
        default: return 2;
    }
}