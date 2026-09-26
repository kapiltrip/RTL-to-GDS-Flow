# Day 11 — Hardware Modeling — Introduction to Verilog I

[Course index](README.md) · Week 3 · [Lecture video](https://www.youtube.com/watch?v=LOIqVrr9jGE) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [What a hardware description language must represent](#what-a-hardware-description-language-must-represent)
- [Lexical rules and four-state values](#lexical-rules-and-four-state-values)
- [Sized literals padding truncation and signed values](#sized-literals-padding-truncation-and-signed-values)
- [Nets variables vectors arrays and strings](#nets-variables-vectors-arrays-and-strings)
- [Recall checks](#recall-checks)

## What a hardware description language must represent

![Bit-accurate values and resolved drivers are distinctive HDL features](images/Day%2011/01-hdl.png)

*Video frame: [9:14](https://www.youtube.com/watch?v=LOIqVrr9jGE&t=554s). Bit-accurate values and resolved drivers are distinctive HDL features*


An **HDL (hardware description language)** describes the behavior and structure of electronic hardware. Verilog lets us express modules, wires, stored state, and the changes that occur when inputs or clocks change. A simulator interprets these descriptions to predict modeled behavior; a synthesis tool interprets a supported subset to construct a circuit. These are different uses of the same source text, so a statement that simulates successfully is not automatically synthesizable.

Hardware needs **concurrency**: two adders can respond to their inputs at the same time. It needs **time**: a register reacts to a clock event, and physical gates have propagation delay. It needs **multiple-driver resolution**: two connected outputs might agree, conflict, or release a line. It needs **bit-accurate modeling**: an eight-bit result cannot retain a ninth carry bit unless the description provides a place for it. A general software integer alone does not express all these properties.

RTL describes state held in registers and the combinational transformations between them. It does not give every transistor's physical layout. Synthesis and physical design progressively supply those details. A delay written as `#10` in a testbench advances simulated time; it does not order the ASIC tool to manufacture a gate with exactly that delay.

![Kapil’s handwritten notes — Part 2, PDF page 2, lower HDL section](images/Day%2011/h01-hdl.jpg)

*Handwritten source: Part 2, PDF page 2, lower HDL section.*


Your examples of multiple drivers and bit-true behavior are the key motivations for an HDL. Distinguish **parallel hardware** from the order of statements inside one process: different `always` blocks are concurrent, while statements within a `begin ... end` block execute in their language-defined order. That order alone does not say how many clock cycles the resulting hardware needs.

Verilog and SystemVerilog are related languages. This pair of lessons uses traditional Verilog terminology such as `wire` and `reg`. Keep those meanings clear before introducing SystemVerilog's additional types and verification features. An IEEE revision date is a language-standard milestone, not the birth date of every feature mentioned alongside it.

## Lexical rules and four-state values

Verilog is **case-sensitive**: `data`, `Data`, and `DATA` are different identifiers. Keywords such as `module` and `always` are lowercase. A simple identifier begins with a letter or underscore and can subsequently contain letters, digits, underscores, and dollar signs. An escaped identifier starts with a backslash and ends at whitespace; it is useful for generated names but makes hand-written RTL harder to read. Use descriptive simple names where possible. `//` introduces a line comment; `/* ... */` encloses a block comment.

The four logic states are:

| State | Meaning in simulation | Typical reason |
|---|---|---|
| `0` | Known logic low | A driver produces zero |
| `1` | Known logic high | A driver produces one |
| `x` | Unknown value | Uninitialized storage, conflicting drivers, or an operation with insufficiently known inputs |
| `z` | High impedance | A driver has released a net, or a net has no active driver |

`x` does not mean that a physical circuit has a stable third digital voltage. It records uncertainty in the model. A real uninitialized flip-flop may settle to either zero or one; simulation uses `x` because the description does not establish which. Similarly, `z` describes the absence of an active drive, not a guaranteed measured voltage. Pull devices, capacitance, leakage, and other connected drivers determine what an actual released node does.

With ordinary equal-strength drivers, `0` against `1` resolves to `x`; an active `1` against a released `z` resolves to `1`. Drive strengths permit more detailed resolution, so the “conflicting drivers give `x`” rule assumes neither driver dominates. In ordinary RTL, avoid multiple procedural drivers for the same state variable.

### Why an unknown input does not always make the output unknown

For a one-bit Boolean operation, ask whether both possible known values of an unknown input give the same result. If they do, that result is already determined:

| Verilog expression | Result | Reason |
|---|---|---|
| `1'b0 & 1'bx` | `1'b0` | Zero AND either zero or one is zero |
| `1'b1 & 1'bx` | `1'bx` | The result depends on the unknown input |
| `1'b1 \| 1'bx` | `1'b1` | One OR either zero or one is one |
| `1'b0 \| 1'bx` | `1'bx` | The result depends on the unknown input |
| `1'bx ^ 1'bx` | `1'bx` | The simulator does not establish a known Boolean relationship between the operands |

Zero is the **controlling value** for AND; one is the controlling value for OR. A controlling value determines the output regardless of the other input. For these bitwise operators, `z` is also treated as an unknown operand, so `1'b0 & 1'bz` produces zero. This differs from **net resolution**, where an active driver can determine the value of a net whose other driver is released.

The last row shows a limit of four-state simulation: an unknown value is not a symbolic variable whose relationships are tracked algebraically. Even `a ^ a` can evaluate to `x` when `a` contains `x`, although the corresponding ideal Boolean identity is zero. Therefore an `x` waveform asks you to inspect initialization, drivers, and operator semantics. It is not an instruction to treat that bit as a freely chosen don't-care.

## Sized literals padding truncation and signed values

![Sized constants retain the declared number of bits](images/Day%2011/02-literals.png)

*Video frame: [33:10](https://www.youtube.com/watch?v=LOIqVrr9jGE&t=1990s). Sized constants retain the declared number of bits*


A based integer literal has the form **size, apostrophe, optional signed marker, base, digits**, for example `8'hA1` or `8'shFA`. The size is a number of **bits**, independent of the chosen base. Binary uses one bit per digit, octal three, and hexadecimal four. Underscores improve readability without changing the value.

| Literal or assignment | Stored bit pattern | Reason |
|---|---|---|
| `1'b1` | `1` | One binary bit |
| `8'hA1` | `10100001` | Two hexadecimal digits in eight bits |
| `6'o71` | `111001` | Two octal digits in six bits |
| `6'h88` | `001000` | `10001000` loses its two most significant bits |
| `8'b11` | `00000011` | Ordinary positive digits are padded on the left with zeros |
| `8'bz1` | `zzzzzzz1` | A leading high-impedance digit extends the unspecified upper positions |
| `8'bx01` | `xxxxxx01` | A leading unknown digit similarly extends with `x` |
| Eight-bit assignment of `-6` | `11111010` | Two's-complement encoding modulo 256 |

For the last row, start with six as `00000110`, invert to `11111001`, then add one to obtain `11111010`. The **same bits** represent unsigned 250 or signed −6 depending on the declared type and expression context. A minus sign is a unary operator, not an extra digit inside a based literal. Writing `8'sd6` gives a signed positive six; `-8'sd6` negates it.

Expression width matters before assignment. An eight-bit destination cannot recover information that was already discarded by a narrower intermediate operation. To calculate an unsigned eight-bit addition with its carry, explicitly widen both operands: `{1'b0, a} + {1'b0, b}` into a nine-bit destination. Unsized decimal constants are signed and at least 32 bits; mixing them with unsigned vectors can change extension and interpretation. Explicit widths and explicit intent make a design easier to review.

![Kapil’s handwritten notes — Part 2, PDF page 3, complete values and data-types page](images/Day%2011/h02-types.jpg)

*Handwritten source: Part 2, PDF page 3, complete values and data-types page.*


Your worked truncation example is a **least-significant-bit retention** operation. A declared width is not a request to round a number. Your negative-number example uses two's complement correctly once the width is fixed; do not attach a unique decimal meaning to a bit string without also specifying signedness.

### Your questions: what is the difference between z and question mark?

Inside a Verilog **based number literal**, `?` is an alternative spelling of `z`. Thus `4'b10?1` and `4'b10z1` encode the same four-state value. `?` is not a fifth logic state and is not automatically a wildcard everywhere. Separately, the punctuation in `condition ? true_value : false_value` belongs to the conditional operator.

Your note “prefer `?` when high impedance is don't care” concerns readability in wildcard **case patterns**. A pattern such as `3'b1??` visually communicates ignored positions, while `3'b1zz` can look like an intentional electrical high-impedance value. The surrounding construct supplies the wildcard behavior:

| Construct | Matching rule |
|---|---|
| `case` | Exact four-state matching, including `x` and `z` |
| `casez` | `z`/`?` positions in either selector or item are ignored |
| `casex` | `x`, `z`, and `?` positions in either selector or item are ignored |

This rule also affects the **selector**, which is easy to overlook: an unintended `z` in a selector can make `casez` match more broadly than expected. `casex` can hide uninitialized `x` values in control logic. Use intentional patterns and a defined default; do not use wildcard matching to conceal an unknown state. The author's [Verilog-2001 reference, decision statements](https://sutherland-hdl.com/pdfs/verilog_2001_ref_guide.pdf#page=29) confirms these matching rules.

For equality, `==` can return `x` when unknown or high-impedance bits make the comparison indeterminate. Case equality `===` compares all four states and produces a known Boolean result; it is especially useful in testbenches. It does not magically make an unknown physical signal safe. For example, `1'bx == 1'bx` gives `x`, while `1'bx === 1'bx` gives `1`.

## Nets variables vectors arrays and strings

![Net and variable types serve different modeling roles](images/Day%2011/03-types.png)

*Video frame: [42:14](https://www.youtube.com/watch?v=LOIqVrr9jGE&t=2534s). Net and variable types serve different modeling roles*


A **net** models a connection and takes its value from its drivers. `wire` is the common net type. An undriven ordinary wire reads `z`. Other net types express special resolution or supply behavior: `wand` models wired-AND resolution, `wor` wired-OR resolution, and `supply0`/`supply1` constant supplies. These modeling facilities do not imply that arbitrary internal tri-state or wired logic is supported by every synthesis target.

A **variable** stores its most recently assigned simulation value until another procedural assignment updates it. Traditional Verilog's `reg` is a four-state variable type. Its name does **not** guarantee a hardware register. `reg` assigned in a complete combinational process can represent combinational logic; assigned only on a clock edge, it can describe flip-flop state. An incomplete combinational assignment can infer a latch. The surrounding process determines the inferred storage.

This complete module deliberately uses both forms of combinational description:

```verilog
module mux_forms (
    input  wire       sel,
    input  wire [7:0] a, b,
    output wire [7:0] y_wire,
    output reg  [7:0] y_reg
);
    assign y_wire = sel ? b : a;
    always @* begin
        if (sel) y_reg = b;
        else     y_reg = a;
    end
endmodule
```

For known `sel`, the two outputs agree and describe multiplexers, without a clock or a hardware register. With `sel=x`, the conditional operator can merge equal bits from its alternatives, while procedural `if` takes its else branch when the condition is not true. That is a simulation distinction worth understanding; ordinary operation should provide a known control signal. [Day 12](Day%2012.md#operators-and-bit-level-examples) works through the conditional operator.

`wire [7:0] bus` declares one eight-bit **vector**; `bus[3]` selects a bit and `bus[7:4]` selects four bits. `reg [7:0] memory [0:15]` declares an **array** containing sixteen eight-bit words; `memory[2]` selects a word. A range before a name describes the vector bits, while the array dimension follows the name in this traditional syntax. `[0:7]` is also legal but reverses the index direction; use a consistent convention and never assume that index zero is always the least significant bit.

Traditional types also include `integer` for a signed 32-bit variable, `time` for a 64-bit unsigned time value, and `real` for floating-point simulation values. Declaring `real` does not synthesize a floating-point arithmetic unit. For actual floating-point hardware, you need a suitable synthesizable architecture or IP and an explicit representation.

A traditional Verilog string literal packs character codes, eight bits per character, into a vector context. `reg [39:0] text;` can hold five characters such as `"HELLO"`. A destination that is too small truncates the most significant portion, so choose the width deliberately. Strings used for `$display` messages are testbench text, not automatically a hardware text-storage subsystem.

The runnable [language examples](examples/verilog/README.md) exercise these values and distinguish variable type from inferred storage. Your parameter and edge-event notes at the right of the handwritten page continue in [Day 12](Day%2012.md).

## Recall checks

1. Why can an undriven wire read `z` while an uninitialized `reg` reads `x`? A net reports its resolved drive; an uninitialized variable has no known stored value.
2. Does `6'h88` equal hexadecimal 88? No: six bits retain only `001000`, decimal eight.
3. Does `reg` imply a flip-flop? No: a clocked assignment can infer a flip-flop; a complete combinational process need not infer storage.
4. Is `?` always a don't-care? No: in a based literal it encodes `z`; wildcard case matching gives that position its don't-care interpretation.
5. Why provide a ninth bit for adding two eight-bit unsigned inputs? The maximum sum is 510, which needs nine bits.

[Previous: Day 10](Day%2010.md) · [Next: Day 12](Day%2012.md)
