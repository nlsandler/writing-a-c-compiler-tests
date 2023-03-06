// larger than 16 bytes but size is not divisible by 8 bytes
struct wonky {
  char arr[19];
};

int main() { return sizeof(struct wonky); }