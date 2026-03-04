-- Functions should be able to mutate outer-scope variables
let calls = 0;

func tick = define() {
    calls = calls + 1;
}

tick();
tick();
tick();

assert(calls == 3, "function should update captured outer variable");
