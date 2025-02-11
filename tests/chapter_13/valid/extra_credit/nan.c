// Test that we handle NaN correctly

int double_isnan(double d); // defined in tests/chapter_13/helper_libs/nan.c

// This should return zero, because all comparisons with NaN are false
int main(void) {
    static double zero = 0.0;
    double nan = 0.0 / zero; // make this constant-folding proof
    if (nan < 0.0 || nan == 0.0 || nan > 0.0 || nan <= 0.0 || nan >= 0.0)
        return 1;

    if (1 < nan || 1 == nan || 1 > nan || 1 <= nan || 1 >= nan)
        return 2;

    if (nan == nan)
        return 3;

    if (!(nan != nan)) { // != should evaluate to true
        return 4;
    }

    if (!double_isnan(nan)) {
        return 5;
    }

    if (!double_isnan(4 * nan)) {
        return 6;
    }

    if (!double_isnan(22e2 / nan)) {
        return 7;
    }

    if (!double_isnan(-nan)) {
        return 8;
    }

    if (!nan) {
        return 9;
    }

    if (nan) {
    }
    else if (nan) {
    }
    else {
        return 10;
    }

    int b_isnan;
    for (b_isnan = 0; nan;) {
        b_isnan = 1;
        break;
    }
    if (!b_isnan) {
        return 11;
    }

    b_isnan = 0;
    while (nan) {
        b_isnan = 1;
        break;
    }
    if (!b_isnan) {
        return 12;
    }

    b_isnan = -1;
    do {
        b_isnan = b_isnan + 1;
        if(b_isnan) {
            break;
        }
    } while(nan);
    if (!b_isnan) {
        return 13;
    }

    b_isnan = nan ? 1 : 0;
    if (!b_isnan) {
        return 14;
    }

    return 0;
}