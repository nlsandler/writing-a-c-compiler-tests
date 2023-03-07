/* could conceivably be type error in some implementations? */
int foo()[3];
int main()
{
    return foo()[2];
}