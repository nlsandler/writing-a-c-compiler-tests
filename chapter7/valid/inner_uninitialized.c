int main(void) {
    int x = 4;
    {
        int x;
        x = x + 1;
    }
    return x;
}