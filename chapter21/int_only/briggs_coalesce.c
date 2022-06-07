// make sure we coalesce x into y
// note that we require both to be callee-saved so we don't
// coalesce either one into EAX

int foo()
{
    return 5;
}

int flag = 1;
int glob = 4;

int fun_call()
{
    flag = !flag;
    return flag;
}
int main()
{

    // look for: subl $10, %reg then movl $40, reg w/ same reg
    // NOTE: not robust to different approaches to codegen
    // e.g. clang puts x and y in different regs and uses conditional move
    int x = glob - 10;
    int y;
    if (flag)
    {
        y = 40;
    }
    else
    {
        y = x;
    }
    fun_call();
    return y;
}