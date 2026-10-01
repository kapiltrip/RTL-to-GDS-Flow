# RTL-to-GDS flow map

[Master index](../README.md)

The NPTEL flow is iterative. Verification and timing analysis recur after transformations; they are not one-time final boxes. The current completed boundary is Constraints I.

| Stage | Purpose in one line | Deep notes |
|---|---|---|
| Specification | Define required function, performance and interfaces. | [Lesson 03](../Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) |
| Architecture and partition | Choose blocks and assign behavior to hardware/software. | [Lesson 03](../Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) |
| High-level synthesis | Schedule, allocate and bind operations into a datapath/controller. | [Lesson 14](../Day%2003.md#lesson-14-high-level-synthesis-using-bambu---tutorial-3) |
| RTL modeling | Specify bit-accurate combinational and sequential behavior. | [Lesson 11](../Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) |
| Functional verification | Exercise and check the modeled behavior; track coverage. | [Lesson 13](../Day%2003.md#lesson-13-functional-verification-using-simulation) |
| RTL synthesis | Parse, elaborate and lower RTL into an internal network. | [Lesson 15](../Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| Logic optimization | Transform equivalent functions and state implementations. | [Lesson 19](../Day%2004.md#lesson-19-logic-optimization---part-ii) |
| Technology mapping | Choose legal library implementations. | [Lesson 22](../Day%2004.md#lesson-22-logic-synthesis-using-yosys) |
| Formal checking | Compare representations or prove stated properties. | [Lesson 25](../Day%2005.md#lesson-25-formal-verification---iv) |
| Constraints and STA | Model requirements and analyze setup/hold and design rules. | [Lesson 32](../Day%2006.md#lesson-32-constraints-i) |
| Floorplanning and power | Arrange major blocks and supply distribution. | [Lesson 07](../Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| Placement | Assign cell locations under area, wire and congestion concerns. | [Lesson 07](../Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| Clock tree synthesis | Build clock distribution and evaluate its arrivals. | [Lesson 07](../Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| Routing | Create legal signal wires and vias. | [Lesson 07](../Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| Physical verification and closure | Check DRC/LVS, extracted timing and related requirements. | [Lesson 08](../Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| GDSII, masks, fabrication and package | Transfer geometric design data into manufactured chips. | [Lesson 09](../Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |

## Reading the hierarchy

```text
Behavior and requirements
  Specification → architecture → RTL
    Simulation and formal verification
    Synthesis
      Parse → elaborate → infer hardware
      Optimize → map to technology cells
        Constraints and timing analysis
Physical implementation
  Floorplan and power → place → distribute clocks → route
    Extract parasitics → timing/physical checks → iterate
Manufacturing handoff
  GDSII → masks → fabricate → test → package
```

Names indicate different objects: a module definition is reusable source, an instance is a particular occurrence, a net connects terminals, a timing arc models a propagation/check relationship, and a physical pin is geometry used for routing. Keeping those distinctions makes the flow diagram explainable.
