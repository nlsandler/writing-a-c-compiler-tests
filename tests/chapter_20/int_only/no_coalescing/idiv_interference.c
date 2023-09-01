int glob = 3;

int client(int a, int b, int c, int d, int e, int f, int g) {
    return (a == 12 && b == 12 && c == -3 && d == 10 && e == -30 && f== 52 && g == 48);
}
int target(void) {

    int tmp1 = glob * 16;
    int a = tmp1 / 4; // idiv creates conflict b/t tmp1 and ax since tmp1 is still live
    int b = glob * 4;
    int c = glob - 6;
    int d = glob + 7;
    int e = d * c;
    int f = tmp1 + 4;
   return client(a, b,c,d,e,f,tmp1);

}

int main(void) {
    return target();
}