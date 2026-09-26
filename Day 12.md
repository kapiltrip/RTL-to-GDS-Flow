# Day 12 — Hardware Modeling — Introduction to Verilog II

[Course index](README.md) · Week 3 · [Lecture video](https://www.youtube.com/watch?v=XEtpwZDhdTk) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [Modules ports hierarchy and parameters](#modules-ports-hierarchy-and-parameters)
- [Operators and bit-level examples](#operators-and-bit-level-examples)
- [Processes event controls and four-state edges](#processes-event-controls-and-four-state-edges)
- [Functions and tasks](#functions-and-tasks)
- [Continuous blocking and nonblocking assignment](#continuous-blocking-and-nonblocking-assignment)
- [System tasks and the next study boundary](#system-tasks-and-the-next-study-boundary)

## Modules ports hierarchy and parameters

![A module can be reused with different elaboration-time parameters](images/Day%2012/01-modules.png)

*Video frame: [8:41](https://www.youtube.com/watch?v=XEtpwZDhdTk&t=521s). A module can be reused with different elaboration-time parameters*


A **module** is a named hardware description with an interface and an implementation. Its ports connect it to a surrounding module: `input` receives a value, `output` drives outward, and `inout` represents a bidirectional connection. Instantiating a module creates a particular instance in the design hierarchy. Multiple instances of one definition are distinct pieces of modeled hardware, each with its own connections and state.

Named port connections make the interface explicit: `.clk(clk)` connects the child port `clk` to the parent's signal `clk`. The names need not be identical. An instance name such as `u_counter` is different from its module type `counter`; this is the same type-versus-instance distinction used for library pins in [Day 06](Day%2006.md#library-pins-and-instance-pins).

A **parameter** is a constant chosen during elaboration, when the simulator or synthesis tool constructs the design hierarchy and sizes. It is not a runtime input. A default can be overridden for an instance. A `localparam` is useful for a derived constant that an instance should not override. Changing an input while a design runs changes a signal; changing a parameter requires a differently elaborated design.

![Kapil’s handwritten notes — Part 2, PDF page 3, parameter and edge-event notes](images/Day%2012/h02-parameters-events.jpg)

*Handwritten source: Part 2, PDF page 3, parameter and edge-event notes.*


Your default/override example means “use this constant unless this instance supplies another.” The following complete example creates an eight-bit counter from a module whose default width is four. `WIDTH` must be at least one.

```verilog
module counter #(parameter WIDTH = 4) (
    input wire clk, rst_n, enable,
    output reg [WIDTH-1:0] count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= {WIDTH{1'b0}};
        else if (enable)
            count <= count + {{(WIDTH-1){1'b0}}, 1'b1};
    end
endmodule

module counter_top (
    input wire clk, rst_n, enable,
    output wire [7:0] count
);
    counter #(.WIDTH(8)) u_counter (
        .clk(clk), .rst_n(rst_n), .enable(enable), .count(count)
    );
endmodule
```

When reset becomes low, `count` clears without waiting for a rising clock; this is an **asynchronous active-low reset**. When reset is high and `enable` is high at a rising edge, the counter increments. When disabled, a clocked variable retaining its old value is intentional register behavior. After 255, the eight-bit counter wraps to zero because the carry exceeds the declared width. This coding example specifies behavior; a real reset network also needs an appropriate reset-release strategy and timing checks.

## Operators and bit-level examples

![Bitwise operations, concatenation, replication, and conditional selection](images/Day%2012/02-operators.png)

*Video frame: [16:19](https://www.youtube.com/watch?v=XEtpwZDhdTk&t=979s). Bitwise operations, concatenation, replication, and conditional selection*


An operator combines values according to its own width, signedness, and four-state rules. Do not substitute a logical operator for a bitwise one merely because their symbols look similar.

| Operation | Example | Result and meaning |
|---|---|---|
| Bitwise AND | `4'b1010 & 4'b1100` | `4'b1000`, one AND per bit position |
| Logical AND | `4'b1010 && 4'b1100` | `1'b1`, both operands are nonzero |
| Reduction AND | `&4'b1110` | `1'b0`, AND all bits of one operand |
| Reduction XOR | `^4'b1011` | `1'b1`, odd parity of the operand |
| Bitwise complement | `~4'b1010` | `4'b0101` |
| Logical negation | `!4'b1010` | `1'b0` |
| Concatenation | `{4'b1010, 4'b1100}` | `8'b10101100` |
| Replication | `{3{2'b10}}` | `6'b101010` |
| Logical right shift | `4'b1000 >> 1` | `4'b0100` |

Arithmetic right shift `>>>` fills with the sign bit when the left operand is signed; an unsigned left operand does not become signed merely because `>>>` is used. Addition, subtraction, multiplication, division, and remainder describe arithmetic operations, but their hardware costs differ greatly. A multiplication by a power of two may simplify to wiring and width handling; a general multiplier requires more logic. Division is not universally a small combinational operation.

**Signedness check:** the surrounding expression can affect operand interpretation. For a signed eight-bit `s=-6`, assign `s >>> 1` to a signed eight-bit temporary and it holds `11111101` (−3). Comparing the shift directly against an **unsigned** based literal can coerce the comparison operands and alter the shift's interpretation. The runnable checks demonstrate both cases. Keep intermediate signed results explicitly signed, and use deliberate casts or signed constants when combining them with other expressions.

Concatenation places the leftmost item in the most significant portion. Nested replication needs its own braces. For a one-bit `a`, two-bit `b`, and one-bit `c`, `{{4{a}}, b, {2{c}}}` has eight bits: four copies of `a`, then the two bits of `b`, then two copies of `c`. Replication counts must be appropriate constant expressions, such as parameters.

The conditional expression `sel ? b : a` selects `b` for a true condition and `a` for a false condition. For a one-bit unknown condition, equal-width four-state vector alternatives are merged bit by bit: equal known bits survive and differing bits become `x`. For example, `1'bx ? 4'b1010 : 4'b1001` yields `4'b10xx`. This differs from a procedural `if` whose condition evaluates to unknown, which does not execute its true branch.

Operator precedence determines how an unparenthesized expression is grouped. Use parentheses to state the intended comparison and logical grouping, especially when mixing bitwise, equality, shift, and arithmetic operators. Parentheses clarify grouping; they do not by themselves widen an expression or change unsigned operands into signed values.

## Processes event controls and four-state edges

![Event controls suspend a process until a specified signal transition](images/Day%2012/03-events.png)

*Video frame: [24:13](https://www.youtube.com/watch?v=XEtpwZDhdTk&t=1453s). Event controls suspend a process until a specified signal transition*


An `initial` process starts once at simulation time zero. An `always` process repeatedly executes its statement for the duration of simulation. Different processes are concurrent; no source-code ordering guarantees which separate time-zero process runs first. A repeating process needs a blocking event or delay along its execution path. `always begin a = ~a; end` has no time advance and can trap the simulator in a zero-time loop.

`begin ... end` groups sequentially executed statements within one process. “Sequentially executed statements” does not automatically mean “sequential hardware”: a combinational process also executes statements in order. `fork ... join` starts concurrent branches and waits for all of them to finish; it is particularly useful in testbenches.

An **event control** suspends a process until the specified event occurs. `@(a or b)` reacts to changes of either operand. `@(posedge clk)` reacts to a positive-edge event. In traditional combinational RTL, `always @*` automatically collects the signals read by that process, avoiding an accidentally incomplete hand-written sensitivity list. Give every combinational output a value on every control-flow path. Otherwise the output must retain an earlier value, which can infer a latch.

The slide's `always @(en)` illustration reacts whenever `en` changes; it does not remain active throughout the time `en` is high. If its body reads another variable, changing that other variable alone does not trigger this particular event control. It is an event-control illustration, not a complete template for a combinational multiplexer or a transparent latch. Use the complete `always @*` example in Day 11 when modeling combinational selection.

Your handwritten edge list includes unknown and high-impedance transitions. The precise single-bit simulation rules are:

| Event | Transitions that trigger it |
|---|---|
| `posedge` | `0→1`, `0→x`, `0→z`, `x→1`, `z→1` |
| `negedge` | `1→0`, `1→x`, `1→z`, `x→0`, `z→0` |
| Neither edge | `x→z`, `z→x`, or no value change |

These are language event rules; they do not promise that an uncertain electrical clock transition is safe. Establish a known testbench clock before measuring behavior. For a multi-bit expression used directly as an edge event, the edge detection concerns its least significant bit; ordinary clock signals should be one bit.

A `for` loop does not automatically consume a clock cycle per iteration. A statically bounded loop describing combinational work may be unrolled into parallel logic. A testbench loop containing `@(posedge clk)` explicitly waits for edges. Hardware cost and latency come from the full description and synthesis interpretation, not from the word `for` alone.

## Functions and tasks

![Traditional Verilog functions and tasks have different timing rules](images/Day%2012/05-functions.png)

*Video frame: [31:54](https://www.youtube.com/watch?v=XEtpwZDhdTk&t=1914s). Traditional Verilog functions and tasks have different timing rules*


Functions and tasks package reusable procedural work. Calling one is not the same as instantiating a module. A function computes a return value for an expression; a task is invoked as a statement and can communicate through output or inout arguments. These lessons use **traditional Verilog** rules; SystemVerilog extends several of them.

![Kapil’s handwritten notes — Part 2, PDF page 4, function/task comparison and assignment notes](images/Day%2012/h01-functions.jpg)

*Handwritten source: Part 2, PDF page 4, function/task comparison and assignment notes.*


| Traditional Verilog feature | Function | Task |
|---|---|---|
| Returned result | One function return value | No function-style return value; can use output/inout arguments |
| Arguments | At least one input; input arguments only | Zero or more input/output/inout arguments |
| Time-consuming controls | No `#`, `@`, or `wait` that suspends execution | May contain timing/event controls |
| Calls | Can call other functions, not tasks | Can call functions and tasks |
| Invocation | Used in an expression | Used as a procedural statement |

“Function executes in zero simulation time” means it does not advance the simulator's time; evaluating it still requires computation. “Task can take time” means permission, not obligation: a task without a wait or delay can also finish in the current time slot. These facts do not automatically classify one as combinational hardware and the other as sequential hardware. Synthesizability depends on the body and how it is called.

By default, traditional task/function locals have static lifetime. `automatic` creates separate storage per invocation, which matters for recursion or overlapping calls. This complete demonstration keeps arithmetic in a function and console output in a task:

```verilog
module function_task_demo;
    function [8:0] add8;
        input [7:0] a, b;
        begin
            add8 = {1'b0, a} + {1'b0, b};
        end
    endfunction

    task show_sum;
        input [7:0] a, b;
        reg [8:0] result;
        begin
            result = add8(a, b);
            $display("%0d + %0d = %0d", a, b, result);
        end
    endtask

    initial begin
        show_sum(8'd200, 8'd100);
        $finish;
    end
endmodule
```

The printed result is 300. Widening the inputs before adding preserves the ninth carry bit. The module as a whole is a demonstration testbench because it prints and finishes simulation; the arithmetic operation can separately be used in suitable synthesizable logic.

## Continuous blocking and nonblocking assignment

![Blocking delays accumulate while delayed nonblocking updates are scheduled independently](images/Day%2012/04-assignments.png)

*Video frame: [43:36](https://www.youtube.com/watch?v=XEtpwZDhdTk&t=2616s). Blocking delays accumulate while delayed nonblocking updates are scheduled independently*


A **continuous assignment**, such as `assign y = a & b;`, continuously drives a net as its source expression changes. A **procedural assignment** runs when execution reaches it inside a process. Traditional combinational procedural code commonly uses blocking `=`, while clocked state updates commonly use nonblocking `<=`.

With **blocking assignment**, the process completes that assignment before moving to its next statement. Without an explicit delay, the new value is available to following statements in that process immediately. With **nonblocking assignment**, the process evaluates the right-hand expression when the statement executes and schedules the destination update. With no explicit delay, that update occurs in the nonblocking-assignment region of the **current simulation time slot**, after the relevant active-region execution. It does not wait until the entire simulation ends or automatically wait for another clock edge.

This last distinction refines your two-step RHS/LHS note and the lecture's informal “end of simulation time” language. The simulator can process many events at one timestamp. Event ordering within that timestamp is different from advancing time to the next timestamp. The next dedicated simulation lesson develops scheduling in more detail; here we need enough to read RTL correctly.

Consider two registers in a pipeline:

```verilog
module pipeline2 (
    input wire clk, rst_n,
    input wire [7:0] d,
    output reg [7:0] q1, q2
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q1 <= 8'd0;
            q2 <= 8'd0;
        end else begin
            q1 <= d;
            q2 <= q1;
        end
    end
endmodule
```

At a normal rising clock edge, `q1` schedules the current input, while `q2` schedules the **old** value of `q1`. If old `q1=10` and `d=25`, the settled post-edge values are `q1=25`, `q2=10`. Both right-hand expressions were evaluated before their pending updates. If both lines instead used blocking assignment in this same order, the second line would observe the newly assigned `q1`, changing the model's behavior. Nonblocking assignment expresses the simultaneous sampling behavior expected from clocked registers.

### Follow one sample through both registers

Assume reset has established `q1=q2=0`, reset is released away from a sampling edge, and each input below is stable before its rising edge. Read the last two columns after the nonblocking updates for that edge have completed:

| Rising edge | Input `d` before the edge | Old `q1` sampled by `q2` | New `q1` | New `q2` |
|---|---|---|---|---|
| First | 25 | 0 | 25 | 0 |
| Second | 42 | 25 | 42 | 25 |
| Third | 9 | 42 | 9 | 42 |

The sample 25 enters `q1` on the first edge and reaches `q2` on the second. Once the pipeline is filled, a new sample can emerge at every edge even though each sample passes through two registers. This separates **latency**, the delay experienced by a particular sample, from **throughput**, the rate of completed samples. When stating a cycle latency, identify the reference event: here `q2` changes one clock period after the edge that first captures the sample into `q1`.

The assignments run at the same simulation timestamp as the edge; the table does not require time to advance by a full period before `q1` updates. It requires the pending nonblocking assignments to settle. An observation made immediately in an active-region process at `posedge clk` can still see the old register values. This is why a waveform's timestamp and its event ordering both matter.

### The lecture's delayed-assignment example

The following is a complete, explicitly timed simulation example. These `#` delays are for understanding the language; they are not a synthesizable implementation of arbitrary hardware delays.

```verilog
`timescale 1ns/1ps
module assignment_delays;
    reg a, b, c, p, q, r;
    initial begin
        a = 0; b = 0; c = 0;
        a = #10 1'b1;
        b = #30 1'b1;
        c = #20 1'b1;
    end
    initial begin
        p = 0; q = 0; r = 0;
        p <= #10 1'b1;
        q <= #30 1'b1;
        r <= #20 1'b1;
    end
    initial begin
        $monitor("t=%0t a=%b b=%b c=%b p=%b q=%b r=%b",
                 $time, a, b, c, p, q, r);
        #61 $finish;
    end
endmodule
```

| Destination | Becomes one at | Why |
|---|---:|---|
| `a` | 10 ns | First blocking assignment delays its completion by ten |
| `b` | 40 ns | Execution reaches it at ten, then waits another thirty |
| `c` | 60 ns | Execution reaches it at forty, then waits another twenty |
| `p` | 10 ns | Scheduled from time zero with a delay of ten |
| `q` | 30 ns | Scheduled from time zero with a delay of thirty |
| `r` | 20 ns | Scheduled from time zero with a delay of twenty |

Here the delay is **inside** the assignment: `p <= #10 expression` samples the expression now and schedules the write ten time units later. Moving the delay in front, `#10 p <= expression`, first suspends the process and then evaluates the expression. These forms can produce different results if inputs change during the delay. The example uses constant RHS values to isolate scheduling.

## System tasks and the next study boundary

System task/function names start with `$`. `$display` prints when it executes; `$monitor` reports changes to its argument values at the end of the time step; `$time` returns simulation time; `$finish` ends simulation and `$stop` requests a simulation stop, whose interactive behavior depends on the tool. Waveform dumping commonly uses `$dumpfile` and `$dumpvars` in tools supporting VCD output. Use the selected simulator's manual for nonstandard names and extensions; do not assume every `$` example on a slide is portable.

Your final handwritten definition of **functional verification using simulation** says that a testbench applies stimuli and checks responses against expected behavior. That introductory definition connects to [Day 08](Day%2008.md). The separate course lesson titled *Functional Verification Using Simulation* is your current lesson and remains the next chapter, outside this completed batch.

The [Verilog example folder](examples/verilog/README.md) contains the complete modules and a check script. It checks arithmetic widths, four-state matching, edge-event behavior, parameter overrides, pipeline state, and the timed blocking/nonblocking example. The examples support these explanations; they do not claim exhaustive verification of a production design.

[Previous: Day 11](Day%2011.md)
