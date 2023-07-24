// Make sure that when we copy values into the red zone during arg passing, we don't accidentally clobber the actual stack;
// this is a regression test for a bug in found in NQCC - copied into 0(rsp) instead of -8(rsp)

struct my_struct {
    char arr[7];
};

long glob = 0;

struct my_struct s = {{0, 0, 0, 1, 2, 3, 4}};

void process_struct(struct my_struct arg);
int check_struct(void); // return 0 if static struct in lib is as expected, 1 otherwise

long f(void) {
    // can we find a less fragile test for this? assembly again?
    long x = glob - 2l; // x should be at 0(%rsp)
    process_struct(s); // we copy s into red zone and then into RDI
    return x; // return X, make sure it wasn't overwritten
}

int main(void) {
    if (f() != -2) {
        return 1;
    }

    if (check_struct()) {
        return 2;
    }

    return 0;
}