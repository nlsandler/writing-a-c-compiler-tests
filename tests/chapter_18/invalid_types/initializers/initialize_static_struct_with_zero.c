struct s {
    int a;
};

// you can't initialize a static struct with a scalar expression, not even 0
struct s x = 0;