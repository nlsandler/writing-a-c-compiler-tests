// can we come up with a program where we get different results from optimizing in different orders?
// current order: constant folding -> DCE -> copy prop -> DSE
/*
does one of these ever _prevent_ another? I think that's the key question

obviously no, except maaaaaaybe copy prop? by introducing new uses of things?




*/