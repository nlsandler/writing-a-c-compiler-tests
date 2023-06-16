// make sure that &ptr[idx] doesn't actually produce memory access
int main(void) {
    // this is equivalent to ((int *) 0), which is a null pointer
    int *null_ptr =  &((int *) 0)[0];
    return null_ptr == 0;
}