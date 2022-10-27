# PhD Vulnerability Detection Prerequisites

## Draper VDISC CWEs
| CWE ID             | CWE Description |
|--------------------|-----------------|
| 120/121/122        | [Buffer Overflow](cwe_120.md)
| 119                | Improper Restriction of Operations within the Bounds of a Memory Buffer
| 476                | [NULL Pointer Dereference](cwe_476.md)
| 469                | [Use of Pointer Subtraction to Determine Size](cwe_469.md)
| 20, 457, 805, etc. | Improver Input Validation, Use of Uninitialized Variable, Buffer Access with Incorrect Length Value, etc.


### CWE-120: Buffer Copy without Checking Size of Input
> The program copies an input buffer to an output buffer without verifying that the size of the input buffer is less than the size of the output buffer, leading to a buffer overflow.

#### Examples
```c++
char last_name[20];
printf ("Enter your last name: ");
scanf ("%s", last_name);
```

```c++
void manipulate_string(char * string){
    char buf[24];
    strcpy(buf, string);
    ...
}
```

```c++
char buf[24];
printf("Please enter your name and press <Enter>\n");
gets(buf);
```

### CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer


#### Examples


### CWE-469: Use of Pointer Subtraction to Determine Size
> The application subtracts one pointer from another in order to determine size, but this calculation can be incorrect if the pointers do not exist in the same memory chunk.

#### Examples
```c++
struct node {
    int data;
    struct node* next;
};

// Returns the number of nodes in a linked list from

// the given pointer to the head of the list.
int size(struct node* head) {
    struct node* current = head;
    struct node* tail;
    while (current != NULL) {
        tail = current;
        current = current->next;
    }
    return tail - head;
}

// other methods for manipulating the list
...
```
