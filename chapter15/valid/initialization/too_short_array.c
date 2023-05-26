int main(void) {
  /* if some elments are explicitly initialized, remaining elements
   * should be initialized to zero
   */
  unsigned long arr[3] = {2147497230u};
  unsigned int arr2[2] = {3};
  return arr[0] == 2147497230u && arr[1] == 0 && arr[2] == 0 && arr2[0] == 3 &&
         arr2[1] == 0;
}