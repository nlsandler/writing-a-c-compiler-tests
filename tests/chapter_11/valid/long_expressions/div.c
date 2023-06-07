int main(void) {
    long a = 4294967290l;
    long b = a / 128l;
    /* Make sure division works correctly even when the first operand
     * can't fit in an int; this requires us to store the operand in RDX:RAX
     * using the 'cqo' instruction, instead of in EDX:EAX using 'cdq'
     */
    if (b == 33554431l) {
        return 1;
    }
    return 0;
}