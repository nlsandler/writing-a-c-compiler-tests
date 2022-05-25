struct s
{
    int a;
    int b;
    int c
};

struct s glob = {1, 2, 3};

int main()
{
    struct s my_struct = glob; // this isn't dead!
    // overwriting part of struct doesn't kill whole thing
    my_struct.c = 100;
    return my_struct.c + my_struct.a;
}