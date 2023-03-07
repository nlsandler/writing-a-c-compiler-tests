double fun(double x) {
    if (x > 2)
        return x;
    else {
        double ret = fun(x + 2);
        return ret + x;
    }
}
