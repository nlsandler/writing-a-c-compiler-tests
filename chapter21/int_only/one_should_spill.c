int get()
{
    static int i = 0;
    i = i + 1;
    return i;
}

int consume(int a, int b, int c, int d, int e, int f)
{
    return a * b * c * d * e * f;
}

/* 1. confirm no more than one spill here
 * (NOTE: it's possible to avoid a spill here
 * by using EBP as general purpose register and/or moving)
 * 2. use handwritten assembly caller, confirm callee-saved regs are restored */
int client()
{
    int a = get(); // store a in a callee-saved reg
    int b = get(); // store b in a callee-saved reg
    int c = get(); // store c in a callee-saved reg
    int d = get(); // store d in a callee-saved reg
    int e = get(); // store e in a callee-saved-reg
    int f = get(); // spill f (we're out of callee-saved regs)
    return consume(a, b, c, d, e, f) + a + b + c + d + e + f;
}