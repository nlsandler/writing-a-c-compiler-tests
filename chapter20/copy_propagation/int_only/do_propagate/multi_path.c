int return_3(int flag)
{
    int x = 0;
    if (flag)
    {
        x = 3;
    }
    else
    {
        x = 3;
    }
    return x; // look for movl $3, %eax
}

int main()
{
    return return_3(1) + return_3(0);
}