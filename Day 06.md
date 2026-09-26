# Day 06 — Overview of VLSI Design Flow III — Logic synthesis

[Course index](README.md) · Week 2 · [Lecture video](https://www.youtube.com/watch?v=3uujV3nJvNM) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [RTL plus libraries plus constraints](#rtl-plus-libraries-plus-constraints)
- [Library pins and instance pins](#library-pins-and-instance-pins)
- [Generic logic and technology mapping](#generic-logic-and-technology-mapping)

## RTL plus libraries plus constraints

![RTL selection and storage mapped into a mux and flip-flop](images/Day%2006/01-synthesis.png)

*Video frame: [9:38](https://www.youtube.com/watch?v=3uujV3nJvNM&t=578s). RTL selection and storage mapped into a mux and flip-flop*


**Logic synthesis** converts a synthesizable RTL description into a functionally equivalent network of available implementation cells while optimizing against constraints. It does not fabricate silicon or choose all final wire geometries. Its main output is a **netlist** describing instances and connectivity.

| Input | Role | Common representation |
|---|---|---|
| RTL | Intended state and combinational behavior | Verilog/VHDL source |
| Technology library | Available cell functions and characterized properties | Liberty `.lib` |
| Constraints | Clock requirements, external timing, loads, and other design intent | SDC and tool commands |

The same file extension `.v` may contain behavioral RTL or a structural gate-level netlist. Inspect the contents to determine its abstraction. The synthesis goal is not merely to produce syntactically legal Verilog: the chosen cells must implement the intended behavior and meet the modeled constraints.

The lecture uses a mux feeding a flip-flop. This complete equivalent teaching version keeps the behavior clear:

```verilog
module select_register (
    input  wire a,
    input  wire b,
    input  wire select,
    input  wire clk,
    output reg  out
);
    wire y;
    assign y = select ? b : a;
    always @(posedge clk)
        out <= y;
endmodule
```

`assign` describes the mux continuously. The edge-sensitive process describes output storage. There is no reset in this example, so simulation starts with `out` unknown until a defined value is captured. A technology library might provide a mux cell and a D flip-flop, or the mapper might implement the mux using an equivalent combination of gates.

## Library pins and instance pins

![A cell definition can have multiple independently named instances](images/Day%2006/02-pins.png)

*Video frame: [25:48](https://www.youtube.com/watch?v=3uujV3nJvNM&t=1548s). A cell definition can have multiple independently named instances*

A library describes reusable cell types. A netlist contains particular instances of those types and nets connecting their pins. Read the figure by first identifying each cell type, then its instance name, and finally the pin being connected. This distinction prevents two pins named `A` on different gates from being mistaken for one connection.

![Kapil’s handwritten notes — Part 1, PDF page 15](images/Day%2006/h01-pins.jpg)

*Handwritten source: Part 1, PDF page 15.*


### Your question: what is a library pin versus an instance pin?

A **library cell** is a reusable definition, such as a two-input AND gate called `AN2`. Its **library pins** `A`, `B`, and `Y` describe the interfaces and associated properties of that cell type. An **instance** is one use of that cell in a design. If `AN2` is instantiated as `I1` and `I2`, then `I1/A` and `I2/A` are different physical/logical connection points, although both refer to the library definition's `A` pin.

| Name | Meaning |
|---|---|
| `AN2` | Library cell type |
| `AN2/A` | Pin A of the library definition, using explanatory notation |
| `I1` | One instance of AN2 |
| `I1/A` | Pin A on that particular instance |
| `in1` | A top-level input port, if declared on the design boundary |
| `n1` | A net connecting a set of pins and/or ports |

The slash is the course's naming convention; a tool may use another separator or a hierarchical path. Instance names are unique within their scope, while a complete hierarchical path identifies an instance across the design. Repeated local pin names such as `A` therefore need instance context.

A **port** belongs to a module/design boundary. A **pin** in this synthesis vocabulary belongs to a cell or instance. A **net** is a connection, not a gate. A net can have one driver and several loads, giving fanout. Direction is defined relative to the owner: an input port brings a signal into the top design, while an output pin of an internal cell can drive a net inside that design.

Your `.lib`, `.sdc`, and `.v` triangle is a useful reminder: changing constraints or the cell library can change the result even when the RTL is unchanged. Relaxing timing may allow smaller/slower cells; tightening timing can require faster cells or a different logic structure. Unachievable constraints do not force the tool to create impossible hardware.

### Timing arcs slew load and operating corners

A **timing arc** describes a timing relationship between specified pins of a cell. For an AND gate, an `A`-to-`Y` propagation arc describes the output response to a relevant input transition, under conditions that permit that transition to propagate. The `B`-to-`Y` arc is a separate relationship. For a flip-flop, clock-to-Q is a propagation relationship; setup and hold are timing-check relationships between data and clock. A timing arc therefore need not mean that data flows directly between its two named pins.

**Slew**, or transition time, measures how long a signal takes to cross specified voltage thresholds. It is different from **propagation delay**, which measures the time between reference crossings at the input and output. A slow input edge and a late output edge are related effects, but they are not the same measurement.

**Capacitive load** is the capacitance the output must drive, including connected input pins and interconnect. Many cell models tabulate output delay and transition against input slew and output load, with separate rise/fall behavior. Consequently, “this gate takes 50 ps” is incomplete without its arc, input transition, loading, and operating conditions. Increasing load commonly slows an output; a stronger cell may drive it faster while presenting more input capacitance to the preceding stage.

For an actual example, the [SKY130 medium-speed library's table templates](https://foss-eda-tools.googlesource.com/skywater-pdk/libs/sky130_fd_sc_ms.git/+/refs/tags/v0.0.2/timing/sky130_fd_sc_ms__common.lib.json) name `input_net_transition` and `total_output_net_capacitance` as delay-table variables. The same file distinguishes 50% propagation-delay reference thresholds from 20%–80% slew thresholds. Those values belong to that library; inspect the chosen library before interpreting another timing report.

An operating **PVT corner** specifies process assumptions, supply voltage, and temperature. Different corners can produce different delays and leakage. Which corner is limiting depends on the check and technology; “hot is always worst for every check” is not a general rule.

For instance, `tt_025C_1v80` in the documented SKY130 configuration means typical NMOS/PMOS process assumptions, 25 °C, and 1.80 V. The process label describes a characterization assumption, not the manufacturing date or a physical corner of the die. [LibreLane's timing-corner guide](https://librelane.readthedocs.io/en/latest/usage/timing_corners.html) also distinguishes these cell PVT corners from interconnect corners used to model wire parasitics.

Keep the information sources separate:

| Data | Question it helps answer |
|---|---|
| Liberty `.lib` | What function and characterized timing/power behavior does this cell have? |
| Netlist `.v` | Which instances exist, and how are their pins connected? |
| SDC constraints | What clocks, external timing, and timing intent must the implementation satisfy? |
| LEF physical abstract | What placement dimensions, pin shapes, and routing obstructions must physical tools respect? |
| SPEF parasitics | What modeled interconnect resistance and capacitance affect the implemented nets? |

For concrete format context, see [OpenSTA's accepted timing inputs](https://github.com/The-OpenROAD-Project/OpenSTA#parallax-static-timing-analyzer) and [SKY130's file-type descriptions](https://skywater-pdk.readthedocs.io/en/main/contents/file_types.html). A LEF pin shape alone does not provide a timing arc, and a logic netlist alone does not provide extracted wire parasitics.

## Generic logic and technology mapping

![Technology mapping chooses real library cells and drive strengths](images/Day%2006/03-mapping.png)

*Video frame: [38:43](https://www.youtube.com/watch?v=3uujV3nJvNM&t=2323s). Technology mapping chooses real library cells and drive strengths*

Technology mapping replaces technology-independent logic with implementations available in the selected library. The available cells have real area, timing, drive, and power properties. Mapping and subsequent optimization therefore choose more than a Boolean symbol: they choose realizations that must meet the supplied constraints.

![Kapil’s handwritten notes — Part 1, PDF page 16](images/Day%2006/h02-synthesis.jpg)

*Handwritten source: Part 1, PDF page 16.*


### Your question: is there a defined set of generic logic gates?

There is no single universal internal gate set required of every synthesis tool. A tool may represent intermediate logic using Boolean operators, muxes, arithmetic operators, flip-flops, or a more specialized internal graph. “Generic” means that the representation has not yet committed to a particular characterized cell implementation. A generic inverter specifies logical inversion; a library inverter adds a concrete implementation and characterized properties.

The lecture's synthesis sequence is:

1. **Parse and elaborate RTL:** interpret syntax, parameters, hierarchy, widths, and connectivity; derive hardware behavior.
2. **Create and simplify generic logic:** infer operators and storage, propagate constants, remove unused logic, and simplify Boolean structure.
3. **Technology map:** cover the required logic with cells available in the target library.
4. **Optimize the mapped implementation:** resize, restructure, buffer, or otherwise improve timing, area, and power while maintaining the required function.

For instance, $ab+ac=a(b+c)$ is a Boolean factoring opportunity. Whether the factored form is physically better depends on available complex gates, loading, fanout, and timing. The smallest number of drawn generic gates need not map to the smallest or fastest real implementation.

A stronger inverter can drive a larger load with less output delay, but its input may load the preceding stage more heavily. The mapper must consider the path and network, not a cell in isolation. Generic gate count provides a rough structural cost; it is not an accurate physical area or power number. Mapped cell models improve estimates, but pre-route wire estimates still differ from extracted post-route parasitics.

**Equivalence checking** verifies that intended behavior survives transformation. Timing analysis checks the modeled temporal constraints. Neither check replaces the other. The resulting netlist proceeds into physical implementation, with test-related transformations included where the flow requires them.

[Previous: Day 05](Day%2005.md) · [Next: Day 07](Day%2007.md)
