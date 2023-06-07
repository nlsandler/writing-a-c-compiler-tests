#include "struct.h"

extern struct s global;

void update_struct(void) {
    global.arr[1] = global.arr[0]*2;
    global.d = 5.0;
}