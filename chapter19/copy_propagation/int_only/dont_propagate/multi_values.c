int multi_path(int flag)
{
    int x = 3;
    if (flag)
        x = 4;
    // make sure it's not propagated - no assembly inspection needed
    return x;
}

int main(void)
{
    return multi_path(1) + multi_path(0);
}