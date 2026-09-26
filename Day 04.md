# Day 04 — Overview of VLSI Design Flow II

[Course index](README.md) · Week 1 · [Lecture video](https://www.youtube.com/watch?v=6_J-x1QfZs0) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [The implementation gap and IP reuse](#the-implementation-gap-and-ip-reuse)
- [Behavioral synthesis and its cost measures](#behavioral-synthesis-and-its-cost-measures)
- [Paths and the clock-period budget](#paths-and-the-clock-period-budget)
- [Three implementations of a plus b plus c](#three-implementations-of-a-plus-b-plus-c)

## The implementation gap and IP reuse

![Metadata supports integration of reusable IP blocks](images/Day%2004/01-ip-assembly.png)

*Video frame: [17:48](https://www.youtube.com/watch?v=6_J-x1QfZs0&t=1068s). Metadata supports integration of reusable IP blocks*


A functional specification says **what** computation must occur. RTL also commits to **when** operations occur relative to clock events and how state is stored. The difference is the **implementation gap**. Translating an untimed expression into RTL requires architectural choices: how many arithmetic units exist, which operations share them, where registers are placed, how inputs are accepted, and when outputs become valid.

The **datapath** contains arithmetic, logic, multiplexers, and data registers. The **control path** generates enables, selects, and state transitions that govern datapath operation. Both run as hardware. Writing lines one after another in a file does not automatically mean that the hardware executes them in separate clock cycles.

Three routes bridge the gap: manually write RTL, integrate existing IP, or use behavioral/high-level synthesis. A **system on chip (SoC)** integrates substantial system components such as processors, memory, accelerators, peripherals, and sometimes analog/RF blocks. A **reusable IP block** packages a design capability and the information needed to use it. “Pre-verified” does not remove the need to verify its configuration and integration in the new system.

![Kapil’s handwritten notes — Part 1, PDF page 11](images/Day%2004/h01-ip.jpg)

*Handwritten source: Part 1, PDF page 11.*


Your hardware/software/verification-IP categories describe different reusable deliverables. Hardware IP can implement a processor or interface; software IP can provide drivers; verification IP can generate protocol transactions and check responses. A driver is not a physical gate block, but it can be essential to operating the hardware correctly.

**Metadata** is structured information about the design: module identities, parameter values, ports, bus interfaces, address maps, registers, and configuration. A generator can use it to create connections, wrappers, register descriptions, or a verification environment. The lecture mentions IP-XACT, SystemRDL, XML, and spreadsheets. They do not all express the same information or offer identical guarantees.

Integration must resolve width, protocol, clock, reset, and power-domain compatibility. An 8-bit interface connected to a 16-bit interface may require a width adapter and a defined ordering of transfers. A **network on chip (NoC)** provides structured on-chip communication. It helps organize complex systems but adds its own latency, arbitration, buffering, and verification concerns; not every SoC requires a NoC.

## Behavioral synthesis and its cost measures

**Behavioral synthesis**, also called **high-level synthesis (HLS)**, converts an algorithmic description into a timed RTL architecture under constraints. Its input is more than the algorithm: it also needs resource and implementation models, target clock requirements, and constraints on area, latency, throughput, or power.

**Scheduling** assigns operations to control steps or cycles. **Allocation** chooses how many resources are available. **Binding** maps operations and stored values to particular resources and registers. These decisions interact: sharing one multiplier can reduce arithmetic area but introduce multiplexers, control, and longer scheduling intervals.

![Kapil’s handwritten notes — Part 1, PDF page 12](images/Day%2004/h02-hls.jpg)

*Handwritten source: Part 1, PDF page 12.*


Your diagram captures the algorithm + constraints + resource-library → RTL relationship. Separate three metrics carefully:

| Metric | Definition | Example |
|---|---|---|
| Latency | Time from an accepted input transaction to its valid result | 2 cycles at 5 ns per cycle = 10 ns |
| Initiation interval | Cycles between accepted independent transactions | An interval of 2 allows one new transaction every other cycle |
| Throughput | Results completed per unit time in steady state | With interval 2 at 200 MHz, at most 100 million results/s |

Register count and arithmetic-unit count provide an early area estimate. Physical wire length, congestion, buffering, and clocking remain uncertain until implementation. A resource-sharing solution can look small at RTL but collect so many signals around one unit that physical implementation becomes difficult. Generated RTL also needs verification against the original algorithm, including finite widths, overflow, signedness, and timing of inputs and outputs.

## Paths and the clock-period budget

![Launch and capture flip-flops connected by combinational logic](images/Day%2004/02-timing.png)

*Video frame: [32:14](https://www.youtube.com/watch?v=6_J-x1QfZs0&t=1934s). Launch and capture flip-flops connected by combinational logic*


A **path** is an ordered sequence of pins and connections along which a signal can propagate. A **combinational path** does not cross a state-holding element. Two flip-flops are **sequentially adjacent** when one can send data to the other through only combinational logic and interconnect. This is a connectivity relationship, not a statement that they sit next to one another on the die.

For a conventional single-cycle register-to-register path, the launch edge causes the first register's output to change. Data traverses logic and wire delay and must settle before the next capture edge by at least the receiving register's setup time. The lecture first approximates this using only maximum combinational delay. A more useful zero-skew setup budget is

$$
T_{\text{clk}}\ge t_{\text{cq,max}}+t_{\text{comb,max}}+t_{\text{setup}}+t_{\text{uncertainty}}.
$$

Here $t_{\text{cq,max}}$ is maximum clock-to-Q delay, $t_{\text{comb,max}}$ includes the logic and wires, and uncertainty reserves margin for specified clock effects. If capture clock arrival is later than launch clock arrival by $t_{\text{skew}}$, using that sign convention adds $t_{\text{skew}}$ to the available setup budget. Real STA also handles multiple clocks, exceptions, corners, and other checks.

![Kapil’s handwritten notes — Part 1, PDF page 13](images/Day%2004/h03-timing.jpg)

*Handwritten source: Part 1, PDF page 13.*


Your arrival-time expression is pointing in the right direction but needs a time reference. Measured from a launch clock event at time zero, data arrival is $t_{\text{cq}}+t_{\text{comb}}$. Required arrival is the capture-edge time **minus** setup time and applicable uncertainty. Setup slack is required arrival minus actual arrival; nonnegative slack meets that modeled check.

For example, with $t_{\text{cq}}=0.08$ ns, combinational delay $0.62$ ns, setup $0.10$ ns, and uncertainty $0.05$ ns, the minimum zero-skew period is $0.85$ ns, corresponding to approximately 1.176 GHz. These are illustrative values. Increasing the clock period helps this setup check; it does not generally fix a hold violation, which concerns data changing too soon around the same capture edge. A common zero-skew hold condition is $t_{\text{cq,min}}+t_{\text{comb,min}}\ge t_{\text{hold}}$ before adding the relevant margins.

The “next cycle” rule assumes an ordinary single-cycle path. Valid multicycle protocols require explicitly justified constraints; they cannot be assumed merely because a path is slow.

## Three implementations of a plus b plus c

![One adder reused over two cycles with multiplexers and feedback](images/Day%2004/03-resource-sharing.png)

*Video frame: [39:00](https://www.youtube.com/watch?v=6_J-x1QfZs0&t=2340s). One adder reused over two cycles with multiplexers and feedback*


The expression $y=a+b+c$ permits several architectures. For a fair comparison, define the bit widths, arithmetic behavior, and input protocol consistently.

| Architecture | Arithmetic resources | Result latency | Long combinational portion | New-input interval |
|---|---|---|---|---|
| Two cascaded adders and output register | 2 adders | 1 cycle | Approximately 2 adder delays | 1 cycle |
| Pipelined adders | 2 adders, additional data registers | 2 cycles | Approximately 1 adder delay per stage | 1 cycle after filling |
| One shared adder | 1 adder, muxes, data/control storage | 2 cycles | Approximately mux + adder | 2 cycles for this simple design |

The pipelined version must delay `c` appropriately so the second stage combines values belonging to the same transaction. That alignment register may be omitted in a simplified drawing whose inputs are held stable. The table describes the protocol explicitly rather than assuming that any two-register drawing is a correct streaming pipeline.

![Kapil’s handwritten notes — Part 1, PDF page 14](images/Day%2004/h04-sharing.jpg)

*Handwritten source: Part 1, PDF page 14.*


Your feedback drawing reuses one physical adder. In phase 0, the muxes select `a` and `b`, and the result register captures their sum. In phase 1, they select `c` and the saved sum, and the register captures the final result. With `a=2`, `b=3`, and `c=4`, the register becomes 5 after the first computing edge and 9 after the second. The first value is an intermediate result; a consumer must not mistake it for the completed transaction.

The toggle flip-flop creates alternating phases only if its initial phase is known. A practical block needs a reset or other defined initialization, a clear input-acceptance rule, and an output-valid indication. Inputs must remain valid when consumed or be captured into local registers. Without these details, the diagram illustrates resource sharing but is not a complete interface specification.

Area savings are conditional: the removed adder must save more than the added muxes, control, and registers cost. A shorter combinational path may permit a higher clock, but reduced initiation rate can still lower throughput. HLS chooses among these tradeoffs according to constraints and its available implementation models. The final design still needs synthesis and physical validation.

[Previous: Day 03](Day%2003.md) · [Next: Day 05](Day%2005.md)
