int f(int x, int y)
{
    /* w/out conservative coalescing:
     * confirm that we don't access memory
     * w/ conservative coalescing:
     * - no mov from EDI or ESI
     * - no mov from memory/register into EAX
     * - mov $10, %eax
     */
    return 10 - (3 * y + x);
}

int main()
{
    // 5 + 30 = 35
    return f(2, 3) + f(-4, -8);
}