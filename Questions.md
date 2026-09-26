# Questions and corrections

[Course index](README.md) · [Handwritten page index](Handwritten%20Index.md)

This index includes explicit handwritten questions and questions implied by incomplete formulas, comparison tables, and shorthand. Wording is normalized for readability; it is not presented as a verbatim transcription of every mark. Full explanations and nearby source images are in the linked chapters.

| Question or point to clarify | Handwritten location | Answer in brief | Read more |
|---|---|---|---|
| What is a mask? | Part 1, page 1 | A patterned exposure template; distinguish wafer lithography from making the mask itself. | [Explanation](Day%2001.md#your-handwritten-question-what-is-a-mask) |
| How can we make good or defect-free dies? | Part 1, page 2 | Control design/process defects, use physical checks and testing, and quantify yield; no process promises perfect yield. | [Explanation](Day%2001.md#your-handwritten-question-how-can-we-make-good-or-defect-free-dies) |
| How does an FPGA differ from cell-based design? | Part 1, page 5 | A fabricated programmable fabric versus mapping, placing, and fabricating a custom standard-cell implementation. | [Explanation](Day%2002.md#your-question-fpga-versus-cell-based-design) |
| Which implementation should we choose? | Part 1, page 6 | Use feasibility, schedule, flexibility, volume, and total cost; the chapter calculates a break-even volume. | [Explanation](Day%2002.md#your-question-what-should-we-choose) |
| Can faster hardware give unlimited system speedup? | Part 1, pages 9–10, partition notes | The unaccelerated portion and communication overhead limit the result; worked Amdahl calculation. | [Explanation](Day%2003.md#hardware-and-software-partitioning) |
| How do arrival time and required time relate? | Part 1, page 13, incomplete expressions | Setup and hold have different inequalities; the chapter defines each delay and clock-skew convention. | [Explanation](Day%2004.md#paths-and-the-clock-period-budget) |
| How does one adder compute a+b+c? | Part 1, page 14 | Store an intermediate sum, select feedback operands, and sequence two additions with control. | [Explanation](Day%2004.md#three-implementations-of-a-plus-b-plus-c) |
| What is a library pin versus an instance pin? | Part 1, page 15 | A pin in the reusable cell definition versus that pin on a particular placed/logical instance, such as I1/A. | [Explanation](Day%2006.md#library-pins-and-instance-pins) |
| Is there a defined universal set of generic gates? | Part 1, page 16 | No universal fixed synthesis IR vocabulary; tools use their own generic cells and operators before library mapping. | [Explanation](Day%2006.md#generic-logic-and-technology-mapping) |
| Does floorplanning decide every cell location? | Part 1, pages 17–18 | It sets regions, macros, constraints, and infrastructure; placement determines standard-cell locations. | [Explanation](Day%2007.md#floorplanning-power-and-placement) |
| Do DRC and LVS prove correct functionality? | Part 1, page 21 | They check physical rules and extracted connectivity; they do not prove the intended algorithm. | [Explanation](Day%2008.md#timing-and-physical-verification) |
| What are the parentheses in the yield model? | Part 1, page 23 | The negative-binomial form is (1+AD/alpha)^(-alpha), with compatible area and defect-density units. | [Explanation](Day%2008.md#yield-fault-coverage-and-escapes) |
| Does 50% fault coverage mean half the defective chips escape? | Part 1, page 23, numerical example | Only under an extra simplifying assumption; modeled-fault coverage and defective-chip detection are different measures. | [Explanation](Day%2008.md#yield-fault-coverage-and-escapes) |
| Why does a mask need OPC? | Part 2, page 1 | Pre-distort the mask so the printed feature approaches the desired shape despite imaging/process effects. | [Explanation](Day%2009.md) |
| Are square brackets always evaluated first in Tcl? | Part 2, page 2 | They perform command substitution when substitution is enabled; a braced literal can suppress it. | [Explanation](Day%2010.md#commands-variables-and-substitution) |
| What is the difference between z and question mark? | Part 2, page 3; Part 1, page 21 margin | A question mark in a based literal encodes z; wildcard behavior comes from casez/casex, not the character alone. | [Explanation](Day%2011.md#your-questions-what-is-the-difference-between-z-and-question-mark) |
| Why prefer question marks in a wildcard pattern? | Part 2, page 3 | They communicate ignored bit positions; exact case still treats those encoded z bits as values. | [Explanation](Day%2011.md#your-questions-what-is-the-difference-between-z-and-question-mark) |
| Does reg always mean a hardware register? | Part 2, page 3 | No; reg is a procedural variable type, and the process determines whether storage is inferred. | [Explanation](Day%2011.md#nets-variables-vectors-arrays-and-strings) |
| What happens when a literal is too wide or negative? | Part 2, page 3 | Size fixes retained bits; signedness interprets them; negative values use two’s complement at the chosen width. | [Explanation](Day%2011.md#sized-literals-padding-truncation-and-signed-values) |
| Can parameters change during execution? | Part 2, page 3 | They select constants during elaboration; a signal input is needed for runtime control. | [Explanation](Day%2012.md#modules-ports-hierarchy-and-parameters) |
| Which x/z transitions count as edges? | Part 2, page 3 | The chapter lists all single-bit posedge/negedge transitions and verifies a deliberate sequence. | [Explanation](Day%2012.md#processes-event-controls-and-four-state-edges) |
| Do tasks always take time and functions mean combinational hardware? | Part 2, page 4 | Tasks may suspend but need not; hardware interpretation depends on body and use. | [Explanation](Day%2012.md#functions-and-tasks) |
| When is the left-hand side of a nonblocking assignment updated? | Part 2, page 4 | At its scheduled NBA update; without a delay, within the current time slot, not at the end of the whole simulation. | [Explanation](Day%2012.md#continuous-blocking-and-nonblocking-assignment) |
