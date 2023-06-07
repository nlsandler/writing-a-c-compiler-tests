int main(void) {
    int a;
    {
        int b = a = 1;
    }
    return a;
}