int foo(unsigned char c)
{
    return c;
}

int main(void)
{
    return foo(0);
}

// invalid redeclaration: char and unsigned char are
// different types
int foo(char c);