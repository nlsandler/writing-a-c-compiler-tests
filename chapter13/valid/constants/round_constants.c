int main(void) {
    /* Both these values should round to
     * 1.000000000000000444089209850062616169452667236328125.
     * (I got these numbers from from example 2 in
     * https://www.exploringbinary.com/17-digits-gets-you-there-once-youve-found-your-way/)
     */
    return 1.00000000000000033306690738754696212708950042724609375 == 1.0000000000000004;
}