#include "struct.h"

struct s global = { 1, {2, 3}, 4.0};

void update_struct();

int main() {
    update_struct();
    return global.arr[1] + global.d;
}