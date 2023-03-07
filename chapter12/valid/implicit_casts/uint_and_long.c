/* When performing an operation on an unsigned type,
 * and a signed type that can represent every value of the
 * unsigned type, convert the unsigned value to the signed type
 */

int main() {
    /* This will be converted to a long
     * with value 100
     */
    unsigned int ui = 100u;

    signed long l = -100;

    return (ui > l);
}