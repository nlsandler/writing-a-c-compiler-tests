# Writing a C Compiler Test Suite

The test suite for [Writing a C Compiler](https://nostarch.com/writing-c-compiler), a hands-on guide to writing your own compiler for a big chunk of C. These tests are still a work in progress!

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

3. Run the valid test cases for chapters 1-5, but skip the invalid ones (useful when only your backend is buggy).

```
./test_compiler ~/mycc --chapter 4 --skip-invalid
```


notes:

- we often use global variables for our operands in Part II tests so they still cover what they're supposed to in Part III, but can be debugged separately from calling conventions

- use different return codes (and sometimes different functions) to make it easier to track where the problem is

- several tests rely on implementation-defined behavior (where the behavior is specified in the book). none of the valid programs have undefined behavior. 

- the invalid programs all violate constraints in the C standard, but some of them are are still accepted by common compilers

- the valid programs are not super fastidious about freeing memory; none of them are long-running in a way that could make memory leaks problematic
