-- Arithmetic precedence and boolean operator behavior
let value = 2 + 3 * 4;
assert(value == 14, "multiplication should happen before addition");

let left_assoc = 20 - 5 - 5;
assert(left_assoc == 10, "subtraction should be left associative");

assert(14 > 10 && 14 < 20, "&& should combine two true comparisons");
assert(14 == 12 || 14 == 14, "|| should allow either side to be true");
assert(5 + 5 == 10);
