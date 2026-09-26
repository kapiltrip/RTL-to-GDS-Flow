# Day 03 — Overview of VLSI Design Flow I

[Course index](README.md) · Week 1 · [Lecture video](https://www.youtube.com/watch?v=vKtoQEAoGck) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [From a product idea to a manufactured chip](#from-a-product-idea-to-a-manufactured-chip)
- [Abstraction and turnaround time](#abstraction-and-turnaround-time)
- [Hardware and software partitioning](#hardware-and-software-partitioning)
- [Estimating hardware before it exists](#estimating-hardware-before-it-exists)

## From a product idea to a manufactured chip

![Pre-RTL, RTL-to-GDS, and post-GDS stages](images/Day%2003/01-flow.png)

*Video frame: [4:43](https://www.youtube.com/watch?v=vKtoQEAoGck&t=283s). Pre-RTL, RTL-to-GDS, and post-GDS stages*


The flow translates a desired behavior into successively more concrete representations. **Pre-RTL design** establishes requirements, chooses algorithms and architecture, partitions hardware and software, and defines cycle-level hardware behavior. **RTL-to-GDS** develops a gate-level implementation and then its physical layout. **Post-GDS** prepares manufacturing data, fabricates, tests, and packages the chip.

**RTL**, register-transfer level, models stored state and the logic that transforms data between storage elements. **GDSII** is a layout-data format describing hierarchical geometry and layers; it is not executable software for a processor. The manufacturing flow uses layout data to prepare patterns and process wafers. These stages are connected by verification and feedback, not a one-way chain that always succeeds on its first attempt.

![Kapil’s handwritten notes — Part 1, PDF page 7, lower portion](images/Day%2003/h01-abstraction.jpg)

*Handwritten source: Part 1, PDF page 7, lower portion.*


Your idea → RTL → GDS → chip chain is the backbone of the course. The “design” bracket includes decisions before RTL and physical implementation after synthesis. Fabrication begins after design-data handoff, but manufacturability must influence design much earlier through the PDK and physical checks.

## Abstraction and turnaround time

![The same NOR function described as an equation or a placed cell](images/Day%2003/02-abstraction.png)

*Video frame: [14:10](https://www.youtube.com/watch?v=vKtoQEAoGck&t=850s). The same NOR function described as an equation or a placed cell*


**Abstraction** is selective omission of detail so a representation exposes the properties needed for a particular decision. The Boolean equation $F=\overline{A+B}$ specifies the NOR truth function. It does not choose transistor sizes, a cell variant, a placement coordinate, or metal routes. A placed and connected NOR instance contains more implementation detail and supports more physically accurate analysis.

A high-level representation lets us compare architectural alternatives quickly. Replacing one algorithm or pipeline organization before layout may be inexpensive; making the equivalent change after placement and routing can require extensive reimplementation. **Turnaround time** is the time needed to complete an iteration. Lower abstraction often increases analysis cost, but it also exposes effects that the higher model hides. Neither level replaces the other: use a simple model to explore and a detailed model to validate.

![Kapil’s handwritten notes — Part 1, PDF page 8](images/Day%2003/h02-system.jpg)

*Handwritten source: Part 1, PDF page 8.*


Your NOR example correctly identifies the equation as the more abstract representation. The claim “hardware is parallel and software is sequential” is a useful introductory contrast, but it needs qualification. Hardware can contain serial dependencies and shared resources; software can use multiple cores, vectors, and threads. The architectural question is which implementation gives the required behavior, cost, flexibility, and performance under the actual workload.

Before partitioning, write measurable requirements: input/output formats, supported functions, maximum response time, throughput, power budget, and operating conditions. Market and schedule constraints help decide whether a technically possible design is a useful product. A vague requirement such as “very fast” cannot guide a partitioning algorithm.

## Hardware and software partitioning

![Profile bottlenecks, move functions into hardware, and evaluate again](images/Day%2003/03-partition.png)

*Video frame: [37:48](https://www.youtube.com/watch?v=vKtoQEAoGck&t=2268s). Profile bottlenecks, move functions into hardware, and evaluate again*


**Hardware/software partitioning** assigns system functions to dedicated hardware or programmable software. A common architecture combines a processor, memory, an interconnect, and one or more accelerators. The accelerator can exploit specialized datapaths and parallelism; software handles control, changing policies, or functions where dedicated hardware brings little benefit.

![Kapil’s handwritten notes — Part 1, PDF page 9](images/Day%2003/h03-partition.jpg)

*Handwritten source: Part 1, PDF page 9.*


In your CPU–memory–accelerator drawing, communication is part of the computation. An accelerator needs input data, configuration, a start/ready protocol, and a way to return results. Shared memory bandwidth and bus contention may become bottlenecks. Replacing an expensive software function with fast hardware does not remove the cost of moving data into and out of that hardware.

The lecture's DCT example illustrates a function that dominates execution time. To quantify the limit, let fraction $p$ of original execution time be accelerated by factor $s$, with normalized extra communication/control overhead $o$. A simple extension of Amdahl's argument is

$$
\text{speedup}=\frac{1}{(1-p)+p/s+o}.
$$

If $p=0.8$, $s=1000$, and $o=0$, total speedup is $1/(0.2+0.0008)\approx4.98$, not 1000. The unaccelerated 20% caps the ideal benefit near 5. Adding overhead of 0.05 reduces speedup to about 3.99. These calculations extend the lecture's example and show why whole-system evaluation matters.

![Kapil’s handwritten notes — Part 1, PDF page 10](images/Day%2003/h04-algorithm.jpg)

*Handwritten source: Part 1, PDF page 10.*


Read your algorithm as a heuristic search:

1. Start with hardware-function set $H=\varnothing$ and software set $S$ containing all candidate functions.
2. Evaluate the current system. If it meets the performance requirement, retain that partition.
3. Profile execution to identify dominant functions or communication costs.
4. Move selected candidate functions from $S$ to $H$, up to the chosen search limit, and evaluate again.
5. Continue if the changes improve the objective. Stop successfully when requirements are met; otherwise report that this search did not find an acceptable partition.

In a set update, $H\leftarrow H\cup\{f_i\}$ and $S\leftarrow S\setminus\{f_i\}$. The braces matter: a function is being moved as an element of a set. In a throughput objective, larger measured performance is better; in a latency objective, smaller is better. The inequality in a stopping condition must match the chosen metric.

“No partition found” is not proof that no feasible partition exists. A greedy choice can miss a beneficial combination or a different architecture. Reprofiling matters because removing one bottleneck exposes another. Moving functions can also create new communication and synchronization costs.

## Estimating hardware before it exists

An early performance estimate can come from an analytical model, high-level simulation, FPGA prototyping, or a rapid synthesis/implementation experiment. Each has limits. An FPGA prototype exercises hardware/software interaction but its clock, memory, and routing characteristics do not automatically predict ASIC timing. A high-level model can evaluate workloads quickly but must model communication and contention well enough for the decision.

**Co-simulation** connects models of hardware and software so their interaction can be checked. It helps expose protocol and sequencing mistakes, but its assurance depends on the models, stimuli, and properties checked. An early model is valuable when its assumptions and uncertainty are explicit.

**Recall checks:** Why might the most frequently called function be a poor accelerator candidate? Why can an accelerator with a short arithmetic delay still reduce total system performance? Why should the stopping condition distinguish feasibility from global optimality?

[Previous: Day 02](Day%2002.md) · [Next: Day 04](Day%2004.md)
