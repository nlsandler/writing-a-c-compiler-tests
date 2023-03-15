// you can't tentatively define an object
// that has internal linkage w/ incomplete type
// strictly speaking this is undefined behavior
// rather than a constraint violation
static void v;

int main(void) { return 0; }