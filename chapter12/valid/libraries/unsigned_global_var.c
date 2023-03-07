unsigned int ui = 4294967200u;

unsigned int return_uint() {
    return ui;
}

int return_uint_as_signed() {
    return ui; //implicitly convert to signed int
}

long return_uint_as_long() {
    return ui; // implicitly convert to signed long
}