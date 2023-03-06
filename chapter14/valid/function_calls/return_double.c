/* Test that we follow the calling convention for a double return type */
double d() {
    return 1234.e75;
}

int main() {
    double retval = d();
    return retval == 1234.e75;
}