# PhD Vulnerability Detection Prerequisites

## Selected CWEs
| ID      | Likelihood | Name                                                                    |
|---------|------------|-------------------------------------------------------------------------|
| CWE-120 | High       | Buffer Copy without Checking Size of Input                              |
| Other   | N/A        | N/A                                                                     |
| CWE-119 | High       | Improper Restriction of Operations within the Bounds of a Memory Buffer |
| CWE-476 | Medium     | NULL Pointer Dereference                                                |
| CWE-469 | Medium     | Use of Pointer Subtraction to Determine Size                            |

### CWE-120: Buffer Copy without Checking Size of Input
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
```c++
void host_lookup(char *user_supplied_addr) {
    struct hostent *hp;
    in_addr_t *addr;
    char hostname[64];
    in_addr_t inet_addr(const char *cp);

    /*routine that ensures user_supplied_addr is in the right format for conversion */

    validate_addr_form(user_supplied_addr);
    addr = inet_addr(user_supplied_addr);
    hp = gethostbyaddr( addr, sizeof(struct in_addr), AF_INET);
    strcpy(hostname, hp->h_name);
}
```

```c++
char * copy_input(char *user_supplied_string){
        int i, dst_index;
        char *dst_buf = (char*) malloc(4*sizeof(char) * MAX_SIZE);
        if ( MAX_SIZE <= strlen(user_supplied_string) ){
            die("user string too long, die evil hacker!");
        }

        dst_index = 0;
        for ( i = 0; i < strlen(user_supplied_string); i++ ){
            if( '&' == user_supplied_string[i] ){
                dst_buf[dst_index++] = '&';
                dst_buf[dst_index++] = 'a';
                dst_buf[dst_index++] = 'm';
                dst_buf[dst_index++] = 'p';
                dst_buf[dst_index++] = ';';
            }
            else if ('<' == user_supplied_string[i] ) {
                /* encode to &lt; */
            }
            else dst_buf[dst_index++] = user_supplied_string[i];
        }
        return dst_buf;
}
```

```c++
int main (int argc, char **argv) {
    char *items[] = {"boat", "car", "truck", "train"};
    int index = GetUntrustedOffset();
    printf("You selected %s\n", items[index-1]);
}
```

```c++
int getValueFromArray(int *array, int len, int index) {
    int value;
    // check that the array index is less than the maximum

    // length of the array
    if (index < len) {
        // get the value at the specified index of the array
        value = array[index];
    }
    // if array index is invalid then output error message
    // and return value indicating error
    else {
        printf("Value is: %d\n", array[index]);
        value = -1;
    }

    return value;
}
```

### CWE-476: NULL Pointer Dereference
#### Examples
```c++
void host_lookup(char *user_supplied_addr){
    struct hostent *hp;
    in_addr_t *addr;
    char hostname[64];
    in_addr_t inet_addr(const char *cp);

    /*routine that ensures user_supplied_addr is in the right format for conversion */
    validate_addr_form(user_supplied_addr);
    addr = inet_addr(user_supplied_addr);
    hp = gethostbyaddr( addr, sizeof(struct in_addr), AF_INET);
    strcpy(hostname, hp->h_name);
}
```

### CWE-469: Use of Pointer Subtraction to Determine Size
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
