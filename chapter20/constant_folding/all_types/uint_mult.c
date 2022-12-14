#include <stdio.h>
unsigned target() {
    return 4294967286u * 3u;
}

int main() {
   return target() == 4294967266u;
}