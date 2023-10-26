#include "pass_wonky_struct.h"

int main(void) {
    // because this is static, it will be initialized to all zeros
    static struct wonky all_zeros;

    struct wonky modified = change_struct(all_zeros);
    if (modified.arr[0] != 1)
        return 100;
    if (modified.arr[6] != 6)
        return 101;
    if (modified.arr[17] != -1)
        return 102;
    for (int i = 0; i < 14; i = i + 1) {
        if (i == 0 || i == 6 || i == 13)
            continue;
        if (modified.arr[i] != 0)
            return i;
    }

    return 0;
}