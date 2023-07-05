# Writing a C Compiler Test Suite

notes:

- we often use global variables for our operands in Part II tests so they still cover what they're supposed to in Part III, but can be debugged separately from calling conventions

- use different return codes (and sometimes different functions) to make it easier to track where the problem is

- several tests rely on implementation-defined behavior (where the behavior is specified in the book). none of the valid programs have undefined behavior. 

- the invalid programs all violate constraints in the C standard, but some of them are are still accepted by common compilers

- the valid programs are not super fastidious about freeing memory; none of them are long-running in a way that could make memory leaks problematic
