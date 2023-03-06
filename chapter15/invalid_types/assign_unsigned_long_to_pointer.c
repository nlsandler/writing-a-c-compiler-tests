int main()
{
    // can't assign an unsigned long to a pointer even though
    // it could conceivably be a valid memory address
    int *ptr = 140732898195768ul;
    return 0;
}