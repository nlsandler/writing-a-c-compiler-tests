struct incomplete;

struct s {
  // member type is invalid: pointer to array of struct incomplete,
  // but can't have array of incomplete type
  struct incomplete (*array_pointer)[3];
};