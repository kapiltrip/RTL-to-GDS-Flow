# RTL to GDS study notes

**Current position: Week 12 complete — Day 09, Lesson 06 of the day (course Lesson 54).** Updated from Kapil's reported progress on 3 October 2026. Tutorials count in the sequence; the study notes review demonstrations without claiming new laboratory runs.

Open [Daily Notes](Daily%20Notes/README.md) for the day-wise RTL-to-GDS notes or [PDFs](PDFs/README.md) for the reading collection. The two reference PDFs at the top level provide quick revision: [Full Forms](Full%20Forms.pdf) explains terminology, and [RTL to GDS Flow](RTL%20to%20GDS%20Flow.pdf) outlines the stages, their purpose and the NPTEL teaching sequence.

The references emphasize implementation theory, requirements and design artifacts, which carry over to a Synopsys workflow. Each daily PDF has clickable contents, hierarchical bookmarks and figure/footer links back to contents. Markdown figures return to their day index. Detailed mechanisms, original handwriting, lecture timestamps, corrections and worked applications remain together in the daily notes.

The allocation is **six lessons per study day**: `day = floor((lesson−1)/6)+1`. All 54 course lessons now occupy nine completed study blocks. Equal lesson counts do not imply equal video durations or study effort.

## Daily reading index

| Day | Lessons | Topic | PDF | Pages |
|---|---|---|---|---:|
| [Day 01](Daily%20Notes/Day%2001.md) | 01–06 | IC foundations and synthesis | [Read PDF](PDFs/Day%2001%20-%20IC%20Foundations%20and%20Logic%20Synthesis.pdf) | 65 |
| [Day 02](Daily%20Notes/Day%2002.md) | 07–12 | Physical design and Verilog | [Read PDF](PDFs/Day%2002%20-%20Physical%20Design%20and%20Verilog%20Foundations.pdf) | 66 |
| [Day 03](Daily%20Notes/Day%2003.md) | 13–18 | Simulation, synthesis and Boolean covers | [Read PDF](PDFs/Day%2003%20-%20Simulation%20Synthesis%20and%20Logic%20Optimization.pdf) | 40 |
| [Day 04](Daily%20Notes/Day%2004.md) | 19–24 | Multilevel optimization and formal methods | [Read PDF](PDFs/Day%2004%20-%20Multilevel%20Optimization%20and%20Formal%20Verification.pdf) | 28 |
| [Day 05](Daily%20Notes/Day%2005.md) | 25–30 | Equivalence, libraries and STA | [Read PDF](PDFs/Day%2005%20-%20Equivalence%20Libraries%20and%20Static%20Timing%20Analysis.pdf) | 26 |
| [Day 06](Daily%20Notes/Day%2006.md) | 31–36 | Constraints, mapping and timing optimization | [Read PDF](PDFs/Day%2006%20-%20OpenSTA%20and%20Clock%20Constraints.pdf) | 42 |
| [Day 07](Daily%20Notes/Day%2007.md) | 37–42 | Power, scan design and ATPG | [Read PDF](PDFs/Day%2007%20-%20Power%20Scan%20Design%20and%20ATPG.pdf) | 40 |
| [Day 08](Daily%20Notes/Day%2008.md) | 43–48 | BIST, physical foundations and chip planning | [Read PDF](PDFs/Day%2008%20-%20BIST%20Physical%20Foundations%20and%20Chip%20Planning.pdf) | 42 |
| [Day 09](Daily%20Notes/Day%2009.md) | 49–54 | Placement, clocks, routing and signoff | [Read PDF](PDFs/Day%2009%20-%20Placement%20Clocks%20Routing%20and%20Signoff.pdf) | 56 |

[Find handwritten pages](Resources/Handwritten%20Index.md) · [Corrections and doubts](Resources/Questions.md) · [Sources and timestamps](Resources/Sources.md) · [Study method](Resources/Study%20Guide.md) · [Coverage and depth review](Resources/Coverage%20Review.md)

[Week 7 and Week 8 practice questions](Resources/Week%2007%20and%2008%20-%20Practice%20Questions.md) · [Question-only worksheet PDF](PDFs/Week%2007%20and%2008%20-%20Practice%20Questions.pdf). All 20 assignment questions, their unmarked options and six source figures are included.

## Course lesson index

| Day | Week | Lesson and topic |
|---|---|---|
| 01 | 1 | [01 — Basic Concepts of Integrated Circuit I](Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| 01 | 1 | [02 — Basic Concepts of Integrated Circuit II](Daily%20Notes/Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| 01 | 1 | [03 — Overview of VLSI Design Flow I](Daily%20Notes/Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) |
| 01 | 1 | [04 — Overview of VLSI Design Flow II](Daily%20Notes/Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) |
| 01 | 1 | [05 — Tutorial 1 — Unix foundations for EDA](Daily%20Notes/Day%2001.md#lesson-05-tutorial-1--unix-foundations-for-eda) |
| 01 | 2 | [06 — Overview of VLSI Design Flow III — Logic synthesis](Daily%20Notes/Day%2001.md#lesson-06-overview-of-vlsi-design-flow-iii--logic-synthesis) |
| 02 | 2 | [07 — Overview of VLSI Design Flow IV — Physical design](Daily%20Notes/Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| 02 | 2 | [08 — Overview of VLSI Design Flow V — Verification and test](Daily%20Notes/Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| 02 | 2 | [09 — Overview of VLSI Design Flow VI — From layout to chip](Daily%20Notes/Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |
| 02 | 2 | [10 — Introduction to Tcl](Daily%20Notes/Day%2002.md#lesson-10-introduction-to-tcl) |
| 02 | 3 | [11 — Hardware Modeling — Introduction to Verilog I](Daily%20Notes/Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) |
| 02 | 3 | [12 — Hardware Modeling — Introduction to Verilog II](Daily%20Notes/Day%2002.md#lesson-12-hardware-modeling--introduction-to-verilog-ii) |
| 03 | 3 | [13 — Functional Verification using Simulation](Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| 03 | 3 | [14 — High-level synthesis using Bambu - Tutorial 3](Daily%20Notes/Day%2003.md#lesson-14-high-level-synthesis-using-bambu---tutorial-3) |
| 03 | 4 | [15 — RTL Synthesis - Part I](Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| 03 | 4 | [16 — RTL Synthesis - Part II](Daily%20Notes/Day%2003.md#lesson-16-rtl-synthesis---part-ii) |
| 03 | 4 | [17 — Logic Optimization - Part I](Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| 03 | 4 | [18 — Simulation-based Verification using Icarus](Daily%20Notes/Day%2003.md#lesson-18-simulation-based-verification-using-icarus) |
| 04 | 5 | [19 — Logic Optimization - Part II](Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii) |
| 04 | 5 | [20 — Logic Optimization - Part III](Daily%20Notes/Day%2004.md#lesson-20-logic-optimization---part-iii) |
| 04 | 5 | [21 — Formal Verification - I](Daily%20Notes/Day%2004.md#lesson-21-formal-verification---i) |
| 04 | 5 | [22 — Logic Synthesis using Yosys](Daily%20Notes/Day%2004.md#lesson-22-logic-synthesis-using-yosys) |
| 04 | 6 | [23 — Formal Verification - II](Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| 04 | 6 | [24 — Formal Verification - III](Daily%20Notes/Day%2004.md#lesson-24-formal-verification---iii) |
| 05 | 6 | [25 — Formal Verification - IV](Daily%20Notes/Day%2005.md#lesson-25-formal-verification---iv) |
| 05 | 6 | [26 — Technology Library](Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| 05 | 6 | [27 — Logic Optimization using Yosys](Daily%20Notes/Day%2005.md#lesson-27-logic-optimization-using-yosys) |
| 05 | 7 | [28 — Static Timing Analysis - I](Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| 05 | 7 | [29 — Static Timing Analysis - II](Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| 05 | 7 | [30 — Static Timing Analysis - III](Daily%20Notes/Day%2005.md#lesson-30-static-timing-analysis---iii) |
| 06 | 7 | [31 — Static Timing Analysis using OpenSTA](Daily%20Notes/Day%2006.md#lesson-31-static-timing-analysis-using-opensta) |
| 06 | 8 | [32 — Constraints I](Daily%20Notes/Day%2006.md#lesson-32-constraints-i) |
| 06 | 8 | [33 — Constraints II](Daily%20Notes/Day%2006.md#lesson-33-constraints-ii) |
| 06 | 8 | [34 — Technology Mapping](Daily%20Notes/Day%2006.md#lesson-34-technology-mapping) |
| 06 | 8 | [35 — Timing-driven Optimizations](Daily%20Notes/Day%2006.md#lesson-35-timing-driven-optimizations) |
| 06 | 8 | [36 — Technology Library and Constraints](Daily%20Notes/Day%2006.md#lesson-36-technology-library-and-constraints) |
| 07 | 9 | [37 — Power Analysis](Daily%20Notes/Day%2007.md#lesson-37-power-analysis) |
| 07 | 9 | [38 — Power Optimizations](Daily%20Notes/Day%2007.md#lesson-38-power-optimizations) |
| 07 | 9 | [39 — Basic Concepts of DFT](Daily%20Notes/Day%2007.md#lesson-39-basic-concepts-of-dft) |
| 07 | 9 | [40 — Scan Design Flow](Daily%20Notes/Day%2007.md#lesson-40-scan-design-flow) |
| 07 | 9 | [41 — Power Analysis using OpenSTA](Daily%20Notes/Day%2007.md#lesson-41-power-analysis-using-opensta) |
| 07 | 10 | [42 — Automatic Test Pattern Generation](Daily%20Notes/Day%2007.md#lesson-42-automatic-test-pattern-generation) |
| 08 | 10 | [43 — Built-in Self-Test](Daily%20Notes/Day%2008.md#lesson-43-built-in-self-test) |
| 08 | 10 | [44 — Basic Concepts of Physical Design I](Daily%20Notes/Day%2008.md#lesson-44-basic-concepts-of-physical-design-i) |
| 08 | 10 | [45 — Basic Concepts of Physical Design II](Daily%20Notes/Day%2008.md#lesson-45-basic-concepts-of-physical-design-ii) |
| 08 | 10 | [46 — Installation of OpenROAD](Daily%20Notes/Day%2008.md#lesson-46-installation-of-openroad) |
| 08 | 11 | [47 — Chip Planning I](Daily%20Notes/Day%2008.md#lesson-47-chip-planning-i) |
| 08 | 11 | [48 — Chip Planning II](Daily%20Notes/Day%2008.md#lesson-48-chip-planning-ii) |
| 09 | 11 | [49 — Placement](Daily%20Notes/Day%2009.md#lesson-49-placement) |
| 09 | 11 | [50 — Chip Planning and Placement](Daily%20Notes/Day%2009.md#lesson-50-chip-planning-and-placement) |
| 09 | 12 | [51 — Clock Tree Synthesis](Daily%20Notes/Day%2009.md#lesson-51-clock-tree-synthesis) |
| 09 | 12 | [52 — Routing](Daily%20Notes/Day%2009.md#lesson-52-routing) |
| 09 | 12 | [53 — Post-layout Verification and Signoff](Daily%20Notes/Day%2009.md#lesson-53-post-layout-verification-and-signoff) |
| 09 | 12 | [54 — Clock Tree Synthesis and Routing](Daily%20Notes/Day%2009.md#lesson-54-clock-tree-synthesis-and-routing) |

## Collection structure

```text
README.md                 Master reading index and current position
Full Forms.pdf            Indexed terminology and concise meanings
RTL to GDS Flow.pdf        Two-page technical sequence and course approach
Daily Notes/              Day 01.md to Day 09.md and the daily index
PDFs/                     Nine daily PDFs, practice worksheet and PDF index
Resources/                Supporting material and maintained sources
  sources/                Complete source pages, provenance registers and decks
  images/                 Lecture frames and comparison crops by day/lesson
  examples/               Verilog, Tcl and checked study examples
  tools/pdf/              PDF builders, checks and ignored local QA/dependencies
  tools/sources/          Historical source-import helpers
  Data/                   Preserved raw uploads (local, ignored by Git)
  *.md                    Source register, handwriting index and reference sources
```

Start with the day table or lesson index above. Daily Markdown is the editable explanation source; the PDFs are its checked reading editions. The two root reference PDFs provide quick terminology and flow navigation. [Resource guide](Resources/README.md) explains the supporting sources, builders and verification.

## Upload coverage

All **128 readable source pages** are indexed: 28 earlier pages, 32 pages from Scans A/B, and 68 October additions (Scans C/D/E contain 24/24/19 pages; the ATPG notebook adds one). The earlier zero-byte upload remains preserved separately and contributes no readable pages. Original source-PDF positions, handwritten numbers and generated PDF page numbers remain distinct.

The primary course is **VLSI Design Flow: RTL to GDS**, Prof. Sneh Saurabh, IIIT Delhi, NPTEL. Images are actual lecture captures from Chrome and scans of Kapil’s notes. Explanations and worked examples are study annotations.

## Notebook review and maintenance

The 4 October iteration checks all 128 handwritten pages and adds 26 worked explanations across all nine days. Examples develop assumptions, traces and counterexamples: operand ownership, X behavior, signed division, proof scope, multicycle schedules, scan ordering, signature collisions, macro pins, clock-skew limits, via pitch, RC topology and ECO timing budgets. [Coverage Review](Resources/Coverage%20Review.md) records validation and source limits.

Use the [maintenance workflow](Resources/tools/pdf/README.md) after editing. [Executable study checks](Resources/examples/README.md) verify the small models, while PDF checks validate source coverage and navigation. The [source inventory](Resources/sources/handwritten-inventory.json) supports published-image checks in a fresh clone and optional verification of the preserved local originals.
