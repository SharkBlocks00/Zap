-- Foreach over variable-backed collection and string concatenation
let source = "zap";
let count = 0;

foreach (ch: source) {
    count = count + 1;
}

assert(count == 3, "foreach should iterate each character");
