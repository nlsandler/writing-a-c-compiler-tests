/* Because long is a keyword, you can't use it as a function name */
int long() {
    return 4;
}

int main(){
    return long();
}