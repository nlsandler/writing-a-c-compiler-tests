int glob = 20;
int glob2 = 30;
int glob3 = 40;
int flag = 0;

int use(int a, int b, int c, int d, int e, int f, int g, int h);

int target(int arg) {

   int a;
   int b;
   int c;
   int d;
   int e;
   int f;
   int g;
   int h;
   // a-h all conflict,
   // but coalescing a w/ arg removes conflicts, which then lets us coalesce others w/ arg too
   // flag prevents us from performing copy prop
   if (flag) {
    a = arg;
    b = arg;
    c = arg;
    d = arg;
    e = arg;
    f = arg;
    g = arg;
    h = 2;
   } else {
    a = glob * 2;
    b = a;
    c = a;
    d = a;
    e = a;
    f = a;
    g = a;
    h = 1;
   }
   // total of 11 mov instructions:
   // move EDI into each param-passing reg,
   // then into EAX so we can push it onto stack (as g)
   return use(a,b,c,d,e,f, g,h);
}