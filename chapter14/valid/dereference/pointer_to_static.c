int x = 10;

int main(void)
{
    int *static_ptr = &x;
    x = 20;
    return *static_ptr;
}