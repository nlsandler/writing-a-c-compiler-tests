// we can't declare a parameter with invalid type
// void[3], even though it would be adjusted
// to the valid type void *
int arr(void foo[3]) { return 3; }

int main() { return 0; }