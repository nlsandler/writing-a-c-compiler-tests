int main(void)
{
    // a mix of escaped and unescaped special characters
    char special[6] = "\a\b\n	";
    return special[0] == '\a' && special[1] == '\b' && special[2] == '\n' && special[3] == '\v' && special[4] == '\f' && special[5] == '\t';
}