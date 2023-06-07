/* Test comparisons to several null pointer constants */
int main(void)
{
    double x;
    double *null = 0;
    double *non_null = &x;

    int eq_zero_true = null == 0;
    int eq_zero_false = non_null == 0l;

    int neq_zero_true = 0u != non_null;
    int neq_zero_false = null != 0ul;

    return eq_zero_true && !eq_zero_false && neq_zero_true && !neq_zero_false;
}