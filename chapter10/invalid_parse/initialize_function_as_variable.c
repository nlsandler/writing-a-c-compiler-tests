/* You can't declare a function with an initializer.
   Our implementation will reject this during parsing.
   Because the C grammar permits this declaration,
   some compilers may reject it during type checking.
*/
int foo() = 3;

int main() {
    return 0;
}