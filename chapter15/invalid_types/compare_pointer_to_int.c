int main(void)
{
    long *l = 0;
    // can't compare a pointer to any integer type
    return l <= 100ul;
}