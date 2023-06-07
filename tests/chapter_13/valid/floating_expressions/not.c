/* Test logical negation of doubles */
int main(void) {
    int not1 = !0.0; // this is zero
    int not2 = !33.3e3; // this is not zero
    int not3 = !1e-330; // this number is so small it will be rounded to zero

    return not1 && !not2 && not3;
}