# Day 02 — Basic Concepts of Integrated Circuit II

[Course index](README.md) · Week 1 · [Lecture video](https://www.youtube.com/watch?v=6lJ2u7eYrek) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [Application-specific and general-purpose chips](#application-specific-and-general-purpose-chips)
- [Four implementation styles](#four-implementation-styles)
- [Economics and the break-even point](#economics-and-the-break-even-point)
- [PPA and the rest of design quality](#ppa-and-the-rest-of-design-quality)

## Application-specific and general-purpose chips

![ASIC and general-purpose IC examples](images/Day%2002/01-application-classes.png)

*Video frame: [5:16](https://www.youtube.com/watch?v=6lJ2u7eYrek&t=316s). ASIC and general-purpose IC examples*


An **application-specific integrated circuit (ASIC)** is designed around a particular application or class of applications. A **general-purpose IC** supplies a reusable capability that can serve many systems. A microprocessor executes different programs; a memory stores information for many applications; an FPGA offers configurable logic. This classification describes intended use, whereas full-custom, standard-cell, and FPGA-based design describe implementation styles.

An ASIC can contain a programmable processor. It is still application-specific if the whole chip is built for a particular purpose. Conversely, configuring an FPGA for a camera does not mean you fabricated a custom ASIC: you implemented application-specific behavior on a manufactured programmable fabric. Production volume and programmability are tendencies in the lecture's introductory comparison, not necessary definitions. Some ASICs ship in enormous volumes, and some general-purpose parts serve small markets.

![Kapil’s handwritten notes — Part 1, PDF page 3, lower portion](images/Day%2002/h01-applications.jpg)

*Handwritten source: Part 1, PDF page 3, lower portion.*


Your camera/audio-processing examples distinguish the product's intended function from the flexibility offered to its user. Read “less programmable” as “more of the function is fixed in hardware,” not “contains no programmable element.” Volume helps choose a cost-effective implementation, but it cannot by itself identify a chip as ASIC or general-purpose.

## Four implementation styles

![Comparison of customization, design effort, masks, and PPA](images/Day%2002/02-design-styles.png)

*Video frame: [18:53](https://www.youtube.com/watch?v=6lJ2u7eYrek&t=1133s). Comparison of customization, design effort, masks, and PPA*


| Style | What the designer customizes | What is reused | Main consequence |
|---|---|---|---|
| Full custom | Transistor circuits, sizes, and layout geometry | Process/device knowledge and selected existing blocks | Greatest freedom and substantial design and verification effort |
| Standard cell | Cell instances, connectivity, placement, and routing | Pre-designed, characterized logic cells and macros | Automation handles large digital designs efficiently |
| Gate array | Principally the interconnection of prefabricated devices | A regular base device array | Less device-level freedom; only selected mask layers are customized |
| FPGA | Configuration bits controlling logic and routing | The already fabricated programmable chip | Rapid reconfiguration; programmable fabric consumes area and delay |

A **standard cell** is a library implementation of a small function, such as a NAND gate, multiplexer, buffer, or flip-flop. A family usually has compatible row heights and several widths and drive strengths. A **macro** is a larger block, such as an SRAM, whose physical shape need not match a single standard-cell row. The physical-design tool places instances of these blocks and routes their connections.

Full custom is useful where transistor-level choices matter strongly, including analog circuits and highly optimized blocks. Standard-cell design still fabricates a custom layout: reusing a cell's design does not mean the final wafer already contains the placed cells. An FPGA, by contrast, already exists as silicon before the customer's design is loaded. Configuration selects functions and routes through that silicon; it does not create new metal layers.

The slide's PPA ranking is a broad comparison for implementing comparable functionality. It is not a promise that any full-custom design is better than any standard-cell design. Process, architecture, engineering quality, hard blocks, and constraints all matter.

![Kapil’s handwritten notes — Part 1, PDF page 4](images/Day%2002/h02-design-styles.jpg)

*Handwritten source: Part 1, PDF page 4.*


Your note correctly separates cell creation from cell use. During ordinary standard-cell implementation, you choose and instantiate characterized cells. Changing a NAND's internal transistor sizes or layout would create a different cell that needs appropriate characterization and physical verification. Selecting `NAND2_X1` versus a stronger library variant is not the same as editing that cell's internal geometry.

![Kapil’s handwritten notes — Part 1, PDF page 5](images/Day%2002/h03-fpga.jpg)

*Handwritten source: Part 1, PDF page 5.*


### Your question: FPGA versus cell-based design

Both can start from RTL, but their targets differ. ASIC synthesis maps logic into the selected standard-cell library; FPGA synthesis and implementation map logic into lookup tables, flip-flops, routing switches, memories, DSP blocks, and other resources provided by that FPGA family. A lookup table stores a truth-table result for each input combination; programmable routing connects blocks. The FPGA user pays for available fabric, including unused capacity and configurability overhead. The ASIC designer pays substantial development cost but can tailor the fabricated implementation to the application.

Gate arrays are different again: base devices are fabricated in advance, but customization traditionally occurs through a manufacturing step for selected interconnect layers. FPGA configuration happens electrically after manufacturing. Fill your comparison table using these distinctions, especially the **custom mask** row: all relevant custom layout layers for a conventional standard-cell ASIC, selected upper layers for a traditional gate array, and no customer-specific fabrication masks for FPGA configuration.

## Economics and the break-even point

![Fixed cost, per-unit cost, and the break-even graph](images/Day%2002/03-cost.png)

*Video frame: [27:52](https://www.youtube.com/watch?v=6lJ2u7eYrek&t=1672s). Fixed cost, per-unit cost, and the break-even graph*


**Fixed cost** is development expenditure that is approximately independent of how many units are produced in a particular comparison: design work, verification, tools, and masks are examples. **Variable cost** grows with unit count: fabrication, packaging, test, and procurement contribute. Costs can be more complicated in practice, but a useful first model is

$$
C_{\text{total}}=C_{\text{fixed}}+N C_{\text{unit}}.
$$

The graph's vertical intercept is fixed cost; its slope is variable cost per unit. A standard-cell ASIC often has a larger intercept and smaller slope than an FPGA implementation of the same function. At low volume, avoiding ASIC development cost can dominate. At high volume, saving cost on every unit can repay that investment.

![Kapil’s handwritten notes — Part 1, PDF page 6, cost comparison](images/Day%2002/h04-cost.jpg)

*Handwritten source: Part 1, PDF page 6, cost comparison.*


### Your question: what should we choose?

Use required performance, power, volume, schedule, reprogrammability, and total cost together. The cheapest projected manufacturing cost is irrelevant if the design cannot meet the deadline or performance requirement. Conversely, choosing an expensive implementation only for a small speed benefit may be unjustified if both meet the specification.

For an **illustrative calculation**, let ASIC fixed cost be 10,000,000 cost units and unit cost 100; let FPGA fixed cost be 1,000,000 and unit cost 400. Equating total costs gives

$$
N_{\text{break-even}}=\frac{10{,}000{,}000-1{,}000{,}000}{400-100}=30{,}000.
$$

Below 30,000 units, this simplified model favors FPGA cost; above it, ASIC cost. These are teaching numbers, not current price quotations. Mask respins, yield, inventory, engineering changes, and time value can shift the decision. In the slide's manufacturing model, larger die area reduces gross dies per wafer and can reduce yield; both can increase cost per good die. A commercial FPGA purchase price also includes many business factors beyond bare-die cost.

## PPA and the rest of design quality

![Power, performance, and area as competing objectives](images/Day%2002/04-ppa.png)

*Video frame: [30:13](https://www.youtube.com/watch?v=6lJ2u7eYrek&t=1813s). Power, performance, and area as competing objectives*


**Power** is the rate of energy consumption. Dynamic power includes switching-related consumption; static power includes leakage while the logical state is unchanged. **Performance** must be specified as a useful metric: clock frequency, operations per second, response latency, or another application measure. **Area** can mean the total cell area, core area, or die area; these are different quantities and must be named.

For example, a higher clock frequency does not guarantee lower end-to-end latency if an implementation requires many more cycles. A small cell-area result may still require a larger core to allow routing. Increasing drive strength may improve timing while increasing input capacitance, area, and power. An improvement in one figure can therefore worsen another.

![Kapil’s handwritten notes — Part 1, PDF page 6, PPA note](images/Day%2002/h05-ppa.jpg)

*Handwritten source: Part 1, PDF page 6, PPA note.*

![Kapil’s handwritten notes — Part 1, PDF page 7, upper portion](images/Day%2002/h06-quality.jpg)

*Handwritten source: Part 1, PDF page 7, upper portion.*


Your added measures are essential: **testability** is how readily manufacturing faults can be controlled and observed; **reliability** concerns correct operation over the required lifetime and conditions; **time to market** is the schedule for delivering a usable product. **Quality of results (QoR)** is judged against the chosen objectives and constraints. A feasible design meets the constraints; an optimal design is best under a precisely defined objective and search space. Large design problems usually use heuristics, so finding an acceptable result does not prove a global optimum.

**Recall check:** if design A uses less cell area but cannot route within its core, while design B is slightly larger and meets timing after routing, which one actually satisfies the specification? Explain why the answer requires physical implementation evidence, not just the synthesis area report.

[Previous: Day 01](Day%2001.md) · [Next: Day 03](Day%2003.md)
