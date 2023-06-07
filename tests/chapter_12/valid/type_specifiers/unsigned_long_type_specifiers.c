/* Exercise different ways to specify the type "unsigned long" */

/* Declare the global variable x in several different ways */
unsigned long x;
long unsigned x;
long int unsigned x;
unsigned int long x = 4;

int main(void) {
    /* Declare the same variable again with a storage-class specifier */
    long extern unsigned x;
    unsigned long extern x;
    int extern unsigned long x;
    return x;
}
