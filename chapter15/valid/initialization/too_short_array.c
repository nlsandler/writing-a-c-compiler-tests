int main() {
  /* if some elments are explicitly initialized, remaining elements
   * should be initialized to zero
   */
  int arr[3] = {1};
  unsigned int arr2[2] = {3};
  return arr[0] == 1 && arr[1] == 0 && arr[2] == 0 && arr2[0] == 3 &&
         arr2[1] == 0;
}