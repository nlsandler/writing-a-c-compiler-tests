void *calloc(unsigned long nmemb, unsigned long size);
void free(void *ptr);
int main() {
  int i = 10;
  void *arr[4] = {calloc(2, sizeof(int)), &i, 0, arr};

  // first element points to 8 bytes initialized to 0
  int *elem_0 = arr[0];
  if (elem_0[0] || elem_0[1])
    return 0;

  // second element points to i
  int elem_1_val = *(int *)arr[1];
  if (elem_1_val != i)
    return 0;

  // 3rd element is a null pointer
  if (arr[2])
    return 0;

  // 4th element points to arr itself! trippy!
  if (arr[3] != arr)
    return 0;
  free(elem_0);
  return 1;
}