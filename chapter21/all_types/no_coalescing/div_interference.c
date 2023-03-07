int glob = 3;

int client(unsigned int a, unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int f, unsigned int g) {
    return (a == 12 && b == 12 && c == -3 && d == 10 && e == -30 && f== 52 && g == 48);
}
int target() {

    unsigned int tmp1 = glob * 16; 
    unsigned int a = tmp1 / 4; // div creates conflict b/t tmp1 and ax since tmp1 is still live
    unsigned int b = glob * 4;
    unsigned int c = glob - 6;
    unsigned int d = glob + 7;
    unsigned int e = d * c;
    unsigned int f = tmp1 + 4;
   return client(a, b,c,d,e,f,tmp1);

}

int main() {
    return target();
}