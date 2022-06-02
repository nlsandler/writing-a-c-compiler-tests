int main() {
    char escapes[3] = "\a\b\n";
    return escapes[0] == '\a' && escapes[1] == '\b' && escapes[2] == '\n';
}