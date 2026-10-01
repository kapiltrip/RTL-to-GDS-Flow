# Checked study examples

[Master index](../../README.md) · [Earlier Verilog examples](verilog/README.md)

The examples are small teaching checks. They do not establish that a full implementation or timing-closure flow has been run.

| Example | Study purpose | Notes |
|---|---|---|
| [queue_demo.v](queue_demo.v) | Observe an active-region value before a nonblocking update, then the settled value | [Day 03, Lesson 13](../../Day%2003.md#lesson-13-functional-verification-using-simulation) |
| [counter_simulation.v](counter_simulation.v) | Explicitly assert asynchronous reset, then check counting and wraparound | [Day 03, Lesson 18](../../Day%2003.md#lesson-18-simulation-based-verification-using-icarus) |
| [tcl_basics.tcl](tcl_basics.tcl) | Lists, procedures, command substitution and file channels | [Day 02, Lesson 10](../../Day%2002.md#lesson-10-introduction-to-tcl) |

With Python, Icarus Verilog and Tcl available, run from the repository root:

```text
python Resources/examples/run_checks.py
python Resources/examples/check_new_study_examples.py
```

The earlier check covers the printed Verilog and Tcl examples. The new check extracts the simulation programs from the editable notes, compiles the wildcard-case fragment, exhaustively compares the small Boolean examples, and independently recomputes the displayed timing and interpolation results. It enumerates legal cubes and all small covers for the restored A-14 chart, establishing its four primes and two minimum three-term covers, and checks all assignments for the added UNSAT contrast. Compilation products and waveforms stay in temporary directories. The script refreshes the two named example files from the notes.

The queue check prints `active a=0` followed by `settled a=1`. The counter check prints `PASS: reset, count and wrap`. The arithmetic and Boolean check reports its verified topics. A successful simulation is evidence for the asserted cases and stated assumptions.

The formal reading edition adds exhaustive checks for priority selection, a gate's exact CNF relation, Moore-state partition refinement, reachable cutpoint invariants and a fanout counterexample to a local don't-care change. Independent calculations verify the new cost, speedup, width, overlay, timing, interpolation and common-clock-path examples. Tcl executes the staged substitution cases, and a finite-state reachability calculation checks its fixed point and unreachable-state result.
