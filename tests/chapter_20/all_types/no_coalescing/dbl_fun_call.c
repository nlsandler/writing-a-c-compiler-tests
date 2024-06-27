/* make sure values of doubles are preserved across function calls
 * (they must be on the stack, since XMM regs are all caller-saved).
 * Just validate behavior, don't inspect assembly.
 */

double glob = 3.0;

double callee(void); // defined in chapter_20/libraries/clobber_xmm_regs_(linux|os_x).s

int main(void) {
    double d = glob;
    double x = callee();
    return (d + x == 13.0);
}