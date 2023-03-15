double glob = 3.0;

int main(void) {

    // this is a regression test for a bug I found in my reference implementaton,
    // instruction fix-up rewrite cvttsd2sil -8(%rbp), -12(%rbp) to
    // cvttsdi2sil -8(%rbp), %r11d
    // movq        %r11, %-12(%rbp)
    // which potentilly clobbers other things on the stack
    // we include other variables on the stack in order to catch this
    int i = 10;
    int j = (int) glob;
    int k = 20;
    return i + j + k;
}