-- Break inside inner loop should not terminate outer loop
let outer = 0;
let total = 0;

while (outer < 3) {
    let letters = "ab";

    foreach (ch: letters) {
        total = total + 1;
        break;
    }

    outer = outer + 1;
}

assert(outer == 3, "outer loop should continue after inner break");
assert(total == 3, "inner loop should run once per outer iteration");
