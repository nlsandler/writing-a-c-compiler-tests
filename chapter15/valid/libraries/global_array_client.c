extern long x;
extern long *arr[4];

long *set_pointer(void);

int main(void) {
    if (set_pointer() != 0)
        return 0;
    if (*arr[2] != x)
        return 0;
    x = -4;
    if (*arr[2] != x)
        return 0;
    return 1;
}