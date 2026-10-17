# Revision

[Master index](../README.md) · [Assignments](../Assignments/README.md) · [Full reading PDFs](../PDFs/README.md)

**Weeks 1 to 3 are ready.** Later weeks will be added when requested; the completed 12-week lecture notes remain in the full reading collection. Use **Download PDF** to save a revision guide; the local app is for assignment practice.

| Week | Revision | Download | Pages |
|---|---|---|---:|
| 01 | [IC foundations and pre-RTL methods](Week%2001%20-%20Revision.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Revision/Week%2001%20-%20Revision.pdf) | 8 |
| 02 | [Implementation, verification, manufacturing and Tcl](Week%2002%20-%20Revision.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Revision/Week%2002%20-%20Revision.pdf) | 13 |
| 03 | [Verilog, simulation, coverage and Bambu HLS](Week%2003%20-%20Revision.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Revision/Week%2003%20-%20Revision.pdf) | 16 |

**Week 1** covers IC structure and fabrication, design styles, economics, PPA, abstraction, hardware-software partitioning, SoC/IP reuse and Unix. Behavioural synthesis receives a detailed treatment of scheduling, allocation, binding, control, interfaces, resource sharing, advantages and limitations. Worked examples distinguish latency, initiation interval, throughput and clock-period budgets.

**Week 2** combines Kapil's new points with the remaining course material: synthesis inputs and mapping; cell/instance/pin/port/net terminology; floorplanning, PDN, placement, CTS and routing; verification methods and DRC/LVS/ERC; test activation and observability; yield, fault coverage and escaping bad chips; masks, OPC, multiple patterning, packaging and binning; and Tcl substitutions, lists, control flow and files. Nine typed revision pages are followed by four pages reproducing the Week 2 handwriting. Worked checks clarify utilization, IR drop, clock skew, setup timing, the yield model and the 100-chip escape example.

**Week 3** covers Verilog types and four-state values; literal widths and signedness; operators, equality and wildcard cases; hierarchy, parameters and traditional functions/tasks; processes, edge events and time precision; blocking/nonblocking assignments and delayed sampling; event queues and races; testbenches, VCD and coverage; and the Bambu HLS tutorial. Ten typed pages with worked traces are followed by six complete original handwritten pages. The accompanying verifier runs 38 Verilog semantic checks plus the queue, clock and precision examples with the installed Icarus simulator; it does not claim a Bambu synthesis run.

Week 1 is four lectures plus Tutorial 1. The existing Day 01 reading PDF also includes the first Week 2 lecture; this revision uses the course-week boundary. Original handwriting and full lecture figures remain in the [Day 01 reading edition](../PDFs/Day%2001%20-%20IC%20Foundations%20and%20Logic%20Synthesis.pdf).

Week 2 follows course Lessons 06-09 plus the Tcl tutorial, Lesson 10. Its full lecture explanations are split between the [Day 01 reading edition](../PDFs/Day%2001%20-%20IC%20Foundations%20and%20Logic%20Synthesis.pdf) and [Day 02 reading edition](../PDFs/Day%2002%20-%20Physical%20Design%20and%20Verilog%20Foundations.pdf). The [complete new handwritten upload](../Resources/weekly/Week%2002/handwritten/Fsm.pdf) is preserved under Resources, including the earlier FSM exercises outside Week 2.

Week 3 follows Lessons 11-14, split between the [Day 02 reading edition](../PDFs/Day%2002%20-%20Physical%20Design%20and%20Verilog%20Foundations.pdf) and [Day 03 reading edition](../PDFs/Day%2003%20-%20Simulation%20Synthesis%20and%20Logic%20Optimization.pdf). Its appendix retains Part 2 original pages 2-4 and Scan A pages 1-3; the first also contains earlier Week 2 notes. Later Day 03 synthesis and optimization lessons belong to Week 4.

Editable sources for [Week 1](../Resources/weekly/Week%2001/revision.md), [Week 2](../Resources/weekly/Week%2002/revision.md) and [Week 3](../Resources/weekly/Week%2003/revision.md), together with the [source guide](../Resources/weekly/README.md), retain the references. The practice bank is syllabus-based preparation, not a claimed list of verified past exam questions.
