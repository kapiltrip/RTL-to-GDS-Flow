# Full forms and meanings

[Master index](../README.md) · [Read the PDF](../Full%20Forms.pdf)

Alphabetical terminology for the completed lessons and the RTL-to-GDS overview. Each entry links to the relevant daily explanation; that lesson contains lecture frames, timestamps and supporting primary references. Coverage extends through all 54 lessons and Week 12. Links point to the detailed treatment, including ATPG, BIST and final physical verification.

Context matters: SDC has separate logic and timing meanings; CDC here means controllability don't-care. Liberty is a format name. tCQ, tSU and tH are timing symbols rather than acronyms. NAND, NOR, XOR, SAT, UNSAT and TB are conventional abbreviations or operation names.

| Term | Full form or expansion | Meaning | Deep explanation |
|---|---|---|---|
| ASIC | Application-Specific Integrated Circuit | A chip designed for a particular application. | [Lesson 02](../Daily%20Notes/Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| AST | Abstract Syntax Tree | Hierarchical representation of parsed source syntax. | [Lesson 15](../Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| ATE | Automatic Test Equipment | Applies and measures manufactured-device test patterns. | [Lesson 08](../Daily%20Notes/Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| ATPG | Automatic Test Pattern Generation | Derives patterns to detect modeled manufacturing faults; fault-model coverage differs from functional coverage. | [Explanation](../Daily%20Notes/Day%2007.md#lesson-42-automatic-test-pattern-generation) |
| BCP | Boolean Constraint Propagation | Repeated deduction from unit clauses. | [Lesson 23](../Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| BDD | Binary Decision Diagram | Graph representing recursive Boolean decisions. | [Lesson 21](../Daily%20Notes/Day%2004.md#lesson-21-formal-verification---i) |
| BEOL | Back End of Line | Fabrication of interconnect and related structures after the transistor/device stages; not the entire physical-design workflow. | [Explanation](../Daily%20Notes/Day%2008.md#d-09-feol-forms-devices-beol-connects-them) |
| BIST | Built-In Self-Test | On-chip pattern generation and response evaluation for a defined test target. | [Explanation](../Daily%20Notes/Day%2008.md#lesson-43-built-in-self-test) |
| BMC | Bounded Model Checking | Checks unfolded behavior through a specified cycle bound. | [Lesson 24](../Daily%20Notes/Day%2004.md#lesson-24-formal-verification---iii) |
| CCS | Composite Current Source | More detailed current-based library model. | [Lesson 26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| CDC | Controllability Don't-Care | Impossible internal input combination caused by network dependencies. | [Lesson 19](../Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii) |
| CEC | Combinational Equivalence Checking | Compares corresponding combinational functions. | [Lesson 25](../Daily%20Notes/Day%2005.md#lesson-25-formal-verification---iv) |
| CMOS | Complementary Metal-Oxide-Semiconductor | Uses complementary n-channel and p-channel devices; the inverter illustrates pull-down and pull-up behavior. | [Lesson 01](../Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| CNF | Conjunctive Normal Form | AND of clauses, each an OR of literals. | [Lesson 23](../Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| CPU | Central Processing Unit | Executes an instruction set; an architecture may allocate some behavior to software running on it. | [Lesson 04](../Daily%20Notes/Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) |
| CTS | Clock Tree Synthesis | Builds a clock-distribution network. | [Explanation](../Daily%20Notes/Day%2009.md#lesson-51-clock-tree-synthesis) |
| CTS skew | Capture arrival minus launch arrival, S=C−L | Positive pair skew adds setup margin and removes hold margin for the stated same-clock path. | [Explanation](../Daily%20Notes/Day%2009.md#e-07-useful-skew-transfers-margin-and-can-create-hold-failures) |
| DC | Don't-Care | Behavior permitted to vary under justified specification conditions. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| DEF | Design Exchange Format | Exchanges a design instance's physical implementation data, such as placement, nets and routing. | [Lesson 07](../Daily%20Notes/Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| DFT | Design For Test | Structures that improve manufactured-device testability. | [Explanation](../Daily%20Notes/Day%2007.md#lesson-39-basic-concepts-of-dft) |
| DPLL | Davis-Putnam-Logemann-Loveland | SAT search through decisions, implications and backtracking. | [Lesson 23](../Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| DRC | Design Rule Checking | Checks geometric manufacturing rules. | [Explanation](../Daily%20Notes/Day%2009.md#e-17-drc-checks-geometry-erc-checks-electrical-construction) |
| DUT | Design Under Test | Implementation exercised by a verification environment. | [Lesson 13](../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| DVFS | Dynamic Voltage and Frequency Scaling | Changes voltage and frequency together; distinguish power from energy for a fixed task. | [Explanation](../Daily%20Notes/Day%2007.md#c-16-signal-probability-is-not-transition-activity-dvfs-changes-both-power-and-time) |
| ECO | Engineering Change Order | A controlled connectivity/geometry change followed by renewed affected verification. | [Explanation](../Daily%20Notes/Day%2009.md#e-19-ecos-change-the-evidence-tapeout-releases-a-verified-layout) |
| ECSM | Effective Current Source Model | Current-source model introduced alongside NLDM and CCS. | [Lesson 26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| EDA | Electronic Design Automation | Tools for design, implementation and verification. | [Lesson 05](../Daily%20Notes/Day%2001.md#lesson-05-tutorial-1--unix-foundations-for-eda) |
| EM | Electromigration | Current/stress-related material transport requiring technology-qualified reliability limits. | [Explanation](../Daily%20Notes/Day%2008.md#d-20-meshes-spread-current-electromigration-sets-reliability-limits) |
| EPI | Essential Prime Implicant | Prime covering a required minterm uniquely among primes. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| ERC | Electrical Rule Checking | Checks electrical connection and usage rules defined by the technology and rule deck. | [Explanation](../Daily%20Notes/Day%2009.md#e-17-drc-checks-geometry-erc-checks-electrical-construction) |
| ESL | Equivalent Series Inductance | A capacitor connection/model has inductance that limits rapid current delivery. | [Explanation](../Daily%20Notes/Day%2008.md#d-21-separate-steady-ir-drop-from-transient-droop-and-decap-support) |
| ESR | Equivalent Series Resistance | A capacitor model includes resistive loss and voltage drop in addition to ideal charge storage. | [Explanation](../Daily%20Notes/Day%2008.md#d-21-separate-steady-ir-drop-from-transient-droop-and-decap-support) |
| FEOL | Front End of Line | Fabrication stages that form device structures, before most interconnect processing. | [Explanation](../Daily%20Notes/Day%2008.md#d-09-feol-forms-devices-beol-connects-them) |
| FPGA | Field-Programmable Gate Array | Configurable logic and routing programmed after manufacture. | [Lesson 02](../Daily%20Notes/Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| FSM | Finite State Machine | State, transition and output model for sequential behavior. | [Lesson 20](../Daily%20Notes/Day%2004.md#lesson-20-logic-optimization---part-iii) |
| GBA | Graph-Based Analysis | Propagates timing bounds through graph vertices. | [Lesson 29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| GDSII | Graphic Data System II | Layout exchange format used for geometric mask data. | [Lesson 09](../Daily%20Notes/Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |
| HDL | Hardware Description Language | Models concurrent hardware behavior and structure. | [Lesson 11](../Daily%20Notes/Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) |
| HLS | High-Level Synthesis | Schedules and binds behavioral operations into hardware. | [Lesson 14](../Daily%20Notes/Day%2003.md#lesson-14-high-level-synthesis-using-bambu---tutorial-3) |
| HPWL | Half-Perimeter Wire Length | Bounding-box estimate used in placement; does not specify a legal routed tree. | [Explanation](../Daily%20Notes/Day%2009.md#d-23-hpwl-is-a-bounding-box-estimate-not-a-routed-tree) |
| IC | Integrated Circuit | Devices and interconnect integrated on a substrate. | [Lesson 01](../Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| IP | Intellectual Property | Reusable design block and supporting integration information. | [Lesson 04](../Daily%20Notes/Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) |
| LEF | Library Exchange Format | Abstract physical information for cells and routing. | [Lesson 26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| LFSR | Linear Feedback Shift Register | Deterministic shift/XOR recurrence; taps, convention and seed set its sequence. | [Explanation](../Daily%20Notes/Day%2008.md#d-07-work-out-the-seven-state-lfsr-and-the-rare-pattern-problem) |
| Liberty | Liberty timing-library format | Cell functions, timing, units and power models in .lib files. | [Lesson 26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| LVS | Layout Versus Schematic | Checks extracted layout connectivity against a design reference. | [Explanation](../Daily%20Notes/Day%2009.md#e-18-lvs-and-signoff-must-refer-to-the-same-final-design) |
| MISR | Multiple-Input Signature Register | Compacts several response bits per step into a finite signature, with possible aliasing. | [Explanation](../Daily%20Notes/Day%2008.md#d-08-signature-compression-trades-data-volume-for-aliasing-risk) |
| MMMC | Multi-Mode Multi-Corner | Checks justified combinations of mode and timing conditions. | [Lesson 30](../Daily%20Notes/Day%2005.md#lesson-30-static-timing-analysis---iii) |
| MOSFET | Metal-Oxide-Semiconductor Field-Effect Transistor | Gate voltage controls channel conduction; complementary device types form CMOS logic. | [Lesson 01](../Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| NAND | NOT-AND | Boolean complement of AND; its output is zero only when every input is one. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| NBA | Nonblocking Assignment | Schedules a later left-side update after evaluating the right side. | [Lesson 13](../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| NLDM | Nonlinear Delay Model | Lookup models of delay and transition versus slew and load. | [Lesson 26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| NMOS | N-channel Metal-Oxide-Semiconductor | N-channel MOS device; the CMOS inverter uses it for the pull-down path. | [Lesson 01](../Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| NOR | NOT-OR | Boolean complement of OR; its output is one only when every input is zero. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| OCV | On-Chip Variation | Models local timing variation using appropriate early/late effects. | [Lesson 30](../Daily%20Notes/Day%2005.md#lesson-30-static-timing-analysis---iii) |
| ODC | Observability Don't-Care | Internal variation masked at all relevant observed outputs. | [Lesson 19](../Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii) |
| OPC | Optical Proximity Correction | Adjusts mask geometry to compensate for predictable lithographic printing distortion. | [Lesson 09](../Daily%20Notes/Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |
| PBA | Path-Based Analysis | Recomputes selected paths with path-consistent quantities. | [Lesson 29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| PDK | Process Design Kit | Process models, layers and design rules. | [Lesson 01](../Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| PDN | Power Delivery Network | Connected supply/ground structures whose impedance affects local voltage, timing and reliability. | [Explanation](../Daily%20Notes/Day%2008.md#d-21-separate-steady-ir-drop-from-transient-droop-and-decap-support) |
| PI | Prime Implicant | A legal product cube that cannot be further expanded. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| PMOS | P-channel Metal-Oxide-Semiconductor | P-channel MOS device; the CMOS inverter uses it for the pull-up path. | [Lesson 01](../Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| POS | Product of Sums | AND of OR terms in Boolean notation. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| PPA | Power, Performance, Area | Interacting implementation quality measures. | [Lesson 02](../Daily%20Notes/Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| PVT | Process, Voltage, Temperature | Operating/characterization conditions of timing models. | [Lesson 30](../Daily%20Notes/Day%2005.md#lesson-30-static-timing-analysis---iii) |
| RC | Resistance-Capacitance | Interconnect resistance and capacitance contribute to delay, transition and loading. | [Lesson 29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| ROBDD | Reduced Ordered Binary Decision Diagram | Canonical for one fixed variable order, with reduction rules applied. | [Lesson 21](../Daily%20Notes/Day%2004.md#lesson-21-formal-verification---i) |
| RPI | Redundant Prime Implicant | In the essentials-first classification, a nonessential prime whose ON points are already covered by selected essentials. | [A-13 cover selection](../Daily%20Notes/Day%2003.md#a-13-the-prime-implicants-of-ab--abc--bc) |
| RTL | Register Transfer Level | Describes transfers and transformations between state elements. | [Lesson 15](../Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| SAT | Boolean Satisfiability | Existence of an assignment satisfying a Boolean formula. | [Lesson 23](../Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| SDC (logic) | Satisfiability Don't-Care | Impossible relation between local inputs and their computed output. | [Lesson 19](../Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii) |
| SDC (timing) | Synopsys Design Constraints | Tcl-based design/timing requirements. | [Lesson 32](../Daily%20Notes/Day%2006.md#lesson-32-constraints-i) |
| SEC | Sequential Equivalence Checking | Compares behavior over legal sequences and related initial states. | [Lesson 25](../Daily%20Notes/Day%2005.md#lesson-25-formal-verification---iv) |
| SoC | System on Chip | Integrates major system functions and reusable blocks on one integrated circuit. | [Lesson 04](../Daily%20Notes/Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) |
| SOP | Sum of Products | OR of AND terms in Boolean notation. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| SPEF | Standard Parasitic Exchange Format | Extracted interconnect resistance and capacitance information. | [Lesson 29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| SPI | Selective Prime Implicant | Remaining nonessential prime that can cover a still-uncovered ON point; select a sufficient residual cover. | [A-14 worked chart](../Daily%20Notes/Day%2003.md#a-14-coverage-charts-minimal-covers-and-minimum-cost) |
| STA | Static Timing Analysis | Analyzes timing paths with models and constraints. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| TB | Testbench | Stimulus, checking and supporting simulation logic. | [Lesson 13](../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| Tcl | Tool Command Language | Command language used by many EDA interfaces. | [Lesson 10](../Daily%20Notes/Day%2002.md#lesson-10-introduction-to-tcl) |
| tCQ | Clock-to-Q delay | Delay from the launch clock pin to changing Q. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| tH | Hold time | Required data stability after a capture edge. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| tSU | Setup time | Required data stability before a capture edge. | [Lesson 28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| UNSAT | Unsatisfiable | No satisfying assignment under the encoded conditions. | [Lesson 23](../Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| VCD | Value Change Dump | Timestamped signal changes for waveform inspection. | [Lesson 13](../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| VLSI | Very Large Scale Integration | Integration scale motivating a staged design flow. | [Lesson 03](../Daily%20Notes/Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) |
| XOR | Exclusive OR | For two inputs, the output is one when they differ; multiple-input XOR represents odd parity. | [Lesson 17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |

## Reference trail

[NPTEL course outline](https://onlinecourses.nptel.ac.in/e-learning/preview/noc26_ee147) establishes the course terminology and teaching sequence. The [course lecture playlist](https://www.youtube.com/playlist?list=PLyqSpQzTE6M8iOrfy70ELk9W72JG5a98V), the source frames and the [source register](Sources.md) supply the evidence behind the linked lesson explanations. Meanings are concise study summaries, with the particular context stated where an abbreviation is ambiguous.
