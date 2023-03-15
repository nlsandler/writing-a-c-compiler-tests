// make sure that when we initialize an array from a string literal,
// we zero out elements that aren't explicitly initialized
// include static/automatic/nested arrays w/ all three character types

static char stat[5] = "hi";
static signed char nested_stat[3][4] = {"", "bc"}; // empty string just initializes to null byte

int main(void)
{

    // validate stat
    if (stat[0] != 'h' || stat[1] != 'i' || stat[2] || stat[3] || stat[4])
        return 1;

    // validate nested_stat
    for (int i = 0; i < 3; i = i + 1)
        for (int j = 0; j < 4; j = j + 1)
        {

            signed char c = nested_stat[i][j];
            if (i == 0)
            {
                if (j == 0)
                {
                    if (c)
                        return 2;
                }
            }
            else if (i == 1)
            {
                if (j == 0 && c != 'b')
                {
                    return 4;
                }
                else if (j == 1 && c != 'c')
                {
                    return 5;
                }
                else if (j > 1 && c)
                {
                    return 6;
                }
            }
            else if (i > 1 && c)
            {
                return 7;
            }
        }

    unsigned char aut[4] = "ab";
    // validate aut
    if (aut[0] != 'a' || aut[1] != 'b' || aut[2] || aut[3])
        return 8;

    signed char nested_auto[2][2][4] = {{"foo"}, {"x", "yz"}};
    // validate nested auto
    signed char *foo = nested_auto[0][0];
    if (foo[0] != 'f' || foo[1] != 'o' || foo[2] != 'o' || foo[3])
        return 9;
    for (int i = 0; i < 2; i = i + 1)
        for (int j = 0; j < 2; j = j + 1)
        {
            if (i == 0 && j == 0)
            {
                // this is "foo", which we already validated
                continue;
            }
            for (int k = 0; k < 4; k = k + 1)
            {
                signed char c = nested_auto[i][j][k];
                if (i == 1 && j == 0 && k == 0)
                {
                    if (c != 'x')
                        return 10;
                }
                else if (i == 1 && j == 1)
                {
                    if (k == 0 && c != 'y')
                    {
                        return 11;
                    }
                    else if (k == 1 && c != 'z')
                    {
                        return 12;
                    }
                    else if (k > 1 && c)
                    {
                        return 13;
                    }
                }
                else if (c)
                    return 14;
            }
        }

    return 0;
}