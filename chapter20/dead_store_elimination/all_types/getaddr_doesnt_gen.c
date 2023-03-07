int target()
{
    int x = 4; // initialization is a dead store
    int *ptr = &x;
    return ptr == 0;
}

int main() {
    return target();
}