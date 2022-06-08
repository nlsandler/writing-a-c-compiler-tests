int flag = 1;
int glob = 4;

int fun_call()
{
    flag = !flag;
    return flag;
}
int foo()
{

    // make sure we don't coalesce x and y, they conflict
    int x = glob - 10;
    int y = x;
    if (flag)
    {
        y = 40;
    }
    fun_call();
    return y + x;
}

int main()
{
    return foo() + foo();
}