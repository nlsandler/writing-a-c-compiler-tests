// if a graph has more than twelve temporaries but few conflicts, we can still coloro itw ithout spills

int client(int i);

int no_spills(int one, int two, int flag) {


    if (!flag) {
        int five = one * two;
        int six = client(five) + 6;
        return six;
    }

    if (flag == 1) {
        int seven = one + two;
        int eight = client(seven) + 8;
        return eight;
    }

    if (flag == 2) {
        int nine = one - two;
        int ten = client(nine) + 10;
        return ten;
    }

    if (flag == 3) {
        int eleven = one % two;
        int twelve = client(eleven) + 12;
        return twelve;
    }

    if (flag == 4) {
        int thirteen = one / two;
        int fourteen = client(thirteen) + 14;
        return fourteen;
    }

    return 0;


}