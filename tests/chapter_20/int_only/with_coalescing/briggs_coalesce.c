int flag = 1;
int glob = 4;


int target(void) {
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
    if (y == -16)
        return 1;
    if (y == 40)
        return 2;
    return -1;
}