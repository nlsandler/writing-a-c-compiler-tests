long *pass_and_return(long *ptr)
{
    return ptr;
}

int main()
{
    long l;
    long *ptr = &l;
    long *other_ptr = pass_and_return(ptr);
    l = 10; // <-- not a dead store b/c l is aliased
    // and this is followed by load from memory
    return *other_ptr;
}