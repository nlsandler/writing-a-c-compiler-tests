int main(void) {
    int ident = 5;
    goto ident;
    return 0;
    ident:
        return ident;
}