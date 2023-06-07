/* could conceivably be type error in some implementations? */
int foo(void)[3];
int main(void)
{
    return foo()[2];
}