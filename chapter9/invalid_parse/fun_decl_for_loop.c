int main() {
    /* Function declarations aren't permitted in for loop headers. */
    for (int f(); ; ) {
        return 0;
    }
}