# PhD Vulnerability Detection Prerequisites

## Draper VDISC CWEs
| CWE ID             | CWE Description |
|--------------------|-----------------|
| 120/121/122        | [Buffer Overflow](cwe_120.md)
| 119                | Improper Restriction of Operations within the Bounds of a Memory Buffer
| 476                | [NULL Pointer Dereference](cwe_476.md)
| 469                | [Use of Pointer Subtraction to Determine Size](cwe_469.md)
| 20, 457, 805, etc. | Improper Input Validation, Use of Uninitialized Variable, Buffer Access with Incorrect Length Value, etc.

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
    * [1] Perform comparison of sizes (120, 121, 122, 125, 126, 466, 785, 787, 788, 805, 806)
    * [1] Perform comparison to 0 (120, 121, 122, 124, 125, 787, 805, 806)
* Pointers
    * [4] Identify pointer (124, 125, 126, 786, 788)
    * [5] Identify absence of pointer initialization (824)
    * [4] Identify conversion to pointer (822)
    * [2] Identify invalid pointer (825)
    * [4] Identify pointer arithmetic (823)
    * [4] Identify pointer dereference (476, 822, 825)
    * [4] Identify pointer initialization (824)
    * [4] Identify pointer offset (823)
    * [2] Identify pointer that might be NULL (476)
    * [4] Identify pointer usage (469, 824)
    * [2] Identify valid pointer (823, 825)
    * [5] Identify absence of NULL check (476)
* Buffers & Memory
    * [5] Identify absence of size verification (120, 680)
    * [5] Identify absence of verification (119, 120)
    * [4] Identify buffer (119, 785, 787, 806) ❗ This should be most of them
    * [4] Identify buffer creation (785)
    * [ ] Identify buffer overflow (680)
    * [4] Identify buffer read (119, 125, 126, 786, 788, 805, 806)
    * [4] Identify buffer write (119, 124, 786, 787, 788, 805, 806)
    * [2] Identify code that copies buffers (120)
    * [4] Identify index (124, 125, 126, 786, 788)
    * [4] Identify location in buffer being written (119, 121, 122, 124, 125, 126, 786, 788, 805, 806)
    * [4] Identify memory free (415, 416)
    * [4] Identify memory reference (416)
    * [4] Identify operations on buffer (119)
    * Identify precursor to memory allocation (680)
    * [4] Identify sequential operations (e.g., strncpy) (805)
    * [2] Identify size of buffer (120, 121, 122, 124, 126, 466, 786, 787, 788, 805, 806)
    * [4] Identify usage of buffer size (806)
    * [2] Identify valid buffer range (119, 805, 823)
* Functions
    * [4] Identify function (466)
    * [4] Identify function call (785)
    * Identify multiple usages of function (415)
    * Identify usage of function on variable (415)
    * [4] Identify function return (466)
    * [4] Identify function return type (466)
* Math
    * [4] Identify calculation (680)
    * [4] Identify subtraction (469)

* Unsorted
    * Identify failure condition (119)
    * Identify max possible path size (785)
    * Identify path/file normalization (785)
    * Identify potential integer overflow (680)
    * Identify untrusted source (822)
    * Identify value being obtained (822)

### Major Tasks
1. Perform comparison between two explicit or implicit values (e.g., `x > y`)
    * Values listed explicitly in the code
    * Values that are calculable, even if symbolically, based on the code
    * Values that are known to programmers or environments, but are not in the code.
2. Track variable value across multiple statements. (e.g., `x = 0; x++; y = 1; x += y`)
    * Concrete values, explicitly calculable based on the code
    * Symbolic values, based only on relationships and possible ranges
3. Track code flow (e.g., `x = 0; if(x < 1) { x = 1 }`)
4. Identify code based on patterns of usage (this is what ANNs do!)
    * Identify variable
5. Make positive prediction based on presence of some code and absence of other code.

## Method

> **Hypothesis:** Existing MLAVD models are performing advanced pattern recognition, but do not have the capability to truly detect vulnerabilities.

### Test 1: Raw Comparisons
> Test performance of models on simple relational operations.
```c
[number 1] > [number 2]
```

Variables
* Numbers (int, float, values)
* Operators (`<`, `>`, `<=`, `>=`, `==`, `!=`)

### Test 2: Tracking values
> Test ability of models to track values across statements
```c
x = [number 1]
y = [number 2]
x > y
```

Additional Variables
* Variable names / comparison order
* Assignment order

### Test 3: Perform calculations
> Test ability of models to perform/understand arithmetic calculations
```c
x = [number 1]
y = [number 2]
x = x + 1
y = y + 100
y = x * 1
x > y
```

Additional Variables
* Arithmetic operators (`+`, `-`, `*`, `/`, `%`, `++`, `--`, `x=`)
* Number of arithmetic operations

### Test 4: Control Flow
> Test if models can track values through conditional statements.

```c
x = [number 1]
y = [number 2]

if (x > [number 3]) {
    x = y + 1
} else {
    y *= 1000
}
x > y
```

Additional Variables
* Logical operators (`&&`, `||`, `!`)
* Number of comparisons in if-statement
* Nesting of if statements

### Test 5: Relative Values
> Test if models can understand relative values.
```c
x, y
x = x * y
x > y
```