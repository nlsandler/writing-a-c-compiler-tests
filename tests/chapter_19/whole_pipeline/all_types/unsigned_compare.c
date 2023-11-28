// really a consatnt-folding test
int target(void) {
    return (-1u > 100u);
}

int main(void) {
    return target();
}