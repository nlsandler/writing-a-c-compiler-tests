/* When performing an operation on two types
 * of the same rank, convert the signed value
 * to the type of the unsigned value
 */

int main() {
    unsigned int ui = 100u;

    // this will be converted to 2^32 - 100
    signed int i = -100;

    return (i > ui);
}