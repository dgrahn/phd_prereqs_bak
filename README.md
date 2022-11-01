# PhD Vulnerability Detection Prerequisites

## Draper VDISC CWEs
| CWE ID             | CWE Description |
|--------------------|-----------------|
| 120/121/122        | [Buffer Overflow](cwe_120.md)
| 119                | Improper Restriction of Operations within the Bounds of a Memory Buffer
| 476                | [NULL Pointer Dereference](cwe_476.md)
| 469                | [Use of Pointer Subtraction to Determine Size](cwe_469.md)
| 20, 457, 805, etc. | Improver Input Validation, Use of Uninitialized Variable, Buffer Access with Incorrect Length Value, etc.

## Prerequisite Tasks

### Raw Tasks
* Identify absence of NULL check (476)
* Identify absence of pointer initialization (824)
* Identify absence of size verification (120, 680)
* Identify absence of verification (119, 120)
* Identify buffer (119, 785, 787, 806) ❗ This should be most of them
* Identify buffer creation (785)
* Identify buffer overflow (680)
* Identify buffer read (119, 125, 126, 786, 788, 805, 806)
* Identify buffer write (119, 124, 786, 787, 788, 805, 806)
* Identify calculation (680)
* Identify code that copies buffers (120)
* Identify conversion to pointer (822)
* Identify expected length value (805)
* Identify failure condition (119)
* Identify function (466)
* Identify function call (785)
* Identify index (124, 125, 126, 786, 788)
* Identify invalid pointer (825)
* Identify location being written (121, 122)
* Identify location in buffer being written (119, 124, 125, 126, 786, 788, 805, 806)
* Identify max possible path size (785)
* Identify memory free (415, 416)
* Identify memory reference (416)
* Identify multiple usages of function (415)
* Identify operations on buffer (119)
* Identify path/file normalization (785)
* Identify pointer (124, 125, 126, 786, 788)
* Identify pointer arithmetic (823)
* Identify pointer dereference (476, 822, 825)
* Identify pointer initialization (824)
* Identify pointer offset (823)
* Identify pointer that might be NULL (476)
* Identify pointer usage (469, 824)
* Identify potential integer overflow (680)
* Identify precursor to memory allocation (680)
* Identify purpose of subtraction (469) ❓
* Identify return (466)
* Identify return type (466)
* Identify sequential operations (805)
* Identify size of buffer (120, 121, 122, 124, 126, 466, 786, 787, 788, 805, 806)
* Identify subtraction (469)
* Identify untrusted source (822)
* Identify usage of buffer size (806)
* Identify usage of function on variable (415)
* Identify valid buffer range (119, 805, 823)
* Identify valid pointer (823, 825)
* Identify value being obtained (822)
* Perform comparison of sizes (120, 121, 122, 125, 126, 466, 785, 787, 788, 805, 806)
* Perform comparison to 0 (120, 121, 122, 124, 125, 787, 805, 806)

### Organized
* Comparisons
    * Perform comparison of sizes (120, 121, 122, 125, 126, 466, 785, 787, 788, 805, 806)
    * Perform comparison to 0 (120, 121, 122, 124, 125, 787, 805, 806)
* Pointers
    * Identify pointer (124, 125, 126, 786, 788)
    * Identify absence of pointer initialization (824)
    * Identify conversion to pointer (822)
    * Identify invalid pointer (825)
    * Identify pointer arithmetic (823)
    * Identify pointer dereference (476, 822, 825)
    * Identify pointer initialization (824)
    * Identify pointer offset (823)
    * Identify pointer that might be NULL (476)
    * Identify pointer usage (469, 824)
    * Identify valid pointer (823, 825)
    * Identify absence of NULL check (476)
* Buffers & Memory
    * Identify absence of size verification (120, 680)
    * Identify absence of verification (119, 120)
    * Identify buffer (119, 785, 787, 806) ❗ This should be most of them
    * Identify buffer creation (785)
    * Identify buffer overflow (680)
    * Identify buffer read (119, 125, 126, 786, 788, 805, 806)
    * Identify buffer write (119, 124, 786, 787, 788, 805, 806)
    * Identify code that copies buffers (120)
    * Identify index (124, 125, 126, 786, 788)
    * Identify location in buffer being written (119, 121, 122, 124, 125, 126, 786, 788, 805, 806)
    * Identify memory free (415, 416)
    * Identify memory reference (416)
    * Identify operations on buffer (119)
    * Identify precursor to memory allocation (680)
    * Identify sequential operations (e.g., strncpy) (805)
    * Identify size of buffer (120, 121, 122, 124, 126, 466, 786, 787, 788, 805, 806)
    * Identify usage of buffer size (806)
    * Identify valid buffer range (119, 805, 823)
* Functions
    * Identify function (466)
    * Identify function call (785)
    * Identify multiple usages of function (415)
    * Identify usage of function on variable (415)
    * Identify function return (466)
    * Identify function return type (466)
* Math
    * Identify calculation (680)
    * Identify subtraction (469)

* Unsorted
    * Identify failure condition (119)
    * Identify max possible path size (785)
    * Identify path/file normalization (785)
    * Identify potential integer overflow (680)
    * Identify untrusted source (822)
    * Identify value being obtained (822)
