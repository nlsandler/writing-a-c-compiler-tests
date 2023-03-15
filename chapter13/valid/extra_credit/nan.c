// Test that we handle NaN correctly

// This should return zero, because all comparisons with NaN are false
int main(void) {
    double nan = 0.0 / 0.0;
    if (nan < 0.0 || nan == 0.0 || nan > 0.0)
        return 1;

    if (nan == nan)
        return 1;

    return 0;
}