void *malloc(unsigned long size);

struct node {
    int val;
    struct node *next;
};

struct node *array_to_list(int *array, int count) {
    struct node *head = (struct node *) malloc(sizeof(struct node));
    head->val = array[0];
    struct node *current = head;
    for (int i = 1; i < count; i = i + 1) {
        current->next = (struct node *) malloc(sizeof(struct node));
        current->next->val = array[i];
        current = current->next;
    }
    return head;
}

int main() {
    int arr[4] = {9, 8, 7, 6};
    struct node *elem = array_to_list(arr,4);
    int sum = 0;
    for (int i = 0; i < 4; i = i + 1) {
        sum = sum + elem->val;
        elem = elem->next;
    }
    return sum;
}