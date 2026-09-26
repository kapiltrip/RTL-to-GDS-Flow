# Day 08 — Overview of VLSI Design Flow V — Verification and test

[Course index](README.md) · Week 2 · [Lecture video](https://www.youtube.com/watch?v=g6ElOGlF3bs) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [Verification simulation and formal methods](#verification-simulation-and-formal-methods)
- [Timing and physical verification](#timing-and-physical-verification)
- [Defects faults and test patterns](#defects-faults-and-test-patterns)
- [Yield fault coverage and escapes](#yield-fault-coverage-and-escapes)
- [Automatic test equipment and design for test](#automatic-test-equipment-and-design-for-test)

## Verification simulation and formal methods

![Compare a design response against the expected response for the same stimulus](images/Day%2008/01-simulation.png)

*Video frame: [9:05](https://www.youtube.com/watch?v=g6ElOGlF3bs&t=545s). Compare a design response against the expected response for the same stimulus*


**Design verification** checks whether a design meets its specified behavior and requirements. **Manufacturing test** checks fabricated devices for faults and acceptance criteria. Verification can find a logic error shared by every chip made from a design; manufacturing test can reject an individual die affected by a fabrication defect. Design for test prepares the design so that those later tests are effective.

In **simulation**, a simulator evaluates the design under supplied input events. A testbench applies stimulus and checks the observed response against an expected result or reference model. Stimulus includes ordering and time, not just an unordered list of zeros and ones. A sequential design's output can depend on earlier inputs and reset history.

![Kapil’s handwritten notes — Part 1, PDF page 20, verification portion](images/Day%2008/h01-verification.jpg)

*Handwritten source: Part 1, PDF page 20, verification portion.*


Your two-branch drawing is a useful verification structure: apply equivalent transactions to the implementation and a **golden/reference model**, align their outputs in time, then compare. A mismatch identifies a discrepancy; debugging determines whether the implementation, testbench, reference model, or specification is wrong. A reference model is not correct merely because it is called “golden.”

Passing a finite collection of simulation tests establishes agreement for those executed scenarios. For $n$ independent binary inputs, a combinational truth table already has $2^n$ assignments; stored state and input sequences make sequential verification much larger. Coverage measures what was exercised, but a high coverage number does not alone prove correct behavior.

**Formal property checking** tries to prove stated properties under explicit assumptions. A safety property might say that conflicting traffic movements are never both green. A liveness property might say an accepted request eventually receives a grant; that requires suitable assumptions about the environment and fairness. A successful proof covers the modeled cases allowed by those assumptions. An inconclusive proof is neither a pass nor a demonstrated design failure.

**Equivalence checking** compares two representations, such as RTL and a synthesized netlist. The lecture introduces combinational equivalence checking across transformations. Designs whose state encoding, pipeline latency, or reset behavior changes may require additional correspondence information or sequential equivalence techniques. Equivalence to an incorrect reference preserves that error, so the original specification-to-RTL verification remains necessary.

## Timing and physical verification

![Physical verification complements functional and timing checks](images/Day%2008/02-physical-checks.png)

*Video frame: [25:42](https://www.youtube.com/watch?v=g6ElOGlF3bs&t=1542s). Physical verification complements functional and timing checks*

Physical verification asks whether the manufactured geometry can implement the intended circuit under the selected technology rules. DRC checks geometry, LVS compares extracted devices and connections with a reference, and ERC checks electrical rules. Timing analysis answers a separate question: whether signals can arrive and remain stable when required.

![Kapil’s handwritten notes — Part 1, PDF page 21](images/Day%2008/h02-signoff.jpg)

*Handwritten source: Part 1, PDF page 21.*


**Static timing analysis (STA)** evaluates timing paths using the netlist, cell models, interconnect estimates or extracted parasitics, clocks, and constraints. “Static” means that it does not require an explicit functional stimulus sequence to calculate each path's timing. It checks setup, hold, and other relevant requirements across chosen modes and corners.

Your phrase “considers worst-case behavior” should be read **within the modeled conditions and constraints**. A passing report cannot compensate for a missing clock, incorrect exception, unmodeled operating condition, or wrong library. Pessimistic modeling can create conservative reports; incomplete modeling can still hide real problems. The setup budget in [Day 04](Day%2004.md#paths-and-the-clock-period-budget) shows the components of one check.

| Check | Main question | What it does not establish by itself |
|---|---|---|
| DRC: design rule checking | Do geometric features obey the selected process rule deck? | Correct algorithm or complete electrical behavior |
| LVS: layout versus schematic | Does extracted layout connectivity and device information match the intended reference? | All timing requirements or complete system functionality |
| ERC: electrical rule checking | Are specified electrical-connection and usage rules obeyed? | Every possible physical failure |
| STA | Do modeled paths meet temporal constraints in the analyzed scenarios? | Functional correctness |
| RTL/constraint/netlist rule checks | Are suspicious constructs, conflicts, missing intent, or illegal structures present? | A proof of all design requirements |

Your LVS wording “functionally equal” is understandable, but the concrete check compares extracted devices/connectivity against a reference under tool rules. It is not the same task as proving a high-level algorithm. DRC rules are technology-specific. ERC content varies by tool and rule deck; shorts and opens can also be exposed through connectivity comparison. These checks overlap, but their purposes should remain distinct.

## Defects faults and test patterns

![Kapil’s handwritten notes — Part 1, PDF page 22](images/Day%2008/h03-defects.jpg)

*Handwritten source: Part 1, PDF page 22.*


A **defect** is a physical imperfection. A **fault model** is an abstract representation of a possible incorrect circuit behavior caused by defects. A **failure** is an observed violation of required behavior. One physical defect can have several effects, and one fault model can abstract several different defects.

In your example, a short to ground can be modeled as a **stuck-at-0 fault** on a line. To detect that fault, a test must both excite it and propagate its effect to an observable point. If a good line would also be 0 under the chosen input, the short cannot be distinguished by that observation. If the good value is 1 but downstream logic masks it, the fault still escapes that test.

For a simple AND gate $y=a\land b$, testing an `a` input stuck at 0 requires setting `a=1` and `b=1`: the good output is 1 and the faulty output is 0. Setting `b=0` masks the difference. This illustrates **controllability** and **observability**, the two central practical obstacles that test structures help address.

Process variation, contamination, alignment error, and other mechanisms can affect manufactured structures. Optical distortion is a pattern-fidelity problem addressed through process and mask techniques; an electrical manufacturing test is not a microscope inspecting every rounded corner. If a distortion creates an electrically relevant failure, suitable electrical tests may detect its consequence. An inconsequential geometric imperfection need not fail an electrical acceptance test.

## Yield fault coverage and escapes

![Yield depends on die area, defect density, and defect clustering](images/Day%2008/03-yield.png)

*Video frame: [47:24](https://www.youtube.com/watch?v=g6ElOGlF3bs&t=2844s). Yield depends on die area, defect density, and defect clustering*

A yield model connects the fraction of acceptable dies with factors such as die area, relevant defect density, and defect clustering. Larger area usually exposes each die to more defect opportunities when the other factors are held fixed. The clustering parameter changes how those opportunities are distributed across dies; the model below makes those assumptions explicit.

![Kapil’s handwritten notes — Part 1, PDF page 23](images/Day%2008/h04-yield-coverage.jpg)

*Handwritten source: Part 1, PDF page 23.*


**Yield** is a fraction of manufactured units meeting specified goodness criteria at a stated stage. Your previous page's example is correct: 300 good dies out of 400 gives $300/400=75\%$. It does not imply that every mature process must exceed a single universal percentage; die area, design, process maturity, and acceptance criteria matter.

The clustered-defect yield model in the lecture is

$$
Y=\left(1+\frac{Ad}{\alpha}\right)^{-\alpha},\qquad Y_{\%}=100Y.
$$

Here $A$ is die area, $d$ is the relevant defect density per unit area, and $\alpha>0$ is a clustering parameter. The exponent applies to the **whole parenthesis**, a detail that is easy to lose in handwriting. $Ad$ must be dimensionless. This is a model fitted to a process and defect population, not an exact physical law for every yield mechanism.

For $Ad=1$, $\alpha=1$ gives $Y=1/2=50\%$; $\alpha=2$ gives $Y=(1.5)^{-2}\approx44.44\%$. As $\alpha$ becomes very large, this expression approaches $e^{-Ad}$, giving about 36.79% for $Ad=1$. Smaller positive $\alpha$ corresponds to stronger clustering in this model. The same number of defects concentrated on already-bad dies can leave more other dies untouched. Deliberately adding defects is not a yield-improvement strategy; the observation compares distributions at a stated defect density.

**Fault coverage** measures detected modeled faults divided by the relevant modeled-fault population, with the exact denominator stated by the report. A coverage figure depends on fault model, exclusions, and treatment of untestable faults. It is not the fraction of bad chips automatically detected in all circumstances. Even 100% stuck-at coverage does not cover every delay, analog, intermittent, or other unmodeled physical failure.

**Defect level** measures the fraction of bad units among units that passed test. Your 100-chip example assumes 90 good and 10 bad, and further assumes the test detects exactly 5 of those 10 bad units. It then passes 95 units, of which 5 are bad:

$$
DL=\frac{5}{95}\times10^6\approx52{,}632\ \text{parts per million}.
$$

The arithmetic is correct under that assumption. The shortcut “50% fault coverage means exactly half the bad chips are detected” is a teaching simplification, not a general equivalence. Real escape probability depends on the physical fault distribution, multiple faults per die, and the test set. The denominator is **95 passed chips**, not the original 100.

## Automatic test equipment and design for test

![Test quality affects which defective devices escape detection](images/Day%2008/04-ate.png)

*Video frame: [55:40](https://www.youtube.com/watch?v=g6ElOGlF3bs&t=3340s). Test quality affects which defective devices escape detection*

A test program screens manufactured devices by applying conditions and comparing responses. Its fault coverage describes a modeled fault population, while defect level describes bad devices among the devices that pass. The slide places those two quality measures side by side; they must not be treated as interchangeable percentages.

![Kapil’s handwritten notes — Part 1, PDF page 24, upper portion](images/Day%2008/h05-ate.jpg)

*Handwritten source: Part 1, PDF page 24, upper portion.*


**Automatic test equipment (ATE)** supplies test conditions and patterns, measures responses, and compares them with acceptance criteria. At wafer test, a probe interface makes electrical contact to die pads. Packaged devices are tested through a suitable package interface. The test program defines timing, stimulus, expected values, and measurements; a diagram showing a comparator is an abstraction of that larger process.

Your pass/fail drawing should read “passes the specified tests,” not “proved physically perfect.” Failed devices are screened out; test diagnosis and process feedback can identify systematic problems for future production. **Design for test (DFT)** adds structures and plans that improve access to internal state and observation, such as scan or built-in test in appropriate designs. Test-pattern generation and expected-response preparation occur before manufactured devices reach the tester.

The bottom line of your final handwritten page begins “Functional Verification — Simulation.” It is preserved in the source archive and its definition is covered in this chapter. The later dedicated simulation lecture remains outside this batch, as requested.

**Recall checks:** Can a design pass LVS but fail timing? Can an incorrect RTL and its correctly synthesized netlist be equivalent? Why is fault coverage not interchangeable with yield?

[Previous: Day 07](Day%2007.md) · [Next: Day 09](Day%2009.md)
