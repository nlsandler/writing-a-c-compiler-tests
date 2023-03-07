int main(){
    switch(3) {
        case 0:
            return 0;
        case 3: {
            switch(4) {
                case 3: return 0;
                case 4: return 1;
                default: return 0;
            }
        }
        case 4: return 0;
        default: return 0;
    }
}