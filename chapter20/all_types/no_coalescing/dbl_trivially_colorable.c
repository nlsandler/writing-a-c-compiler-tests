int target(double x, double y)
{
    /* w/out conservative coalescing:
     * confirm that we don't access memory
     * w/ conservative coalescing:
     * - no mov from xmm0 or xmm1
     */
    return 10 - (3.0 * y + x);
}