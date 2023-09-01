int glob = 10;
int glob2;

// first round of coalescing will coalesce x into EAX
// if we don't realize that EAX is live at exit, we'll then
// coalesce the temporary that holds x + 100 into eax, clobbering x

int target(void) {
    int x = glob + 1;
    glob2 = x + 100;
    return x;
}

int main(void) {
    return target() == 11 && glob2 == 111;
}