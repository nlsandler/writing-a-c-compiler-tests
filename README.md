# Writing a C Compiler Test Suite

The test suite for the upcoming book [Writing a C Compiler](https://nostarch.com/writing-c-compiler), a hands-on guide to writing your own compiler for a big chunk of C. These tests are still a work in progress!

Each test case is a C program. Some (in the `valid/` subdirectories) are valid, and others (in the `invalid_*/` subdirectories) have compile-time errors.

The test runner compiles each test program with the compiler under test. An invalid test case passes if the compiler rejects it (i.e. terminates with a non-zero exit code and does not produce any output files). A valid test case passes if it's compiled correctly (i.e. the compiler produces an executable which, when run, produces the expected output and terminates with the expected exit code).

Some invalid test cases include errors that most compilers don't warn about by default. If GCC or Clang isn't complaining about an invalid test case, try compiling it again with the `-pedantic` flag.

## Prerequisites
You need the `gcc` command on your path. (On macOS this is an alias for Clang; this is fine.) You also need Python 3.8 or later.
## Quickstart

```
git clone https://github.com/nlsandler/writing-a-c-compiler-tests.git
cd writing-a-c-compiler-tests
git checkout complete-test-suite # until it's merged into main
./test_compiler --check-setup # make sure you meet all the system requirements
```

## Usage Examples


1. Run the tests for chapters 1-4
```
./test_compiler ~/mycc --chapter 4
```

2. Run the tests for chapter 4 but not chapters 1-3

```
./test_compiler ~/mycc --chapter 4 --latest-only
```

3. Run the valid test cases for chapters 1-4, but skip the invalid ones (useful when your frontend passess are working but the backend is buggy).

```
./test_compiler ~/mycc --chapter 4 --skip-invalid
```

4. Run the tests for chapters 1-4, stopping after the first test failure:

```
./test_compiler ~/mycc --chapter 4 -f
```

5. Run the tests for chapters 1-9; include tests for bitwise operations and switch statements (extra credit features) but not for other extra credit features.

```
./test_compiler ~/mycc --chapter 9 --bitwise --compound
```

6. Run test cases for chapter 1; specify that the compiler exits with code `1` or `2` if it hits a lexer or parser error. When specified, an invalid test case passes only if the compiler exits with one of these exit codes, and fails otherwise. Useful for distinguishing expected failures (i.e. the compiler detected an error) from unexpected failures (e.g. internal errors, segfaults).

```
./test_compiler ~/my_cc --chapter 1 --expected-error-codes 1 2
```

# Note for Early Access Readers

Two things have changed since the initial early access version of the book:
1. The chapter numbers have decreased by 1 (e.g. Chapter 2 in the EA version is now Chapter 1).
2. We now use `int main(void)` instead of `int main()` to declare a function with no parameters. You'll need to define a `void` token in the lexer and include it in the grammar rule for function definitions.
