int x() { return 0; }

// can't apply sizeof to a function
int main() { return sizeof x; }