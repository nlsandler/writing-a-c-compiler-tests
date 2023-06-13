int main(void)
{
    /* It's illegal to assign an unsigned long to a pointer,
     * even if it might be a valid memory address
     */
    int *ptr = 140732898195768ul;
    return 0;
}