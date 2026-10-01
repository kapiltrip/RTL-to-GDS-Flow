# RTL to GDS Flow

Implementation sequence, stage purpose and the NPTEL teaching approach.

## 1. Define intent and architecture

Set function, interfaces and power/performance/area targets; partition the design into blocks. Architecture determines what hardware must do. High-level synthesis is one route from behavioral operations to a datapath and controller; RTL can also be written directly. [L03-L04](../Daily%20Notes/Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i)

## 2. Model and verify RTL

Describe bit-accurate combinational logic and state transitions. Simulation exercises behavior with a testbench; formal methods check specified properties or equivalence under stated assumptions. Resolve intent before implementation. Output: verified synthesizable RTL and its requirements. [L11](../Daily%20Notes/Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i); [L13](../Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation)

## 3. Synthesize a technology-mapped netlist

**Elaborate and infer hardware.** Resolve hierarchy, parameters and widths; turn RTL constructs into registers, multiplexers, arithmetic and control networks. [L15-L16](../Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i)

**Optimize logic.** Simplify Boolean covers, factor/share expressions and optimize state representations while preserving required behavior. Cost depends on both logic structure and its implementation. [L17](../Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i); [L19-L20](../Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii)

**Map to technology.** Select legal cells from a characterized library under timing, load and area objectives. Output: a cell-instance netlist with connectivity. Constraints and library models guide optimization from this stage onward. [L26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library); [L32](../Daily%20Notes/Day%2006.md#lesson-32-constraints-i)

## 4. Make the design testable

Plan DFT early; add appropriate scan/test structures to improve internal controllability and observability. Generate tests for defined fault models and recheck functional/test modes and timing. Scan insertion and physical scan-chain reordering belong to coordinated logical and physical stages. [L08](../Daily%20Notes/Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test)

## 5. Implement the physical design

**Floorplan and power plan:** set die/core organization, macro locations, pin access and the supply network; provide space and electrical support for implementation.

**Place and legalize:** assign legal cell locations, balancing wirelength, congestion and timing. **Clock tree synthesis:** distribute clocks with controlled skew, latency and transition.

**Route:** allocate signal paths, then create rule-compliant wires and vias. Output: placed and routed geometry with a realizable clock and power network. [L07](../Daily%20Notes/Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design)

## 6. Close and hand off GDSII

Extract interconnect parasitics; close setup/hold timing across required modes/corners, physical rules and power/reliability checks. DRC checks geometry, LVS checks extracted connectivity against the reference, and ERC checks electrical rules. ECOs trigger relevant rechecks. GDSII exports layout geometry; masks, fabrication, packaging and manufactured-device test follow the design handoff. [L08-L09](../Daily%20Notes/Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test)

<!-- pagebreak -->

# Iteration and course approach

## Why optimization appears more than once

Logic minimization changes functions' representations. Technology mapping changes the available gates and their costs. Placement and routing then expose wire resistance, capacitance and congestion. A smaller Boolean expression can map to slower cells or worse wiring; each stage updates the information used to judge the implementation.

| Where it occurs | What changes | Why repeat it? |
|---|---|---|
| Before mapping | Boolean covers, factoring, shared logic and state encodings | Reduce structural cost while preserving specified behavior. |
| During/after mapping | Library cell choices, drive strengths and buffering | Meet modeled delay, transition, load and area requirements. |
| After placement, CTS and routing | Locations, buffers, cell sizes and selected connections | Repair violations using progressively more accurate physical information. |

Resizing a gate changes both its delay and the load seen by its driver. A hold-fix buffer adds delay and can consume setup margin. Repair one violation, then recheck interacting paths; estimated placement parasitics and extracted routed parasitics provide different evidence. [Timing-repair rationale](https://openroad.readthedocs.io/en/latest/main/src/rsz/README.html#repair-timing)

## Models and checks that accompany the flow

**Constraints:** define clocks, external interface timing and justified timing exceptions; timing analysis needs the intended operating requirements. **Libraries:** supply cell functions, delay/check models and operating conditions. **Parasitics:** model interconnect loading and delay, with fidelity appropriate to the implementation stage. [L26](../Daily%20Notes/Day%2005.md#lesson-26-technology-library); [L29](../Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii); [L32](../Daily%20Notes/Day%2006.md#lesson-32-constraints-i)

**Functional checks** establish behavior under a specification and assumptions. **STA** checks modeled timing requirements. **DRC/LVS/ERC** check physical or electrical implementation rules. Passing one check does not establish the others. [L08](../Daily%20Notes/Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test); [L25](../Daily%20Notes/Day%2005.md#lesson-25-formal-verification---iv); [L28](../Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i)

## How NPTEL builds the theory

| Weeks | Main emphasis |
|---|---|
| 1-2 | IC technology, abstractions and the complete design flow |
| 3 | Verilog modeling and functional simulation |
| 4-5 | RTL synthesis, logic/FSM optimization and formal engines |
| 6 | Formal checking and technology libraries |
| 7-8 | STA, constraints, technology mapping and timing optimization |
| 9-10 | Power, DFT/ATPG/BIST and physical-design foundations |
| 11-12 | Floorplanning, placement, CTS, routing and closure |

The teaching order introduces models before detailed optimization. Implementation uses those models together and revisits earlier decisions as physical information becomes available. These concepts carry into a Synopsys-based flow; commands and stage boundaries depend on the chosen tool environment.

## Sources and deeper reading

[NPTEL official course outline](https://onlinecourses.nptel.ac.in/e-learning/preview/noc26_ee147) supports the week sequence and flow scope. Lesson links open the detailed course notes. The [timing-repair reference](https://openroad.readthedocs.io/en/latest/main/src/rsz/README.html#repair-timing) supports interacting setup/hold repairs; only the underlying rationale is used here. [Full forms](../Full%20Forms.pdf) expands the abbreviations. Current completed notes end at Week 8, Constraints I (Lesson 32).
