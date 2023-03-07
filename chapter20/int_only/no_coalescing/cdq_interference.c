int glob = 100;
int glob2 = 0;

int target(int flag) {
  int a;
  int b;
  int c;
  int d;
  int e;
  int f;

  // division means that a-f and callee-saved tmps all conflict w/ each oher,
  // AX, and DX so graph is uncolorable BUT if we don't recognize conflict w/
  // DX, we'll prune the whole graph without spills which will lead us to put a
  // divisor in DX, causing a spill! don't need to inspect this, just make sure
  // it gives the right answer

  // we split this into cases based on value of flag to avoid creating too many
  // other conflicting pseudos each temporary that holds the result of a
  // comparison will conflict with some of a-e, but not all
  if (flag < 10) {

    // provide alternate initialization to prevent copy prop
    if (glob2) {
      a = 10;
      b = 10;
      c = 10;
    } else {
      a = 5;
      b = 5;
      c = 5;
    }

    // each of these clauses makes one temporary conflict with DX and AX
    // performing division first, and then updating all the others, ensures that
    // only cdq causes conflicts with DX (idiv doesn't)
    if (flag < 0) {
      a = glob / a; // now a can't be in dx (or ax)
      b = 1;
      c = 2;
      d = 3;
      e = 4;
      f = 5;
    } else if (flag < 5) {
      b = glob / b; // now b can't be in dx (or ax)
      a = 1;
      c = 2;
      d = 3;
      e = 4;
      f = 5;
    } else {
      c = glob / c; // etc
      a = 1;
      b = 2;
      d = 3;
      e = 4;
      f = 5;
    }

  } else {

    // provide alternate initialization to prevent copy prop
    if (glob2) {
      d = 10;
      e = 10;
      f = 10;
    } else {
      d = 5;
      e = 5;
      f = 5;
    }

    if (flag <= 15) {
      d = glob / d; // now d can't be in dx
      a = 1;
      b = 2;
      c = 3;
      e = 4;
      f = 5;
    } else if (flag < 20) {
      e = glob / e; // now e can't be in dx
      a = 1;
      b = 2;
      c = 3;
      d = 4;
      f = 5;
    } else {
      f = glob / f; // now f can't be in dx
      a = 1;
      b = 2;
      c = 3;
      d = 4;
      e = 5;
    }
  }

  int result;

    // expected values for flag < 0 and glob2 == 0
  if (a == 20 && b == 1 && c == 2 && d == 3 && e == 4 && f == 5) {
    result = 1;
  }
    // expected values for flag < 0 and glob2 != 0
  else if (a == 10 && b == 1 && c == 2 && d == 3 && e == 4 &&
           f == 5) {
    result = 2;
  }
    // expected values for 0 < flag < 5 and glob2 != 0
  else if (a == 1 && b == 10 && c == 2 && d == 3 && e == 4 &&
           f == 5) {
    result = 3;
  }
    // expected values for  0 < flag < 5 and glob2 == 0
  else if (a == 1 && b == 20 && c == 2 && d == 3 && e == 4 &&
           f == 5) {
    result = 4;
  }

    // expected values for 5 < flag < 10 and glob2 == 0
  else if (a == 1 && b == 2 && c == 20 && d == 3 && e == 4 &&
           f == 5) {
    result = 5;
  }

    // expected values for 6 < flag < 10 and glob2 != 0
  else if ( a == 1 && b == 2 && c == 10 && d == 3 && e == 4 &&
           f == 5) {
    result = 6;
  }
    // expected values for 10 < flag <= 15 and glob2 != 0
  else if ( a == 1 && b == 2 && c == 3 && d == 10 && e == 4 &&
             f == 5) {
    result = 7;
  }        // expected values for 10 < flag < 15 and glob2 == 0
  else if (a == 1 && b == 2 && c == 3 && d == 20 && e == 4 &&
             f == 5) {
    result = 8;
  }    // expected values for 15 < flag < 20 and glob2 == 0
  else if ( a == 1 && b == 2 && c == 3 && d == 4 && e == 20 &&
             f == 5) {
    result = 9;
  }     // expected values for 15 < flag < 20 and glob2 != 0
  else if (a == 1 && b == 2 && c == 3 && d == 4 && e == 10 &&
             f == 5) {
    result = 10;
  }      // expected values for flag > 20 and glob2 != 0
  else if (a == 1 && b == 2 && c == 3 && d == 4 && e == 5 &&
             f == 10) {
    result = 11;
  }     // expected values for flag > 20 and glob2 == 0
  else if (a == 1 && b == 2 && c == 3 && d == 4 && e == 5 &&
             f == 20) {
    result = 12;
  } else {
    // something has gone wrong!
    result = -100;
  }
  return result;
}

int main() {
    glob2 = 0;
    if (target(-2) != 1)
        return 1;

    if (target(3) != 4)
        return 2;
    
    if (target(6) != 5)
        return 3;
    
    if (target(11) != 8)
        return 4;
    
    if (target(17) != 9)
        return 5;
    
    if (target(23) != 12)
        return 6;

    glob2 = 1;

    if (target(-2) != 2)
        return 7;

    if (target(3) != 3)
        return 8;
    
    if (target(6) != 6)
        return 9;
    
    if (target(11) != 7)
        return 10;
    
    if (target(17) != 10)
        return 11;
    
    if (target(23) != 11)
        return 12;

    return 0;
}
