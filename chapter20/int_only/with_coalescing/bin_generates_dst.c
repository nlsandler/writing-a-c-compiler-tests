// test that a binary instruction generates its destination, e.g. add src, dst
// makes dst live (or at least doesn't kill it)

int glob = 1;
int flag = 1;

int f();

int target() {
    
    int a = 100;
    while (a) {
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
        a = a - 1;
    }
    return glob;
}

int main() {
    return target();
}