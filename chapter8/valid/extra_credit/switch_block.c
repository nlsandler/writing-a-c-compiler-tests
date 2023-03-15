int main(void) {
    int a = 4;
    int b = 0;
    switch(2) {
        case 2: {
            int a = 8;
            b = a;
        }
    }
    return (a == 4 && b == 8);
}