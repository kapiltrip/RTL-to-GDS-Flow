# Source coverage and depth review

[Master index](../README.md) · [Every original handwritten page](Handwritten%20Index.md) · [Questions and corrections](Questions.md)

Reviewed on **1 October 2026**, through the reported completion of Week 8 Constraints I. The review compared all **60 readable handwritten source pages** with their daily explanations, including margin questions, mixed-topic pages, formulas and worked examples. All 32 completed course items have a lesson section. Day numbers remain six-lesson study blocks: five complete blocks and two lessons in Day 06.

## Review by day

| Day | Completed lessons | Handwritten sources | Pages | Depth checked in the explanations |
|---|---|---|---:|---|
| [01](../Day%2001.md) | 01–06 | Part 1, PDF pages 1–16 | 16 | Layer stack and lithography sequence; mask/wafer/die questions; design styles and cost break-even; communication-aware hardware/software partitioning; HLS scheduling, latency and throughput; setup/hold budgets; library versus instance pins; synthesis and mapping. |
| [02](../Day%2002.md) | 07–12 | Part 1, pages 17–24; Part 2, pages 1–4 | 12 | Physical-input roles; floorplan, PDN, placement, CTS and routing; verification versus manufactured-device test; activating/observing faults and yield; mask preparation, OPC and overlay; Tcl substitution; four-state values, widths, z/? behavior, edges, functions/tasks and blocking/nonblocking timelines. |
| [03](../Day%2003.md) | 13–18 | Scan A, pages 1–14 | 14 | Testbench checking and coverage limits; event-region trace and races; parsing versus elaboration; ports/parameters; case/casez and latch inference; sharing/speculation; constant and strength-reduction limits; cube/ON/OFF/DC reasoning; PI/EPI/RPI/SPI; restored prime chart, minimum-cover proof and heuristic operations. |
| [04](../Day%2004.md) | 19–24 | Scan A, pages 15–21 | 7 | Factoring and literal-count correction; network transformations and local don't-cares; cube-graph question; state equivalence and encoding; signed-range/error-finding margin notes; Shannon cofactors and ROBDD reduction/order; SOP/CNF witnesses, BCP, branch conflicts and UNSAT; reachability versus bounded model checking. |
| [05](../Day%2005.md) | 25–30 | Scan B, pages 1–8 | 8 | Equivalence correspondence; Liberty units, arcs, slew/load and interpolation; setup/hold arrival inequalities and slack signs; frequency and hold repair; signed pin-relative requirements; GBA/PBA correlation; MMMC coverage, uncertainty and early/late OCV. |
| [06](../Day%2006.md) | 31–32 | Scan B, pages 9–11 | 3 | OpenSTA inputs and report interpretation; constraint categories and design-object selection; primary/generated-clock relationship and duty cycle; source/network latency; jitter versus skew versus uncertainty; setup/hold uncertainty examples; transition versus period. |

The [handwritten index](Handwritten%20Index.md) provides the individual 60 page-to-explanation mappings and full-resolution originals. Shared pages have multiple explanation links where their subjects cross lessons. A-17's upper don't-care section belongs to Lesson 19 and its FSM section to Lesson 20; A-21's upper ROBDD section belongs to Lesson 21 and its SAT section to Lesson 23. The full source pages remain intact.

Some tutorials and lectures have no separate handwritten page in these uploads. Their sections use lecture evidence and additional explanation: Unix (05), Bambu (14), Icarus (18), Yosys synthesis (22), model checking (24), equivalence (25), technology libraries (26), Yosys optimization (27) and OpenSTA (31). A lack of handwriting is not treated as a missing completed lesson. Tcl occupies a short section on Part 2 page 2 and has a full tutorial explanation.

## Details strengthened in this review

- [A-13 and A-14](../Day%2003.md#a-13-the-prime-implicants-of-ab--abc--bc): expanded the PI/EPI/RPI/SPI shorthand and restored the partial chart from the official lecture-material slide. The notes derive the two three-term minimum covers, distinguish an absorbed nonprime term from an RPI, explain Quine's theorem, and describe expand/reduce/reshape/irredundant heuristic steps. The restored chart is explicitly identified as a lecture-source annotation.
- [A-17 cube question](../Day%2004.md#a-17-upper-section-controllability-and-observability-dont-cares): explained why a product term represents a cube and how that assignment graph differs from a graph of circuit dependencies.
- [A-17 margin notes](../Day%2004.md#margin-notes-signed-integers-and-finding-errors): corrected the signed lower bound, reconciled the two alternative state encodings, and connected finding an error to the first simulation mismatch or a formal counterexample.
- [A-21 witnesses](../Day%2004.md#a-21-sat-unsat-cnf-and-robdd-scope): evaluated the written 001/101 SOP witnesses and added a complete forced-contradiction example to distinguish UNSAT from one failed decision branch.
- [B-04 signed requirements](../Day%2005.md#b-04-derive-the-skew-signs-before-memorizing-them): derived negative external setup/hold values from a simplified internal sampling model, with explicit assumptions and numeric examples.
- Part 1 page 19: corrected the [handwritten index](Handwritten%20Index.md) topic label to clock gating.

## Formal reading edition and second depth pass

All six PDFs now use concise lecture/source captions and formal technical prose. Repeated descriptions of left/right comparisons, crop placement and image-click instructions have been removed. A single introductory navigation sentence remains. The handwritten evidence, lecture timestamps, original page identities and complete code are retained. The daily Markdown files supply all lesson content; the builder only supplies layout, references and navigation.

- Day 01: replaced conversational speaking scripts with formal applications, including resist polarity, break-even sensitivity to a respin, Amdahl's limiting speedup with communication overhead, an HLS resource bound, shell output/exit-status interpretation and a load-dependent synthesis-cell choice.
- Day 02: added coupled setup/hold repair arithmetic, an outgoing-defect-level derivation, an overlay-spacing tolerance calculation, staged Tcl substitution, a full-width unsigned sum and a pipeline transaction trace.
- Day 03: linked requirements to counter checkers, derived parameterized-counter modulus, established the priority-case Boolean function and a counterexample to losing priority, derived speculation's arrival-time benefit and traced the wrap boundary.
- Day 04: supplied a don't-care fanout counterexample, a complete Moore-state partition-refinement exercise, an exact gate-to-CNF encoding and symbolic image/reachability reasoning tied to initial-state assumptions.
- Day 05: worked an unreachable-cutpoint mismatch, generalized the library-table interpolation, counted sharing/mux area under explicit assumptions and quantified common-clock-path pessimism.
- Day 06: decomposed a timing report into independent arrival/required accumulations, derived mixed-edge budgets from a non-50% waveform, worked a master-to-divided-clock path and derived cancellation of common source latency.

The expanded example checker exhaustively verifies the priority function, gate clauses, FSM refinement, cutpoint invariant and fanout example. It also recomputes the new numeric results, checks the reachability fixed point and executes the Tcl substitution cases. These are checks of the stated teaching models, not reports of an executed complete ASIC flow.

## Additional depth iteration

Each day now contains two further worked explanations beside the relevant source discussion:

- Day 01: derives a feedback-limited HLS initiation interval from an explicit schedule, then proves a NAND mapping by preserving inversion polarity.
- Day 02: traces the extra clock edge produced by a changing enable during the high phase, then demonstrates how Tcl lists preserve a filename containing spaces as one argument.
- Day 03: includes different input/output mux delays in the speculation comparison, then constructs an irredundant four-term cover that costs more than either three-term optimum.
- Day 04: counts ordinary ROBDD nodes for two variable orders of the same function, then derives every satisfying assignment of the handwritten CNF rather than stopping at one witness.
- Day 05: follows rising/falling polarity through sensitized timing arcs, then propagates earliest and latest arrivals separately to expose a passing setup check alongside a failing hold check.
- Day 06: calculates high/low pulse-width margins independently of period, then derives mixed-edge hold pairing from absolute events, including latency and uncertainty signs.

The checker independently enumerates the legal primes and all selections for the new cover, constructs and evaluates both ROBDDs, and exhaustively checks the Boolean mappings and CNF witnesses. It also executes the Tcl list example, reproduces the clock-gating event trace, and recomputes the recurrence, mux, arc, arrival, pulse-width and mixed-edge timing results. The final visual pass checks every exported page, with full-page inspection of the new tables, formulas and paragraph breaks. Original handwritten pages and captured lecture frames are unchanged.

The Chrome review also checks GitHub's rendered formulas. Set delimiters and product signs use named LaTeX commands so Markdown escape handling preserves the intended notation in both the web notes and the PDFs.

## What verification establishes

The content review checks whether the explanation develops the mechanism, assumptions, calculations and corrections suggested by the source. Page counts and word counts alone do not establish depth. The daily notes retain examples and recall questions so revision involves reproducing reasoning rather than only recognizing terminology.

The maintained collection checker now verifies all 60 original page identities, all four readable source-PDF page counts, their explanation links, complete new-page images, all 32 lesson identities, current progress and lecture-capture hashes. The PDF checker verifies retained paragraphs and code, contents/bookmark destinations, supporting-file links, image/footer navigation and page geometry. Rendered PDFs are inspected visually after rebuilding. Machine checks establish structure and exported-content coverage; interpreting handwriting and judging explanation depth remain part of the content review.

The small Boolean examples are checked exhaustively. For the restored chart, the example checker independently enumerates legal cubes and searches covers, verifying four primes and two minimum three-term covers. It also checks all assignments for the added UNSAT example. The executable Verilog/Tcl examples retain their stated checks. Tutorial command descriptions are not claims that a complete Yosys or OpenSTA flow has been run locally.

The six exported PDFs contain **235 pages**. Every one of their **161 source-figure rectangles** and **235 footer rectangles** has a verified link to contents, and all **222 retained heading bookmarks** point to their matching sections. All 26 code blocks and native paragraphs pass exported-content checks; page-geometry checks report no issues. The final PDFs are visually reviewed, including the revised charts, derivations and margin explanations.

## Source limits retained honestly

The third new upload, `Data/Scan-Empty-Upload.pdf`, has **zero bytes** and no recoverable pages. The readable inventory is Part 1 (24), Part 2 (4), Scan A (21) and Scan B (11), totaling 60. No content is inferred for the empty file.

Some small K-map sketches on A-13 lack sufficient variable/function labels to verify their handwritten counts. Their original images are preserved, and the notes explain what must be supplied before deriving counts. This uncertainty is kept visible. An unclear formula or incomplete diagram is not silently converted into a confident claim.

The completed boundary remains **Day 06, Lesson 02 of the day, course Lesson 32**. Constraints II is the next lesson and is not marked completed.
