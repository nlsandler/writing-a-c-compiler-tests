int main() {
    /* Converting a positive or negative int to a long preserves its value */ 

    int pos = 10;
    long pos_long = (long) pos;
    int neg = -10;
    long neg_long = (long) neg;

    if (pos_long != 10l)
        return 0;

    if (pos_long + neg_long != 0l)
        return 0;

    return 1;
}