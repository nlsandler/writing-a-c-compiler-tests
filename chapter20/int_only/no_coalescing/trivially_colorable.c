int glob = 10;
int glob2 = 11;

int client(int x, int y, int z) {
    return x == 13 && y == 143 && z ==  -130;
}

int target() {
    int x = glob + 3;
    int y = glob2 * x;
    int z = x - y;
    return client(x, y, z);
}