int main()
{
    // w/ dead code elimination: no comparison, jump, or label
    // even w/out constant folding!
    if (10)
        ;

    return 0;
}