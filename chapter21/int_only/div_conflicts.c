/* division causes conflict w/ edx/eax
 * can look for no spills but main req is just correctness
 */

int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;

int reset_globals()
{
    glob0 = 6;
    glob1 = 5;
    glob2 = 4;
    glob3 = 3;
    glob4 = 2;
    glob5 = 1;
    return 10;
}

int consume(int a, int b, int c, int d, int e)
{
    return a == 0 && b == 1 && c == 2 && d == 3 && e == 4;
}

int main()
{
    // first use up all the callee-saved regs
    int a = glob0;
    int b = glob1;
    int c = glob2;
    int d = glob3;
    int e = glob4;
    int f = reset_globals();

    // make lots of pseudoregs that conflict w/ EDX/EAX,
    // make sure they're allocated to other slots

    // make f, sum, sum2, and sum3 conflict w/ EDX and EAX
    // so they'll be assinged to EDI, ESI, ECX, R8, R9
    int sum = glob0 + glob1;
    int sum2 = glob2 + glob3;
    int sum3 = glob3 + glob4;
    int sum4 = glob4 + glob5;

    /*
    glob0 = sum / sum2;
    glob1 = sum3 / f;
    glob2 = sum / sum4;
    */

    glob0 = sum / sum3;
    glob1 = f / sum4;
    glob3 = sum2 / sum4;
    glob4 = sum; // make sure sum is still live after first div so it conflicts w/ EAX/EDX
    // consume a - e so we can't use those registers for anything else
    int x = consume(a, b, c, d, e);
    return (x == 1 && glob0 == 2 && glob1 == 3 && glob2 == 4);
}
