/* A static local variable and a variable with internal linkage
 * may have the same name, but they refer to different objects,
 * since the static local variable has no linkage.
 */

/* A variable with internal linkage */
static int i;

/* this function sets either static local 'i'
 * or the 'i' with internal linkage to new_val,
 * then return value of local 'i'
 */
int update_static_or_global(int update_global, int new_val) {

    /* A static local variable; it has static storage duration,
    * but no linkage
    */
    static int i;
    if (update_global) {
        /* bring i with linkage into scope, shadowing local i */
        extern int i;
        i = new_val;
    } else
        // update local i
        i = new_val;

    // return local i, regardless of what was updated
    return i;
}

int main() {
    if (i != 0) // i with linkage should be initialized to 0
        return 1;

    /* update i with linkage, and check values of both variables */
    int result = update_static_or_global(1, 10);

    if (result != 0)
        return 1;

    if (i != 10)
        return 1;

    /* update local i */
    result = update_static_or_global(0, 9);
    if (result != 9)
        return 1;
    if (i != 10)
        return 1;

    /* update i with linkage again,
     * and make sure local i retains the value from the prior call
     */
    result = update_static_or_global(1, 11);
    if (result != 9)
        return 1;
    if (i != 11)
        return 1;
    return 0;
}