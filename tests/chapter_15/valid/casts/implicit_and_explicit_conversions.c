/* Test that we correctly track both implicit type conversions via array decay
 * and explicit casts 
 */
int main(void) {
    long arr[4] = {1,2,3,4};

    // (int *) cast here is a no-op, since arr already decays to a pointer to its first element
    if (arr != (long *) arr) {
        return 1;
    }

    // taking address with & and explicitly converting to pointer to array
    // both result in address of arr with same type
    if ((long (*)[4]) arr != &arr) {
        return 2;
    }

    return 0;
}