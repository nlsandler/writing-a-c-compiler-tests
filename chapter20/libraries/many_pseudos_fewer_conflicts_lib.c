int no_spills(int one, int two, int flag);

int client (int i) {
    return 100 * i;
}

int target() {
    if (no_spills(1,2,0) != 206)
        return 1;
    if (no_spills(1,2,1) != 308)
        return 2;
    if (no_spills(1,2,2) != -90)
       return 3;
    if (no_spills(11,6,3) != 512)
        return 4;
    if (no_spills(12,2, 4) != 614)
        return 5;
    return 0;
}