int target()
{
    // w/ dse and copy prop, look for movl $10, %eax and no other movl $10, whatever
    int x = 10;
    return x;
}

int main() {
    return target();
}