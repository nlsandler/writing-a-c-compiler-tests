/* Same idea as int-only track_arg_registers but for doubles */
int callee(double a, double b, double c);

int target(double one, double two, double three) {
    double four = three * one;
    double five = two * one;
    double six = four - five;
    double seven = 100. * four;
    double eight = one + two;
    double nine = three + four;
    double ten = five * six;
    double eleven = eight - nine - ten;
    double twelve = ten - (one - two) * (three - four) * (five - six) * (seven - one) * (eight + nine);
    return callee(ten, eleven, twelve);
}
