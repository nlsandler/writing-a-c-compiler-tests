int main() {
    /* when performing an arithmetic operation or comparison
     * on an unsigned int and an unsigned long, promote
     * the unsigned int to an unsigned long first
     */

    // 2^35 - if you converted this to an unsigned long
    // its value would be 0
    unsigned long ul =  34359738368u;

    unsigned int ui = 1073741824u; // 2^30

    return (ul > ui);
}