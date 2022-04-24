/* Test out different ways to declare a signed int */
static int x;
signed extern x;
int static signed x = 5;
signed int static x;

int main() {
    int signed extern x;
    return x;
}