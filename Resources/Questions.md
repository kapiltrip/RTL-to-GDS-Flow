# Questions and corrections

[Course index](../README.md) · [Handwritten page index](Handwritten%20Index.md)

This index includes explicit handwritten questions and questions implied by incomplete formulas, comparison tables, and shorthand. Wording is normalized for readability; it is not presented as a verbatim transcription of every mark. Full explanations and nearby source images are in the linked chapters.

| Question or point to clarify | Handwritten location | Answer in brief | Read more |
|---|---|---|---|
| What is a mask? | Part 1, page 1 | A patterned exposure template; distinguish wafer lithography from making the mask itself. | [Explanation](../Daily%20Notes/Day%2001.md#what-is-a-mask) |
| How can we make good or defect-free dies? | Part 1, page 2 | Control design/process defects, use physical checks and testing, and quantify yield; no process promises perfect yield. | [Explanation](../Daily%20Notes/Day%2001.md#how-can-we-make-good-or-defect-free-dies) |
| How does an FPGA differ from cell-based design? | Part 1, page 5 | A fabricated programmable fabric versus mapping, placing, and fabricating a custom standard-cell implementation. | [Explanation](../Daily%20Notes/Day%2001.md#fpga-versus-cell-based-design) |
| Which implementation should we choose? | Part 1, page 6 | Use feasibility, schedule, flexibility, volume, and total cost; the chapter calculates a break-even volume. | [Explanation](../Daily%20Notes/Day%2001.md#what-should-we-choose) |
| Can faster hardware give unlimited system speedup? | Part 1, pages 9–10, partition notes | The unaccelerated portion and communication overhead limit the result; worked Amdahl calculation. | [Explanation](../Daily%20Notes/Day%2001.md#hardware-and-software-partitioning) |
| How do arrival time and required time relate? | Part 1, page 13, incomplete expressions | Setup and hold have different inequalities; the chapter defines each delay and clock-skew convention. | [Explanation](../Daily%20Notes/Day%2001.md#paths-and-the-clock-period-budget) |
| How does one adder compute a+b+c? | Part 1, page 14 | Store an intermediate sum, select feedback operands, and sequence two additions with control. | [Explanation](../Daily%20Notes/Day%2001.md#three-implementations-of-a-plus-b-plus-c) |
| What is a library pin versus an instance pin? | Part 1, page 15 | A pin in the reusable cell definition versus that pin on a particular placed/logical instance, such as I1/A. | [Explanation](../Daily%20Notes/Day%2001.md#library-pins-and-instance-pins) |
| Is there a defined universal set of generic gates? | Part 1, page 16 | No universal fixed synthesis IR vocabulary; tools use their own generic cells and operators before library mapping. | [Explanation](../Daily%20Notes/Day%2001.md#generic-logic-and-technology-mapping) |
| Does floorplanning decide every cell location? | Part 1, pages 17–18 | It sets regions, macros, constraints, and infrastructure; placement determines standard-cell locations. | [Explanation](../Daily%20Notes/Day%2002.md#floorplanning-power-and-placement) |
| Do DRC and LVS prove correct functionality? | Part 1, page 21 | They check physical rules and extracted connectivity; they do not prove the intended algorithm. | [Explanation](../Daily%20Notes/Day%2002.md#timing-and-physical-verification) |
| What are the parentheses in the yield model? | Part 1, page 23 | The negative-binomial form is (1+AD/alpha)^(-alpha), with compatible area and defect-density units. | [Explanation](../Daily%20Notes/Day%2002.md#yield-fault-coverage-and-escapes) |
| Does 50% fault coverage mean half the defective chips escape? | Part 1, page 23, numerical example | Only under an extra simplifying assumption; modeled-fault coverage and defective-chip detection are different measures. | [Explanation](../Daily%20Notes/Day%2002.md#yield-fault-coverage-and-escapes) |
| Why does a mask need OPC? | Part 2, page 1 | Pre-distort the mask so the printed feature approaches the desired shape despite imaging/process effects. | [Explanation](../Daily%20Notes/Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |
| Are square brackets always evaluated first in Tcl? | Part 2, page 2 | They perform command substitution when substitution is enabled; a braced literal can suppress it. | [Explanation](../Daily%20Notes/Day%2002.md#commands-variables-and-substitution) |
| What is the difference between z and question mark? | Part 2, page 3; Part 1, page 21 margin | A question mark in a based literal encodes z; wildcard behavior comes from casez/casex, not the character alone. | [Explanation](../Daily%20Notes/Day%2002.md#what-is-the-difference-between-z-and-question-mark) |
| Why prefer question marks in a wildcard pattern? | Part 2, page 3 | They communicate ignored bit positions; exact case still treats those encoded z bits as values. | [Explanation](../Daily%20Notes/Day%2002.md#what-is-the-difference-between-z-and-question-mark) |
| Does reg always mean a hardware register? | Part 2, page 3 | No; reg is a procedural variable type, and the process determines whether storage is inferred. | [Explanation](../Daily%20Notes/Day%2002.md#nets-variables-vectors-arrays-and-strings) |
| What happens when a literal is too wide or negative? | Part 2, page 3 | Size fixes retained bits; signedness interprets them; negative values use two’s complement at the chosen width. | [Explanation](../Daily%20Notes/Day%2002.md#sized-literals-padding-truncation-and-signed-values) |
| Can parameters change during execution? | Part 2, page 3 | They select constants during elaboration; a signal input is needed for runtime control. | [Explanation](../Daily%20Notes/Day%2002.md#modules-ports-hierarchy-and-parameters) |
| Which x/z transitions count as edges? | Part 2, page 3 | The chapter lists all single-bit posedge/negedge transitions and verifies a deliberate sequence. | [Explanation](../Daily%20Notes/Day%2002.md#processes-event-controls-and-four-state-edges) |
| Do tasks always take time and functions mean combinational hardware? | Part 2, page 4 | Tasks may suspend but need not; hardware interpretation depends on body and use. | [Explanation](../Daily%20Notes/Day%2002.md#functions-and-tasks) |
| When is the left-hand side of a nonblocking assignment updated? | Part 2, page 4 | At its scheduled NBA update; without a delay, within the current time slot, not at the end of the whole simulation. | [Explanation](../Daily%20Notes/Day%2002.md#continuous-blocking-and-nonblocking-assignment) |

## September 30 clarifications
Each item is explained alongside the original page. These corrections preserve the handwriting and make the assumptions explicit.
| Page | Clarification | Deep explanation |
|---|---|---|
| A-03 | Display sees the active value; strobe sees the settled value. The classic queue is not the full SystemVerilog model. | [Lesson 13](../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| A-05 | Elaborated ports retain declared directions; parameter overrides create configured instances. | [Lesson 15](../Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| A-06 | Plain case does not treat ? as a 0/1 wildcard; casez does, with first-match priority. | [Lesson 15](../Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| A-08 | ! is logical negation; ~ is bitwise complement. | [Lesson 16](../Daily%20Notes/Day%2003.md#lesson-16-rtl-synthesis---part-ii) |
| A-10 | Common-expression reuse differs from constant propagation; signed division is not always an arithmetic shift. | [Lesson 16](../Daily%20Notes/Day%2003.md#lesson-16-rtl-synthesis---part-ii) |
| A-11 | Minterm is a product; maxterm is a sum. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| A-13 | For AB+ABC+BC, both primes AB and BC are essential. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| A-14 | The official lecture slide restores the partial chart: two essential primes plus either of two selective primes give minimum three-term covers. Heuristic expand/reduce/reshape/irredundant steps do not guarantee that minimum. | [Worked chart](../Daily%20Notes/Day%2003.md#a-14-coverage-charts-minimal-covers-and-minimum-cost) |
| A-15 | The alternative factored expression has seven literal occurrences; preserve the q complement in the source network. | [Lesson 19](../Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii) |
| A-17 | Equal current output alone does not establish state equivalence; one million vectors/s does not exhaust 64 inputs in zero seconds. | [Lesson 20](../Daily%20Notes/Day%2004.md#lesson-20-logic-optimization---part-iii) |
| A-17 margin | Cube graphs represent assignments; network graphs represent dependencies. The two's-complement lower bound is -2^(n-1), without an extra -1. Follow the first simulation mismatch or a formal counterexample to diagnose an error. | [Cube question](../Daily%20Notes/Day%2004.md#a-17-upper-section-controllability-and-observability-dont-cares) · [Integer/error questions](../Daily%20Notes/Day%2004.md#margin-notes-signed-integers-and-finding-errors) |
| A-18 | Formal completeness depends on model, property, assumptions and proof method. | [Lesson 21](../Daily%20Notes/Day%2004.md#lesson-21-formal-verification---i) |
| A-20 | A variable order plus both reduction rules is required for an ROBDD. | [Lesson 21](../Daily%20Notes/Day%2004.md#lesson-21-formal-verification---i) |
| A-21 | ROBDD size can be exponential; the course defines k-SAT with at most k literals per clause. | [Lesson 23](../Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| A-21 witnesses | The written 001 and 101 assignments satisfy the SOP through x2'x3. CNF instead needs every clause true; a forced contradiction proves UNSAT while one failed decision branch does not. | [SAT and UNSAT examples](../Daily%20Notes/Day%2004.md#a-21-sat-unsat-cnf-and-robdd-scope) |
| B-01 | Cell setup time comes from the library model; the period changes the available deadline. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| B-02 | Arrival 26 versus required 20 is setup slack -6, a violation. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| B-03 | A 16 ns minimum period gives 62.5 MHz; hold slack reverses the setup subtraction. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| B-04 | With skew C-L, capture latency helps setup and hurts hold. Derive from absolute edge arrivals. | [Lesson 29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| B-05/B-06 | Largest arrival and largest slew can come from different paths; their combination can be pessimistic. | [Lesson 29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| B-07/B-08 | Corners, mode coverage and early/late OCV choices are distinct; do not remove margins merely to pass. | [Lesson 30](../Daily%20Notes/Day%2005.md#lesson-30-static-timing-analysis---iii) |
| B-10 | create_clock models timing; it does not build a clock generator. Verify units and supported command spellings. | [Lesson 32](../Daily%20Notes/Day%2006.md#lesson-32-constraints-i) |
| B-11 | Positive uncertainty tightens setup and hold, using opposite inequality directions. | [Lesson 32](../Daily%20Notes/Day%2006.md#lesson-32-constraints-i) |

The September 30 8:18:09 PM upload contains zero bytes. It cannot be reviewed or reconstructed. Other unlabeled K-map sketches remain explicitly qualified rather than assigned invented function definitions.
