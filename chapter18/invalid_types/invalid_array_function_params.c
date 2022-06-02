int foo(void (*bad_array)[3]) {
    return bad_array == 0;
}

int main() {
    return 0;
}