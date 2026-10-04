# Source coverage and depth review

[Master index](../README.md) · [Every original handwritten page](Handwritten%20Index.md) · [Questions and corrections](Questions.md)

Updated on **4 October 2026**, through Kapil's reported completion of **Week 12**. All **128 readable source pages** have page-to-explanation mappings, and all **54 course items**, including tutorials, have lesson sections. The October continuation adds 68 source pages and 22 course items after Constraints I. Nine six-lesson study blocks are complete. This review re-examines every notebook page and the complete reading collection.

## Review by day

| Day | Completed lessons | Handwritten sources | Source pages | PDF pages | Depth checked in the explanations |
|---|---|---|---:|---:|---|
| [01](../Daily%20Notes/Day%2001.md) | 01–06 | Part 1, PDF pages 1–16 | 16 | 65 | Layer stack and lithography sequence; mask/wafer/die questions; design styles and cost break-even; communication-aware hardware/software partitioning; HLS scheduling, latency and throughput; setup/hold budgets; library versus instance pins; synthesis and mapping. |
| [02](../Daily%20Notes/Day%2002.md) | 07–12 | Part 1, pages 17–24; Part 2, pages 1–4 | 12 | 66 | Physical-input roles; floorplan, PDN, placement, CTS and routing; verification versus manufactured-device test; activating/observing faults and yield; mask preparation, OPC and overlay; Tcl substitution; four-state values, widths, z/? behavior, edges, functions/tasks and blocking/nonblocking timelines. |
| [03](../Daily%20Notes/Day%2003.md) | 13–18 | Scan A, pages 1–14 | 14 | 40 | Testbench checking and coverage limits; event-region trace and races; parsing versus elaboration; ports/parameters; case/casez and latch inference; sharing/speculation; constant and strength-reduction limits; cube/ON/OFF/DC reasoning; PI/EPI/RPI/SPI; restored prime chart, minimum-cover proof and heuristic operations. |
| [04](../Daily%20Notes/Day%2004.md) | 19–24 | Scan A, pages 15–21 | 7 | 28 | Factoring and literal-count correction; network transformations and local don't-cares; cube-graph question; state equivalence and encoding; signed-range/error-finding margin notes; Shannon cofactors and ROBDD reduction/order; SOP/CNF witnesses, BCP, branch conflicts and UNSAT; reachability versus bounded model checking. |
| [05](../Daily%20Notes/Day%2005.md) | 25–30 | Scan B, pages 1–8 | 8 | 26 | Equivalence correspondence; Liberty units, arcs, slew/load and interpolation; setup/hold arrival inequalities and slack signs; frequency and hold repair; signed pin-relative requirements; GBA/PBA correlation; MMMC coverage, uncertainty and early/late OCV. |
| [06](../Daily%20Notes/Day%2006.md) | 31–36 | Scan B, pages 9–11; Scan C, pages 1–12 | 15 | 42 | Clock/SDC modeling; external input/output delay signs; mapped-cell polarity and timing; late-input rewiring, Shannon decomposition, buffering and retiming with state alignment. |
| [07](../Daily%20Notes/Day%2007.md) | 37–42 | Scan C, pages 13–24; Scan D, pages 1–4; ATPG notebook | 17 | 40 | Switching/internal/leakage power; DVFS energy; power gating and retention; glitch-free clock enable; scan bit ordering/cost; activation, propagation, backtracking and redundancy proofs. |
| [08](../Daily%20Notes/Day%2008.md) | 43–48 | Scan D, pages 5–21 | 17 | 41 | LFSR recurrence/aliasing; implantation and BEOL; wire RC/crosstalk; interface timing budgets; eligible-area utilization; macro halos/orientations; PDN, IR, transient droop, decoupling and EM. |
| [09](../Daily%20Notes/Day%2009.md) | 49–54 | Scan D, pages 22–24; Scan E, pages 1–19 | 22 | 55 | HPWL/density/legalization; scan reordering/ECO spares; buffered clock wire; latency/skew/meshes; useful-skew setup and hold; global/detailed routing; fill, extraction, DRC/ERC/LVS and final signoff. |

The [handwritten index](Handwritten%20Index.md) provides the individual 128 page-to-explanation mappings and full-resolution originals. Shared pages have multiple explanation links where their subjects cross lessons. A-17's upper don't-care section belongs to Lesson 19 and its FSM section to Lesson 20; A-21's upper ROBDD section belongs to Lesson 21 and its SAT section to Lesson 23. The full source pages remain intact.

Some tutorials and lectures have no separate handwritten page in these uploads. Their sections use lecture evidence and additional explanation: Unix (05), Bambu (14), Icarus (18), Yosys synthesis (22), model checking (24), equivalence (25), technology libraries (26), Yosys optimization (27) and OpenSTA (31). A lack of handwriting is not treated as a missing completed lesson. Tcl occupies a short section on Part 2 page 2 and has a full tutorial explanation.

## Details strengthened in this review

- [A-13 and A-14](../Daily%20Notes/Day%2003.md#a-13-the-prime-implicants-of-ab--abc--bc): expanded the PI/EPI/RPI/SPI shorthand and restored the partial chart from the official lecture-material slide. The notes derive the two three-term minimum covers, distinguish an absorbed nonprime term from an RPI, explain Quine's theorem, and describe expand/reduce/reshape/irredundant heuristic steps. The restored chart is explicitly identified as a lecture-source annotation.
- [A-17 cube question](../Daily%20Notes/Day%2004.md#a-17-upper-section-controllability-and-observability-dont-cares): explained why a product term represents a cube and how that assignment graph differs from a graph of circuit dependencies.
- [A-17 margin notes](../Daily%20Notes/Day%2004.md#margin-notes-signed-integers-and-finding-errors): corrected the signed lower bound, reconciled the two alternative state encodings, and connected finding an error to the first simulation mismatch or a formal counterexample.
- [A-21 witnesses](../Daily%20Notes/Day%2004.md#a-21-sat-unsat-cnf-and-robdd-scope): evaluated the written 001/101 SOP witnesses and added a complete forced-contradiction example to distinguish UNSAT from one failed decision branch.
- [B-04 signed requirements](../Daily%20Notes/Day%2005.md#b-04-derive-the-skew-signs-before-memorizing-them): derived negative external setup/hold values from a simplified internal sampling model, with explicit assumptions and numeric examples.
- Part 1 page 19: corrected the [handwritten index](Handwritten%20Index.md) topic label to clock gating.

## Notebook depth iteration

The 4 October pass adds **26 worked explanations** beside the relevant source discussions. Each develops the mechanism, identifies assumptions and gives a trace, calculation or counterexample that the reader can reproduce. Earlier worked derivations and source corrections remain in place.

| Day | Added explanations | New reasoning to reproduce |
|---|---:|---|
| [01](../Daily%20Notes/Day%2001.md) | 2 | Carry wafer yield through shipped-unit cost and break-even volume; keep two transactions separate while sharing an adder. |
| [02](../Daily%20Notes/Day%2002.md) | 2 | Compare bit merging with procedural selection for an unknown mux select; change the RHS during a delay to expose when sampling occurs. |
| [03](../Daily%20Notes/Day%2003.md) | 2 | Repair the signed divide-by-four/shift replacement for negative values; test cube expansion against every care assignment. |
| [04](../Daily%20Notes/Day%2004.md) | 2 | Count equality-BDD nodes for interleaved and grouped orders; strengthen an invariant when an unreachable state defeats induction. |
| [05](../Daily%20Notes/Day%2005.md) | 2 | Substitute a negative pin-relative hold requirement without clamping it; find setup and hold failures in different timing scenarios. |
| [06](../Daily%20Notes/Day%2006.md) | 3 | Make a four-cycle timing exception agree with the real capture schedule; include upstream load in an upsizing decision; align a retimed mux's select with its data. |
| [07](../Daily%20Notes/Day%2007.md) | 3 | Trace a low-transparent clock-gating latch; count capture, overlapped scan load/unload and final unload edges; explain what a masked response can establish. |
| [08](../Daily%20Notes/Day%2008.md) | 5 | Construct a signature collision; separate coupled-voltage amplitude from sampling; distinguish placement space and routing capacity; transform macro pins with the macro outline; calculate capacitive, ESR and ESL droop. |
| [09](../Daily%20Notes/Day%2009.md) | 5 | Preserve test bit order after scan reordering; prove the skew-cycle constraint; calculate track pitch for via landing; follow the topology in an Elmore estimate; select a hold ECO within the setup budget. |

The final-week chapters also retain the detailed course explanations: scan activation/propagation/backtracking, long-wire repeaters, source-to-sink latency and signed pair skew, useful-skew setup/hold tradeoffs, routing demand/capacity, pin/via legality, metal fill and extraction, and the distinct geometry, connectivity, timing and supply checks at signoff.

## Lecture and source evidence

The continuation through Lesson 54 was reviewed in Chrome using the official NPTEL outline, selected lecture segments, captions and actual player frames. Its 22 caption exports remain local review material. The continuation adds 26 captured frames across Lessons 33–54; the maintained capture register now contains 47 reviewed frames. Other earlier course captures retain their timestamps in the [source register](Sources.md). Four official Week 12 decks are preserved for CTS, routing, signoff and Tutorial 12.

Every complete handwritten page has a page identity, full-resolution image, hash and explanation mapping. Original PDF positions, handwritten numbers and exported note-page numbers are kept distinct. Part 1/2 topical crops remain useful beside the corresponding discussion; their complete originals are accessible through the page index.

## Repository maintenance

The [resource guide](README.md) explains the roles of editable notes, reading PDFs, source images, raw uploads, examples and tools. Builders and PDF checks stay in `tools/pdf`; historical source-import helpers live in `tools/sources` and require an explicit historical-import flag. Study-model checks live in `examples`. Folder READMEs document normal rebuild steps and dependencies. Generated QA, temporary compilation products, raw later uploads and bundled dependencies are ignored by Git.

The [handwritten inventory](sources/handwritten-inventory.json) makes page counts and image hashes reviewable. The collection checker validates all available raw originals locally; a published checkout can validate every page image and mapping without the six ignored later PDFs. Strict local-original and published-material modes are documented in the [maintenance workflow](tools/pdf/README.md).

## Verification of the final exports

The nine daily PDFs contain **403 pages**, **255 figures**, **34 code blocks** and **344 heading bookmarks**. Source paragraphs, complete code, figures, contents destinations, supporting-file links and all **403 footer returns** pass the PDF checks. The two reference PDFs contain a further **8 pages**; the terminology guide has 87 terms. Their links into the daily PDFs and their internal destinations pass the reference check. Automated geometry checks report no issues.

All **403 daily pages** and **8 reference pages** were rendered and visually inspected after the final rebuild. The review checks formulas, table alignment, figure readability, lecture captions, code, contents, references and page breaks. Every original notebook page was inspected in legible source contact sheets. The local visual-review record binds these observations to the final PDF hashes. Sparse pages occur where a complete source image needs a new page; the images remain readable.

All four [executable study checks](examples/README.md) pass. They compile the Verilog examples, execute Tcl, enumerate the small Boolean and state models, independently construct covers and ROBDDs, and recompute the timing, scan, signature and physical calculations. The new signed arithmetic is checked for all 256 eight-bit values; the unknown-select example covers 1,024 combinations. The ATPG checker compares the good and faulty functions of the notebook and reconvergent examples.

The [collection check](tools/pdf/check_collection.py) validates all 54 lesson identities, all 128 source-page mappings/image hashes, all available original PDFs, capture hashes and maintained Markdown paths/anchors. These checks establish the stated teaching cases, source coverage and navigation. Handwriting interpretation and explanation depth are established by the content review. No complete local synthesis, OpenSTA, OpenROAD or foundry signoff run is claimed.

## Source limits

The earlier upload `Data/Scan-Empty-Upload.pdf` has **zero bytes** and no recoverable pages. The readable inventory is Part 1 (24), Part 2 (4), Scans A/B (21/11), Scans C/D/E (24/24/19) and the digital ATPG notebook (1), totaling 128. Scan E contains 19 PDF pages rather than the initial estimate of 11.

Some small K-map sketches on A-13 lack sufficient variable/function labels to verify their handwritten counts. Their source images remain intact, and the notes identify what information would be needed. Restored lecture-source annotations are identified explicitly. An incomplete diagram or unclear formula is not treated as a verified original result.

The completed boundary remains **Day 09, Lesson 06 of the day, course Lesson 54: Week 12 complete**.
