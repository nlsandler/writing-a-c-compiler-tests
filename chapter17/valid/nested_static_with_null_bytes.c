char nested[2][4] = {"yes", "yup"};

int main() {
    return nested[0][3] == 0 && nested[1][0] == 'y';
}