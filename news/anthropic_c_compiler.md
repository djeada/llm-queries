Source: [https://www.anthropic.com/engineering/building-c-compiler](https://www.anthropic.com/engineering/building-c-compiler)

## Notes on the “no human input” claim

The post frames this as “we build a compiler with no human input,” but it leaves out two important points:

* **Training-data overlap is likely.** A C compiler is built around a well-known language spec, and there is a huge amount of public material about C, compilers, and toolchains that plausibly exists in model training data. That does not invalidate the result, but it means **this is not a clean evaluation** in the machine-learning sense. Testing on content that resembles training data can overstate generalization.

* **Shortcomings and patch cost are underplayed.** The implementation works, but the write-up does not clearly enumerate limitations, failure cases, or the engineering effort required to patch edge cases. In practice, chasing correctness and compatibility often costs more than getting an initial prototype working.

That said: **it does work**, and it works surprisingly well for what is being claimed.

## Building and a first compile

Build:

```bash
cargo build --release
```

Hello world:

```c
#include <stdio.h>

int main() {
    printf("hello world\n");
    return 0;
}
```

Compile:

```bash
./target/release/ccc -o hello hello.c
```

## Some things don’t work as expected

### 1) `const` is not enforced (repro)

```c
int main(void) {
    const int x = 1;
    x = 7;          // GCC: error, CCC: accepts
    return x;
}
```

Observed:

* `ccc`: compiles; program exits with code `7`
* `gcc -std=c11 -Wall -Wextra -Werror`: `error: assignment of read-only variable 'x'`

Also reproduced with:

```c
const int a[2] = {1,2};
a[0] = 3;          // GCC errors, CCC accepts
```

### 2) Same-scope redeclaration with a different type is accepted (repro)

```c
int main(void) {
    int x = 1;
    float x = 7.25f;   // GCC: conflicting types, CCC: accepts
    return (int)x;
}
```

Observed:

* `ccc`: compiles and runs (exit `7`)
* `gcc`: `error: conflicting types for 'x'`

## A more complex C feature demo

This single-file program exercises a broad slice of C features (macros, token stringification, enums, typedefs, function pointers, structs, bitfields, unions, designated initializers, compound literals, variadics, recursion).

File: `hello.c`

```c
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>

#define ARR_LEN(a) (sizeof(a) / sizeof((a)[0]))
#define SQR(x) ((x) * (x))
#define STR(x) #x
#define XSTR(x) STR(x)

#define MAKE_CONST(name, value) enum { name = (value) }
MAKE_CONST(MAGIC_NUMBER, 1337);

typedef int (*unary_fn)(int);

struct Node {
    int value;
    struct Node *next;
};

struct Flags {
    unsigned enabled : 1;
    unsigned mode : 3;
    signed bias : 4;
};

union U32Bytes {
    uint32_t u32;
    unsigned char b[4];
};

struct Point {
    int x;
    int y;
};

struct Rect {
    struct Point tl;
    struct Point br;
};

static int square(int x) { return SQR(x); }

static int map_sum(const int *arr, size_t n, unary_fn fn) {
    int total = 0;
    for (size_t i = 0; i < n; i++) total += fn(arr[i]);
    return total;
}

static int sum_variadic(size_t n, ...) {
    va_list ap;
    va_start(ap, n);
    int total = 0;
    for (size_t i = 0; i < n; i++) total += va_arg(ap, int);
    va_end(ap);
    return total;
}

static int gcd(int a, int b) {
    return (b == 0) ? a : gcd(b, a % b);
}

static int list_sum(const struct Node *n) {
    int total = 0;
    while (n) {
        total += n->value;
        n = n->next;
    }
    return total;
}

static int rect_area(struct Rect r) {
    int w = r.br.x - r.tl.x;
    int h = r.tl.y - r.br.y;
    return w * h;
}

int main(void) {
    int arr[] = {1, 2, 3, 4, 5};
    int mapped = map_sum(arr, ARR_LEN(arr), square);      /* 55 */
    int variadic = sum_variadic(4, 10, 20, 30, 40);       /* 100 */
    int g = gcd(84, 18);                                  /* 6 */

    int lut[8] = {[0] = 1, [3] = 7, [7] = 9};             /* designated init */
    int lut_sum = lut[0] + lut[3] + lut[7];               /* 17 */

    int *tmp = (int[]){10, 20, 30};                       /* compound literal */
    int tmp_sum = tmp[0] + tmp[1] + tmp[2];               /* 60 */

    struct Node n3 = {.value = 3, .next = NULL};
    struct Node n2 = {.value = 2, .next = &n3};
    struct Node n1 = {.value = 1, .next = &n2};
    int chain = list_sum(&n1);                            /* 6 */

    struct Flags f = {.enabled = 1, .mode = 5, .bias = -3};
    int flag_score = (int)f.enabled + (int)f.mode + (int)f.bias; /* 3 */

    union U32Bytes u = {.u32 = 0x11223344u};
    int little_endian = (u.b[0] == 0x44u);

    struct Rect r = {
        .tl = {.x = 1, .y = 8},
        .br = {.x = 6, .y = 2},
    };
    int area = rect_area(r);                              /* 30 */

    int checksum = mapped + variadic + g + lut_sum + tmp_sum + chain + flag_score + area;

    printf("C feature demo\n");
    printf("magic=%d token=%s\n", MAGIC_NUMBER, XSTR(MAGIC_NUMBER));
    printf("mapped=%d variadic=%d gcd=%d area=%d\n", mapped, variadic, g, area);
    printf("list=%d flags=%d endian=%s\n", chain, flag_score, little_endian ? "little" : "big");
    printf("checksum=%d\n", checksum);

    /* 55 + 100 + 6 + 17 + 60 + 6 + 3 + 30 = 277 */
    return (checksum == 277) ? 0 : 1;
}
```

Compile and run:

```bash
./target/release/ccc -o hello hello.c
./hello
```

Expected output:

```
C feature demo
magic=1337 token=MAGIC_NUMBER
mapped=55 variadic=100 gcd=6 area=30
list=6 flags=3 endian=little
checksum=277
```

## CCC vs GCC Optimization Benchmark

### Environment

* Host kernel: `Linux 6.8.0-90-generic x86_64 GNU/Linux`
* CPU: `AMD Ryzen 5 7535HS with Radeon Graphics`
* GCC: `gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0`
* CCC: `ccc (Claude's C Compiler, GCC-compatible) 14.2.0`
* Source file: `hello.c`
* Optimization flags: `-O2 -march=native`

### Commands Used

```bash
# Build executables
./target/release/ccc -O2 -march=native -o /tmp/a_ccc hello.c
gcc -O2 -march=native -o /tmp/a_gcc hello.c

# Correctness
/tmp/a_ccc > /tmp/out_ccc.txt
/tmp/a_gcc > /tmp/out_gcc.txt
diff -u /tmp/out_ccc.txt /tmp/out_gcc.txt

# Binary size
size /tmp/a_ccc /tmp/a_gcc
stat -c '%n %s bytes' /tmp/a_ccc /tmp/a_gcc

# Compile-time (20x each)
/usr/bin/time -f 'ccc_compile_20x_s %e' bash -lc 'for i in $(seq 1 20); do ./target/release/ccc -O2 -c hello.c -o /tmp/a_ccc.o; done'
/usr/bin/time -f 'gcc_compile_20x_s %e' bash -lc 'for i in $(seq 1 20); do gcc -O2 -c hello.c -o /tmp/a_gcc.o; done'

# Runtime (500x each)
/usr/bin/time -f 'ccc_run_500x_s %e' bash -lc 'for i in $(seq 1 500); do /tmp/a_ccc >/dev/null; done'
/usr/bin/time -f 'gcc_run_500x_s %e' bash -lc 'for i in $(seq 1 500); do /tmp/a_gcc >/dev/null; done'
```

### Results

#### Correctness

* Status: `MATCH` (stdout identical for `hello.c`)

#### Compile Time

* CCC (20 compiles): `0.31s`
* GCC (20 compiles): `0.60s`
* Relative: CCC was about `1.94x` faster in this run

#### Runtime

* CCC binary (500 runs): `0.41s`
* GCC binary (500 runs): `0.44s`
* Relative: CCC binary was about `1.07x` faster in this run

#### Size

`size` output:

```text
   text   data    bss    dec    hex filename
   3158    440      1   3599    e0f /tmp/a_ccc
   2340    616      8   2964    b94 /tmp/a_gcc
```

File size on disk:

```text
/tmp/a_ccc 14664 bytes
/tmp/a_gcc 16112 bytes
```

Observations:

* Section totals (`dec`) were smaller for GCC.
* Final ELF file size on disk was smaller for CCC.

## CCC Pass Timing Snapshot (`CCC_TIME_PASSES=1`)

Top changes in the logged pass run included:

* `dce`: `205` changes (iter 0)
* `narrow`: `27` changes (iter 0)
* `copy_prop2`: `12` changes (iter 0)
* `cfg_simplify2`: `10` changes (iter 0)
* `gvn_total`: `12` changes (iter 0)
* `licm_total`: `6` changes (iter 0)

The optimizer converged by iter 2 with `0` changes in the final reported passes.

## Limitations

* `hyperfine` was not available in this environment, so `/usr/bin/time` + shell loops were used.
* The benchmark target is a single file (`hello.c`), which is too small to draw strong conclusions about optimizer quality.
* For meaningful optimization comparison, repeat this method on compute-heavy kernels (tight loops, math kernels, branch-heavy code) and on larger codebases.

