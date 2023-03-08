int target()
{
    // if we enable DSE and dead code elim, x should go away
    int x = 10;
    if (x)
        ;
    return 10;
}

int main() {
    return target();
}