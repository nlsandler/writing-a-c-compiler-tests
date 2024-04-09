/* Make sure the meet operator doesn't always assume static variables are live;
 * they're only generated by uses, function calls, and EXIT.
 * Test this using a program that never reaches EXIT (but does terminate
 * by caling the exit function indirectly)
 * */

int exit_wrapper(int status);  // defined in chapter_19/libraries/exit.c

int i;

int target(void) {
    i = 30;  // dead store!
    // i isn't killed in this block but it's killed on all paths to function
    // call
    int counter = 0;

    do {
        if (counter < 10) {
            i = counter + 1;
        } else {
            i = counter + 2;
        }
        if (counter > 20) {
            exit_wrapper(i);
        }
        counter = counter + 1;
    } while (1);
    return 0;
}

int main(void) {
    target();
}