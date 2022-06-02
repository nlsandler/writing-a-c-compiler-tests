int get()
{
    static int i = 0;
    i = i + 1;
    return i;
}

int consume(int a, int b, int c, int d, int e, int f)
{
    return a == 1 && b == 2 && c == 3 && d == 4 && e == 5 && f == 6;
}

/* 1. confirm no spills
 * 2. use handwritten assembly caller, confirm callee-saved regs are restored */
int client()
{
    int a = get(); // store a in a callee-saved reg
    int b = get(); // store b in a callee-saved reg
    int c = get(); // store c in a callee-saved reg
    int d = get(); // store d in a callee-saved reg
    int e = get(); // store ein a callee-saved-reg
    int f = get(); // store f in a non-callee-saved reg
    return consume(a, b, c, d, e, f);
}

int main()
{
    return client();
}