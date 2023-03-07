int main() {
    int x = 4;
    {
        int x;
        x = x + 1;
    }
    return x;
}