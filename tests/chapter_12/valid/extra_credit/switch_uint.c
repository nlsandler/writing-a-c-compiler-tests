int switch_on_uint(unsigned int ui)
{
    switch (ui)
    {
    case 5u:
        return 0;
    // this will be converted to 2^32 - 10, or 4294967286
    // case -10l:
    //    return 1;
    // 2^35 + 10, will be converted to 10
    case 34359738378ul:
        return 2;
    default:
        return 3;
    }
}

int main(void)
{
    if (switch_on_uint(5) != 0)
        return 0;
    if (switch_on_uint(4294967286) != 1)
        return 0;
    if (switch_on_uint(10) != 2)
        return 0;
    return 1;
}