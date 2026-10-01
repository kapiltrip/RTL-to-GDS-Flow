# Full forms and meanings

[Master index](../README.md)

Each meaning links to a deeper explanation. Boolean plus/product notation is separate from arithmetic operators; the two SDC meanings are deliberately listed separately.

| Term | Full form or expansion | Meaning | Deep explanation |
|---|---|---|---|
| RTL | Register Transfer Level | Describes transfers and transformations between state elements. | [Lesson 15](../Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| GDSII | Graphic Data System II | Layout exchange format used for geometric mask data. | [Lesson 09](../Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |
| IC | Integrated Circuit | Devices and interconnect integrated on a substrate. | [Lesson 01](../Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| VLSI | Very Large Scale Integration | Integration scale motivating a staged design flow. | [Lesson 03](../Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) |
| ASIC | Application-Specific Integrated Circuit | A chip designed for a particular application. | [Lesson 02](../Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| FPGA | Field-Programmable Gate Array | Configurable logic and routing programmed after manufacture. | [Lesson 02](../Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| PDK | Process Design Kit | Process models, layers and design rules. | [Lesson 01](../Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| IP | Intellectual Property | Reusable design block and supporting integration information. | [Lesson 04](../Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) |
| HLS | High-Level Synthesis | Schedules and binds behavioral operations into hardware. | [Lesson 14](../Day%2003.md#lesson-14-high-level-synthesis-using-bambu---tutorial-3) |
| EDA | Electronic Design Automation | Tools for design, implementation and verification. | [Lesson 05](../Day%2001.md#lesson-05-tutorial-1--unix-foundations-for-eda) |
| Tcl | Tool Command Language | Command language used by many EDA interfaces. | [Lesson 10](../Day%2002.md#lesson-10-introduction-to-tcl) |
| HDL | Hardware Description Language | Models concurrent hardware behavior and structure. | [Lesson 11](../Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) |
| DUT | Design Under Test | Implementation exercised by a verification environment. | [Lesson 13](../Day%2003.md#lesson-13-functional-verification-using-simulation) |
| TB | Testbench | Stimulus, checking and supporting simulation logic. | [Lesson 13](../Day%2003.md#lesson-13-functional-verification-using-simulation) |
| VCD | Value Change Dump | Timestamped signal changes for waveform inspection. | [Lesson 13](../Day%2003.md#lesson-13-functional-verification-using-simulation) |
| NBA | Nonblocking Assignment | Schedules a later left-side update after evaluating the right side. | [Lesson 13](../Day%2003.md#lesson-13-functional-verification-using-simulation) |
| AST | Abstract Syntax Tree | Hierarchical representation of parsed source syntax. | [Lesson 15](../Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| FSM | Finite State Machine | State, transition and output model for sequential behavior. | [Lesson 20](../Day%2004.md#lesson-20-logic-optimization---part-iii) |
| SOP | Sum of Products | OR of AND terms in Boolean notation. | [Lesson 17](../Day%2003.md#lesson-17-logic-optimization---part-i) |
| POS | Product of Sums | AND of OR terms in Boolean notation. | [Lesson 17](../Day%2003.md#lesson-17-logic-optimization---part-i) |
| PI | Prime Implicant | A legal product cube that cannot be further expanded. | [Lesson 17](../Day%2003.md#lesson-17-logic-optimization---part-i) |
| EPI | Essential Prime Implicant | Prime covering a required minterm uniquely among primes. | [Lesson 17](../Day%2003.md#lesson-17-logic-optimization---part-i) |
| RPI | Redundant Prime Implicant | In the essentials-first classification, a nonessential prime whose ON points are already covered by selected essentials. | [A-13 cover selection](../Day%2003.md#a-13-the-prime-implicants-of-ab--abc--bc) |
| SPI | Selective Prime Implicant | Remaining nonessential prime that can cover a still-uncovered ON point; select a sufficient residual cover. | [A-14 worked chart](../Day%2003.md#a-14-coverage-charts-minimal-covers-and-minimum-cost) |
| DC | Dont-Care | Behavior permitted to vary under justified specification conditions. | [Lesson 17](../Day%2003.md#lesson-17-logic-optimization---part-i) |
| CDC | Controllability Dont-Care | Impossible internal input combination caused by network dependencies. | [Lesson 19](../Day%2004.md#lesson-19-logic-optimization---part-ii) |
| ODC | Observability Dont-Care | Internal variation masked at all relevant observed outputs. | [Lesson 19](../Day%2004.md#lesson-19-logic-optimization---part-ii) |
| SDC (logic) | Satisfiability Dont-Care | Impossible relation between local inputs and their computed output. | [Lesson 19](../Day%2004.md#lesson-19-logic-optimization---part-ii) |
| BDD | Binary Decision Diagram | Graph representing recursive Boolean decisions. | [Lesson 21](../Day%2004.md#lesson-21-formal-verification---i) |
| ROBDD | Reduced Ordered Binary Decision Diagram | Canonical for one fixed variable order, with reduction rules applied. | [Lesson 21](../Day%2004.md#lesson-21-formal-verification---i) |
| SAT | Boolean Satisfiability | Existence of an assignment satisfying a Boolean formula. | [Lesson 23](../Day%2004.md#lesson-23-formal-verification---ii) |
| UNSAT | Unsatisfiable | No satisfying assignment under the encoded conditions. | [Lesson 23](../Day%2004.md#lesson-23-formal-verification---ii) |
| CNF | Conjunctive Normal Form | AND of clauses, each an OR of literals. | [Lesson 23](../Day%2004.md#lesson-23-formal-verification---ii) |
| BCP | Boolean Constraint Propagation | Repeated deduction from unit clauses. | [Lesson 23](../Day%2004.md#lesson-23-formal-verification---ii) |
| DPLL | Davis–Putnam–Logemann–Loveland | SAT search through decisions, implications and backtracking. | [Lesson 23](../Day%2004.md#lesson-23-formal-verification---ii) |
| BMC | Bounded Model Checking | Checks unfolded behavior through a specified cycle bound. | [Lesson 24](../Day%2004.md#lesson-24-formal-verification---iii) |
| CEC | Combinational Equivalence Checking | Compares corresponding combinational functions. | [Lesson 25](../Day%2005.md#lesson-25-formal-verification---iv) |
| SEC | Sequential Equivalence Checking | Compares behavior over legal sequences and related initial states. | [Lesson 25](../Day%2005.md#lesson-25-formal-verification---iv) |
| LEF | Library Exchange Format | Abstract physical information for cells and routing. | [Lesson 26](../Day%2005.md#lesson-26-technology-library) |
| Liberty | Liberty timing-library format | Cell functions, timing, units and power models in .lib files. | [Lesson 26](../Day%2005.md#lesson-26-technology-library) |
| NLDM | Nonlinear Delay Model | Lookup models of delay and transition versus slew and load. | [Lesson 26](../Day%2005.md#lesson-26-technology-library) |
| CCS | Composite Current Source | More detailed current-based library model. | [Lesson 26](../Day%2005.md#lesson-26-technology-library) |
| ECSM | Effective Current Source Model | Current-source model introduced alongside NLDM and CCS. | [Lesson 26](../Day%2005.md#lesson-26-technology-library) |
| PVT | Process, Voltage, Temperature | Operating/characterization conditions of timing models. | [Lesson 30](../Day%2005.md#lesson-30-static-timing-analysis---iii) |
| STA | Static Timing Analysis | Analyzes timing paths with models and constraints. | [Lesson 28](../Day%2005.md#lesson-28-static-timing-analysis---i) |
| tCQ | Clock-to-Q delay | Delay from the launch clock pin to changing Q. | [Lesson 28](../Day%2005.md#lesson-28-static-timing-analysis---i) |
| tSU | Setup time | Required data stability before a capture edge. | [Lesson 28](../Day%2005.md#lesson-28-static-timing-analysis---i) |
| tH | Hold time | Required data stability after a capture edge. | [Lesson 28](../Day%2005.md#lesson-28-static-timing-analysis---i) |
| GBA | Graph-Based Analysis | Propagates timing bounds through graph vertices. | [Lesson 29](../Day%2005.md#lesson-29-static-timing-analysis---ii) |
| PBA | Path-Based Analysis | Recomputes selected paths with path-consistent quantities. | [Lesson 29](../Day%2005.md#lesson-29-static-timing-analysis---ii) |
| MMMC | Multi-Mode Multi-Corner | Checks justified combinations of mode and timing conditions. | [Lesson 30](../Day%2005.md#lesson-30-static-timing-analysis---iii) |
| OCV | On-Chip Variation | Models local timing variation using appropriate early/late effects. | [Lesson 30](../Day%2005.md#lesson-30-static-timing-analysis---iii) |
| SDC (timing) | Synopsys Design Constraints | Tcl-based design/timing requirements. | [Lesson 32](../Day%2006.md#lesson-32-constraints-i) |
| PPA | Power, Performance, Area | Interacting implementation quality measures. | [Lesson 02](../Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| SPEF | Standard Parasitic Exchange Format | Extracted interconnect resistance and capacitance information. | [Lesson 29](../Day%2005.md#lesson-29-static-timing-analysis---ii) |
| CTS | Clock Tree Synthesis | Builds a clock-distribution network. | [Lesson 07](../Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| DRC | Design Rule Checking | Checks geometric manufacturing rules. | [Lesson 08](../Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| LVS | Layout Versus Schematic | Checks extracted layout connectivity against a design reference. | [Lesson 08](../Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| DFT | Design For Test | Structures that improve manufactured-device testability. | [Lesson 08](../Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| ATE | Automatic Test Equipment | Applies and measures manufactured-device test patterns. | [Lesson 08](../Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
