-- Const values can be read and used in expressions
const base = 10;
let result = base + 5;
assert(result == 15, "const should be usable in expressions");

-- Reassigning parent variable inside block should update parent scope
let count = 1;
if (true) {
    count = count + 4;
}
assert(count == 5, "assignment in child scope should resolve to parent variable");
