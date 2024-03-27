// can we create a situation where one callee-saved tmp gets coalesced but then we need to use it?
// or all of them get coalesced but then we need to use one of them?

int glob = 20;

int callee(int a, int b, int c, int d, int e, int f);

// in round 1, the graph is unconstrained enough that we can conservatively coalesce all callee-saved tmps into the corresponding registers
// when we rebuild the graph, if we know callee-saved regs are live at exit, we'll recognize that these regs now confict with everything,
// whch prevents us from aggressivly coalescing all the remaining moves
// if we DON'T know they're live at exit, we'll coalesce everything
// specifically, we'll coalesce di, si, cx, r8, and r9 into the corresponding registers, and coalesce x, x1, and x2
// but then x/x1/x2 will conflict with all caller-saved regs, so we'll put it in a callee-saved reg, clobbering its original value

int cant_coalesce_fully(int di, int si) { // these will occupy DI, SI
    int x = glob + 3; // 23
    if (di) {
        int x1 = x * 4; // 92
        glob = glob / 3;
        int cx = 1 - x1; // -91
        return callee(1,2,3,cx,4,5);
    }
    if (si) {
        int x2 = x * 5; // 115
        int r8 = 2 - x2; // -113
        return callee(1,2,3,4,r8,5);
    }
    int x3 = x * 6; // 138
    int r9 = 3 - x3; // -135
    return callee(1,2,3,4,5,r9);
}