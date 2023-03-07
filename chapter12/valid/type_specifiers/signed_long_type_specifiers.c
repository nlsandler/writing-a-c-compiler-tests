/* Test out different ways to declare a signed long */

long signed x;
long x = 7;
int long x;
signed long int x;

int main() {
    extern signed long x;
    return x;
}