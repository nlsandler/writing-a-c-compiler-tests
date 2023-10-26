#include "missing_retval.h"

int main(void) {
    int array[4] = {1, 2, 3, 4};
    missing_return_value(array + 2);
    return array[2] == 10;
}