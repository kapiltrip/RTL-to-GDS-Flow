# Runnable study examples

[Course index](../../../README.md) · [Lesson 11](../../../Daily%20Notes/Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) · [Lesson 12](../../../Daily%20Notes/Day%2002.md#lesson-12-hardware-modeling--introduction-to-verilog-ii)

The `.v` examples reproduce the complete code printed in the chapters. `tb_language.v` checks values and behavior; `tb_delays.v` checks the six assignment times from the lecture example. These are small teaching models, not a complete chip project.

| File | What to inspect |
|---|---|
| [select_register.v](select_register.v) | A multiplexer followed by a flip-flop |
| [mux_forms.v](mux_forms.v) | Combinational wire and procedural variable descriptions |
| [counter.v](counter.v) | Default width, parameter override, asynchronous reset, and wraparound |
| [pipeline2.v](pipeline2.v) | Nonblocking updates preserve the previous stage value |
| [initial_always_demo.v](initial_always_demo.v) | Initialization, a 20 ns clock period, unchanged counter state, and a finite run |
| [function_task_demo.v](function_task_demo.v) | Nine-bit sum returned from a function and printed by a task |
| [assignment_delays.v](assignment_delays.v) | Blocking updates at 10/40/60 ns and nonblocking updates at 10/30/20 ns |
| [tb_language.v](tb_language.v) | Four-state values, wildcard matching, widths, edges, and sequential behavior |
| [tb_delays.v](tb_delays.v) | Checks the settled values after each scheduled event time |

From the repository root, with Python including Tk/Tcl and Icarus Verilog installed:

```text
python Resources/examples/run_checks.py
```

The script uses Verilog-2005 mode, compiles into a temporary directory, runs the checks, and checks the [Tcl examples](../tcl_basics.tcl). The deliberate `6'h88` truncation demonstration may generate a compiler warning; its low-six-bit result is checked explicitly. Simulator finish-message formatting can vary by version.

To run only the assignment demonstration using tools on your PATH:

```text
iverilog -g2005 -s assignment_delays -o Resources/examples/verilog/assignment_delays.vvp Resources/examples/verilog/assignment_delays.v
vvp Resources/examples/verilog/assignment_delays.vvp
```

This prints changes in simulated values. `%t` formatting can display scaled time units according to simulator settings; the source declares a 1 ns unit and 1 ps precision. The chapter's table states times in nanoseconds.
