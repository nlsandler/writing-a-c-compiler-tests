struct s;

int main() {
  return sizeof(struct s); // can't take size of incomplete type
}