// make sure any char array variables larger than 16 bytes are 16-byte aligned

int check_aligment(char *c)
{
    unsigned long l = (unsigned long)c;
    return (l % 16 == 0); // return 1 on success, 0 on failure
}

static unsigned char nested[3][4][2] = {{"a"}, {"b"}};

static signed char flat[17] = "x";

int main(void)
{
    char nested_auto[10][3];
    char flat_auto[22];

    return (check_aligment((char *)nested) && check_aligment((char *)flat) && check_aligment((char *)nested_auto) && check_aligment(flat_auto));
}