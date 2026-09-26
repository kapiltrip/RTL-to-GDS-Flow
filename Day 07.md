# Day 07 — Overview of VLSI Design Flow IV — Physical design

[Course index](README.md) · Week 2 · [Lecture video](https://www.youtube.com/watch?v=--wJOkCvn2M) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [From connectivity to geometry](#from-connectivity-to-geometry)
- [Floorplanning power and placement](#floorplanning-power-and-placement)
- [Clock tree synthesis](#clock-tree-synthesis)
- [Global routing detailed routing and closure](#global-routing-detailed-routing-and-closure)

## From connectivity to geometry

![Physical design adds placement, clock distribution, and routing](images/Day%2007/01-physical-flow.png)

*Video frame: [10:56](https://www.youtube.com/watch?v=--wJOkCvn2M&t=656s). Physical design adds placement, clock distribution, and routing*


**Physical design** converts a logical netlist into manufacturable layout geometry. The logical netlist says which pins connect; physical implementation chooses where instances sit and how metal and vias realize those connections. The tool also changes the implementation where needed, for example by inserting buffers or selecting different cell sizes, while preserving the required behavior.

![Kapil’s handwritten notes — Part 1, PDF page 17](images/Day%2007/h01-physical.jpg)

*Handwritten source: Part 1, PDF page 17.*


Your input diagram needs several complementary views:

| View or input | What it provides |
|---|---|
| Netlist | Instances and connectivity |
| Liberty | Cell function, timing, power, and related characterization |
| Cell/macro LEF | Abstract cell boundary, legal placement information, pin shapes, and obstructions |
| Technology LEF and process data | Routing layers, vias, relevant geometric rules, and technology information |
| Constraints | Clocks, external timing, and design intent |
| Floorplan | Die/core boundaries, regions, macro and I/O intent |

LEF stands for **Library Exchange Format**. It is deliberately an abstract physical view: routing needs to know where a macro's pins and obstacles are without repeatedly processing all its internal transistor geometry. Detailed extraction uses appropriate process/parasitic models; a LEF file is not a substitute for all electrical or manufacturing information. GDSII carries detailed layout geometry, while implementation databases and formats such as DEF can represent placed/routed design state.

## Floorplanning power and placement

**Floorplanning** establishes the large-scale organization of the chip: die and core size, major blocks, macro locations, I/O arrangement, and legal standard-cell regions. The **die** is the silicon boundary; the **core** is the principal implementation region inside it. **Placement** subsequently chooses legal locations for individual standard-cell instances.

**Utilization** is meaningful only with a stated denominator. A common early estimate divides standard-cell area by the available placement area. If cells occupy 0.60 mm² and the usable row area is 1.00 mm², utilization is 60%. The remaining space is not simply wasted: it provides flexibility for placement, buffers, clock cells, routing access, and later fixes. Excessively dense placement can cause congestion and timing detours.

![Kapil’s handwritten notes — Part 1, PDF page 18](images/Day%2007/h02-floorplan.jpg)

*Handwritten source: Part 1, PDF page 18.*


Your note about “location of standard cells” at chip planning means **allocate regions and rows**, not finalize every cell coordinate. Those millions of individual locations belong to placement. The rectilinear L/I sketches describe flexibility available for some blocks. A hard macro with fixed physical geometry cannot arbitrarily be reshaped; a soft block or hierarchical region can offer different aspect ratios or shapes depending on its implementation.

A **power delivery network (PDN)** distributes supply and ground through conductive structures to cells and macros. Wire resistance causes a voltage loss approximately $\Delta V=IR$ in a simple DC segment. For example, 20 mA through 0.5 Ω produces 10 mV of drop. Real networks have distributed current, transient effects, multiple paths, and reliability constraints. Lower local supply voltage can slow cells; adequate power wiring therefore supports timing as well as operation.

**Congestion** means routing demand is excessive relative to available routing resources in a region. A narrow channel between macros may attract many signals but offer few tracks. A globally short placement can still route poorly if it blocks pin access or concentrates too much traffic. Placement optimizes estimated wire length, timing, density, and routability before the exact wires exist; the quality of those estimates matters.

### Worked example: placement area and routing capacity

With utilization defined as cell area divided by usable placement area, rearrange the definition:

$$
A_{\text{placement}}=\frac{A_{\text{cells}}}{U}.
$$

For 0.60 mm² of cells, a 60% target requires 1.00 mm² of usable placement area; a 75% target requires 0.80 mm². The second estimate is 20% smaller. It is an area calculation, not proof of routability. Macros, blockages, reserved regions, and the chosen utilization definition determine how this usable area relates to the total core. Later buffers and clock cells can also change the cell-area numerator.

To understand congestion, imagine one routing boundary with eight available track units and twelve units of estimated demand. The demand/capacity ratio is $12/8=1.5$, and overflow is four units. Average chip utilization cannot reveal this local shortage. Other layers or detours may help, but their availability, vias, pin access, and delay must also be considered. These simple units illustrate the concept; actual congestion reports depend on the router's resource model.

Moving cells apart can reduce demand concentration, while moving a macro can open a blocked channel. Strengthening the PDN may reserve additional routing space for supplies. These interactions explain why floorplanning, power planning, placement, and routing need iteration. As a concrete tool example, [OpenROAD's global placer](https://openroad.readthedocs.io/en/latest/main/src/gpl/README.html) estimates congestion during routability-driven placement and increases the modeled area of cells in congested regions to encourage spreading.

**Try it:** if the cell area grows to 0.66 mm² while the usable placement area remains 1.00 mm², utilization becomes 66%. That percentage still does not tell you whether a particular macro channel has enough tracks.

## Clock tree synthesis

![Clock arrival times differ because the distribution network has delay](images/Day%2007/02-cts.png)

*Video frame: [32:49](https://www.youtube.com/watch?v=--wJOkCvn2M&t=1969s). Clock arrival times differ because the distribution network has delay*


**Clock tree synthesis (CTS)** builds a network that distributes clock events to sequential elements with controlled skew, latency, transition time, and load. A single ideal clock source cannot directly drive an arbitrarily large physical load with zero delay. Buffers and branches distribute that load.

**Clock latency** is the delay from the chosen clock reference to a sink. **Clock skew** is the difference in arrival times between specified sinks. If one sink receives an edge at 10 ps and another at 15 ps, their arrival difference is 5 ps. Equal latency at all sinks can give zero skew even when that common latency is large. Skew and latency are therefore different quantities.

Symmetric topology and balanced electrical loading can reduce skew, but equal drawn wire lengths alone do not guarantee equal delays. Cell delays, loading, parasitics, and variation matter. The introductory goal is small skew; practical timing optimization can also use controlled useful skew under explicit setup and hold analysis.

![Kapil’s handwritten notes — Part 1, PDF page 19](images/Day%2007/h03-cts-routing.jpg)

*Handwritten source: Part 1, PDF page 19.*


Your high-priority clock note reflects its role in synchronous operation. Clock routing is planned before much ordinary signal routing in the lecture's flow, when resources are less constrained. The clock switches frequently and drives large capacitance, so it can consume a substantial fraction of dynamic power. The percentage depends on the design; it is not a universal constant.

**Clock gating** prevents unnecessary clock transitions from reaching inactive logic. The enable must be applied using a glitch-safe structure and verified behavior. A naive AND gate whose enable changes at the wrong time can create an unintended edge. Gating cells can be inserted at different points in an actual flow, so it should not be remembered as an operation that only ever occurs during CTS.

## Global routing detailed routing and closure

![Detailed routing chooses actual wires and vias within the planned regions](images/Day%2007/03-routing.png)

*Video frame: [41:13](https://www.youtube.com/watch?v=--wJOkCvn2M&t=2473s). Detailed routing chooses actual wires and vias within the planned regions*


**Global routing** plans approximate paths through routing regions and layers while accounting for capacity and congestion. **Detailed routing** assigns actual tracks, wire shapes, and vias to connect pins legally. A global route is a plan, not proof that a design-rule-clean detailed route exists. Pin access, spacing, enclosure, and competing wires can invalidate an apparently reasonable plan.

Routing seeks legal connectivity and suitable timing while managing wire length, via count, and congestion. More vias can add resistance and physical constraints; a long detour can worsen delay. After routing, extraction provides more realistic parasitic resistance and capacitance than early estimates, allowing timing and signal-integrity checks to be repeated.

![Kapil’s handwritten notes — Part 1, PDF page 20, right-side ECO notes](images/Day%2007/h04-eco.jpg)

*Handwritten source: Part 1, PDF page 20, right-side ECO notes.*


An **engineering change order (ECO)** is a controlled implementation change, often used for late functional or timing fixes. Examples include resizing a cell, inserting a buffer, or changing selected logic and connections. Every such change needs the appropriate rechecks. A “small” edit in the file can affect many paths, so its impact is judged electrically and logically, not by the number of edited lines.

**Design closure** means that the implementation satisfies the required set of checks and constraints for the intended operating scenarios. It can require iterations: routing may expose a congested placement, and a timing fix may worsen power or hold timing. Your arrows back to earlier stages capture this feedback. **Tapeout** is release of the validated manufacturing design data to the foundry; it does not mean that fabricated parts have already passed test.

**Recall checks:** Can a netlist have correct connectivity but an unroutable placement? Can two clock sinks have equal latency but nonzero skew? Which checks must be revisited after inserting a buffer on a timing-critical net?

[Previous: Day 06](Day%2006.md) · [Next: Day 08](Day%2008.md)
