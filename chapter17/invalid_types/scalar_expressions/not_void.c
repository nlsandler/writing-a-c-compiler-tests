void f(void);
void g(void);
int main(void) { return !(1 ? f() : g()); }