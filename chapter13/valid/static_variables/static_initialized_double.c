// Test an explicitly initialized static double

// Return old value increment by one
double return_static_variable() {
    static double d = 0.5;
    double ret = d;
    d = d + 1.0;
    return ret;
}

int main() {
    double d1 = return_static_variable();
    double d2 = return_static_variable();
    double d3 = return_static_variable();
    return (d1 == 0.5 && d2 == 1.5 && d3 == 2.5);
}
