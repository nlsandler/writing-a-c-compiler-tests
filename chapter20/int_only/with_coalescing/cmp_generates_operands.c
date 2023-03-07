int flag;

int glob = 10;
int glob2 = 20;

int main() {
    int a = glob + 5; // 15
    int b = glob2 - 5; // 15

    // we'll coalesce a and b
    // into tmps that hold these sums
    // if we don't think a and b are live afterward
    glob = a + glob; // 25
    glob2 = b + glob2; // 35

    if (a != b) {
        return -1;
    }
    return (glob == 25 && glob2 == 35);
}