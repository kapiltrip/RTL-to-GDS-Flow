# Checked study examples

[Master index](../../README.md) · [Earlier Verilog examples](verilog/README.md)

The examples are small teaching checks. They do not establish that a full implementation or timing-closure flow has been run.

| Example | Study purpose | Notes |
|---|---|---|
| [queue_demo.v](queue_demo.v) | Observe an active-region value before a nonblocking update, then the settled value | [Day 03, Lesson 13](../../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| [counter_simulation.v](counter_simulation.v) | Explicitly assert asynchronous reset, then check counting and wraparound | [Day 03, Lesson 18](../../Daily%20Notes/Day%2003.md#lesson-18-simulation-based-verification-using-icarus) |
| [tcl_basics.tcl](tcl_basics.tcl) | Lists, procedures, command substitution and file channels | [Day 02, Lesson 10](../../Daily%20Notes/Day%2002.md#lesson-10-introduction-to-tcl) |

With Python, Icarus Verilog and Tcl available, run from the repository root:

```text
python Resources/examples/run_checks.py
python Resources/examples/check_new_study_examples.py
python Resources/examples/check_wrapup_examples.py
python Resources/examples/check_depth_examples.py
```

| Checker | Evidence it establishes |
|---|---|
| [run_checks.py](run_checks.py) | Verilog language, width, four-state, delay, parameter, function/task and clock behavior; Tcl list/procedure/file examples. |
| [check_new_study_examples.py](check_new_study_examples.py) | Extracted simulation programs, prime covers, factoring/CNF, FSM refinement, cutpoints, ROBDDs, interpolation and timing examples from the earlier chapters. |
| [check_wrapup_examples.py](check_wrapup_examples.py) | Good/faulty ATPG networks, scan loading, LFSR periods, DVFS, useful skew, wire resistance and PDN calculations. |
| [check_depth_examples.py](check_depth_examples.py) | The 26 notebook-depth additions: four-state/delayed sampling, signed arithmetic, care masks, BDD order, induction, scan/signature traces and dimensional calculations. |

Compilation products and waveforms stay in temporary directories. `check_new_study_examples.py` refreshes `queue_demo.v` and `counter_simulation.v` from the editable notes. Its cover search independently enumerates legal cubes and all small selections, establishing four primes and two minimum three-term covers for A-14.

The queue check prints `active a=0` followed by `settled a=1`. The counter check prints `PASS: reset, count and wrap`. The arithmetic and Boolean check reports its verified topics. A successful simulation is evidence for the asserted cases and stated assumptions.

## Final-week and notebook-depth checks

[check_wrapup_examples.py](check_wrapup_examples.py) enumerates the notebook ATPG networks and recomputes scan loading, LFSR periods, DVFS, useful skew, wire resistance and PDN examples. [check_depth_examples.py](check_depth_examples.py) simulates the new four-state and delayed-sampling examples, exhaustively checks signed eight-bit divide/shift correction, and constructs the care masks, equality BDDs, reachable/inductive state sets, signature collisions and scan permutations used in the expanded notes. It also checks the new dimensional calculations.

Reports are written to ignored `../tools/pdf/qa`; temporary compilation products are not reader sources. Passing these checks establishes the stated small teaching cases, not a complete synthesis, OpenSTA, OpenROAD or fabrication-signoff result.
