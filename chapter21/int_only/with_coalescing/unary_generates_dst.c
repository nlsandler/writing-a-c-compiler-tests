// test that a unary instruction generates its destination, e.g. neg dst
// makes dst live (or at least doesn't kill it)

int glob = 100;

int target() {
    int a = -100;
    while (a < 0) {
        // this addition becomes:
        // movl %a, %tmp
        // addl %glob, %tmp
        // movl %tmp, %glob
        // so unless we think a is still live,
        // we'll coalesce a & tmp
        glob = a + glob;
        // after one round of coalescing this will be
        // subl $1, %a.0
        // so we need to recognize that this sub instruction
        // won't kill a
        a = -a;
        if (!(a == 100 || a == -100))
            return -1;

    }
    return glob;
}

int main() {
    return target();
}