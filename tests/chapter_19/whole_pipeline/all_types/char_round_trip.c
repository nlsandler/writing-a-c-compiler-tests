// test constant folding of type conversions between char and int;
// this may already be covered elsewhere
int target(void) {
    int i = 257;
    char c = i;
    i = 255;
    char c2 = i;
    return (int)c == 1 && (int) c2 == -1;
}

int main(void) {
    return target();
}