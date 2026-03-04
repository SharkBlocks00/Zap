-- Elseif chain should evaluate first matching branch
let n = 12;
let branch = 0;

if (n < 10) {
    branch = 1;
} elseif (n == 12) {
    branch = 2;
} else {
    branch = 3;
}

assert(branch == 2, "elseif branch should run");
