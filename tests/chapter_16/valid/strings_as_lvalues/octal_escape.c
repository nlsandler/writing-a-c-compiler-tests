// make sure we correctly escape special characters,
// specifically make sure that we won't escape something like
// " 123" as "\40123", which is an invalid escape sequence
// Also make sure we don't just add leading zeros to all octal codes;
// this would, e.g. turn "^@" into "\0136\0100",
// which the assembler will interpret as \013 6 \010 0 
int puts(char *c);
int main(void) {
    puts("Testing, 123.");
    puts("^@1 _\\]");
    return 0;
}