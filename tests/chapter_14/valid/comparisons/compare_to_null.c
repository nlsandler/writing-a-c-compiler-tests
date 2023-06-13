/* Test comparisons to several null pointer constants */

double *get_null_pointer(void) {
    return 0;
}

int main(void)
{
    double x;
    double *null = get_null_pointer();
    double *non_null = &x;

    if (non_null == 0) {
        return 1;
    }

    if (!(null == 0l)) {
        return 2;
    }

    if (!(non_null != 0u)) {
        return 3;
    }

    if (null != 0ul) {
        return 4;
    }

    return 0;
}