// make sure we can use character constants in all the same places as integers

// use character constants to initialize static variables of any arithmetic type
double d = '\\';

int main()
{
    // can use character constants to specify array dimensions,
    // and to initialize array elements of any int-compatible type
    unsigned long array['\n'] = {1, 2, 'a', '\b', 3, 4, 5, '!', '%', '~'};

    // can use character constants in arithmetic expressions
    double d = 10 % '\a' + 4.0 * '_' - ~'@'; // 10 % 7 + 4.0 * 95

    // can use character constants in subscript expressions
    int i = array['\a'];

    return (array[2] == 97) && array[7] == 33 && array[8] == 37 && array[9] == 126 && d == 448.0 && i == 33;
}