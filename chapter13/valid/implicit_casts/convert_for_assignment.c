/* Convert the right-hand operand of an assignment statement
 * to the type of the left-hand operand
 */
int main(void) {
    double d = 18446744073709551586ul; // implicitly convert to nearest double
    int i = 4.9; //implicitly truncate to integer

    return (d == 18446744073709551616. && i == 4);
}