int three() {
    return 3;
}

int main() {
    /* The function call operator () is higher precedence
     * than unary prefix operators
     */
    return !three();
}