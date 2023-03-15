// test that (at least one of) idiv and cdq makes eax live
int glob = 10;

int main(void) {
    int coalesce_into_eax = glob * 2;
    // in second round of coalescing, if we don't know eax if live, we'll coalesce it with product
    int product = coalesce_into_eax + 4;
    if (product != 24)
        return -1;
    int j = coalesce_into_eax % 10; // coalesce_into_eax should be coalsced into eax, j should be coalesced into edx
    if (j)
        return -2;
    
    return 0;
}