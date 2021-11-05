/* Test out converting an initializer from a double to an int at compile time */
static int i = 4.9;

int main() {
    // we truncate doubles down to ints, so 4.9 becomes 4
    return i == 4;
}