/* Make sure our analysis recognizes which registers are used by each function call/return statement
   Liveness analysis should recognize that only EDI, ESI, and EDX are live right before calling client
   If we assume ECX, R8 and R9 are also live, we'll conclude that they're live throughout the whole function
   (since they're never updated) and won't be able to allocate them, resuling in spills
*/

int client (int a, int b, int c) {
    return a == 1 && b == 8 && c == 6;
}

int target(int one, int two, int three) {
    int four = one * one;
    int five = two * 4;
    int six = (one - two) + (one - three);
    return client(four, five, six);
}