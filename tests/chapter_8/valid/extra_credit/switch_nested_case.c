int main(void) {
    switch(3) {
        case 0: return 0;
        case 1: if (0) {
            case 3: return 3;
        }
        default: return 0;
    }
}