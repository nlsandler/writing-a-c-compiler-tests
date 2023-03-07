int main() {
    switch(4) {
        case 0:
            return 0;
        case 4: {
            int acc = 0;
            for (int i = 0; i < 10; i = i + 1) {
                if (i % 2)
                    continue;
                acc = acc + 1;
            }
            return acc;
        }
    }
    return 5;
}