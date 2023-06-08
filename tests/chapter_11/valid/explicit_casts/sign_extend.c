long sign_extend(int i) {
    return (long) i;
}


int main(void) {
    /* Converting a positive or negative int to a long preserves its value */ 

    int pos = 10;
    long pos_long = sign_extend(pos);
    int neg = -10;
    long neg_long = sign_extend(neg);

    if (pos_long != 10l)
        return 1;

    if (pos_long + neg_long != 0l)
        return 2;

    return 0;
}