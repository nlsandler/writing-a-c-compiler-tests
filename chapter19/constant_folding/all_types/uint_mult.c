unsigned target(void) {
    return 4294967286u * 3u;
}

int main(void) {
   return target() == 4294967266u;
}