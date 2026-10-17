# RTL to GDS PDF revision collection

**Current position: Week 12 complete — Day 09, Lesson 06 of the day (course Lesson 54).** Updated from Kapil's reported progress on 3 October 2026. Tutorials count in the sequence; the study notes review demonstrations without claiming new laboratory runs.

**Start with the daily PDFs below.** All 14 reader PDFs are directly at the repository top level. Editable notes, images, original sources and tools are inside [Resources](Resources/README.md). The [complete PDF index](Resources/PDF%20Index.md) lists every document. For quick revision, [Full Forms](Full%20Forms.pdf) explains terminology, and [RTL to GDS Flow](RTL%20to%20GDS%20Flow.pdf) outlines the implementation stages and course sequence.

[Download the complete collection ZIP](https://github.com/kapiltrip/RTL-to-GDS-Flow/archive/refs/heads/main.zip) for all PDFs, editable notes and supporting files. Extract the ZIP before reading. Each day below also has its own **Download PDF** link; the [PDF index](Resources/PDF%20Index.md#references-and-practice) has downloads for the references and practice worksheet.

For the laboratory project, open the [Synopsys RTL to GDS Project Plan](Synopsys%20RTL%20to%20GDS%20Project%20Plan.pdf) or its [editable source](Resources/Synopsys%20RTL%20to%20GDS%20Project%20Plan.md). The 18-page plan maps the tools to the flow, lists technology dependencies, supplies Thapar lab inventory forms and requires a complete trial before the main project begins. Take pages 6–8 to the lab; the readiness trial is on page 9.

The separate [one-page Synopsys tool map](Synopsys%20RTL%20to%20GDS%20Tool%20Map.pdf) lists only the process stages and tool names for quick reference.

The nine daily PDFs contain **all 128 complete handwritten pages**, with explanations beside their source material. Each PDF adds a subject-specific revision route, six worked questions with explained answers, and a clickable handwritten-page finder. Contents, bookmarks and figure/footer links support quick revision; detailed mechanisms, lecture timestamps, corrections, examples and code remain in the reading editions.

The allocation is **six lessons per study day**: `day = floor((lesson−1)/6)+1`. All 54 course lessons now occupy nine completed study blocks. Equal lesson counts do not imply equal video durations or study effort.

## Daily reading index

| Day | Lessons | Topic | PDF | Download | Pages |
|---|---|---|---|---|---:|
| [Day 01](Resources/Daily%20Notes/Day%2001.md) | 01–06 | IC foundations and synthesis | [Read PDF](Day%2001%20-%20IC%20Foundations%20and%20Logic%20Synthesis.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2001%20-%20IC%20Foundations%20and%20Logic%20Synthesis.pdf) | 85 |
| [Day 02](Resources/Daily%20Notes/Day%2002.md) | 07–12 | Physical design and Verilog | [Read PDF](Day%2002%20-%20Physical%20Design%20and%20Verilog%20Foundations.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2002%20-%20Physical%20Design%20and%20Verilog%20Foundations.pdf) | 82 |
| [Day 03](Resources/Daily%20Notes/Day%2003.md) | 13–18 | Simulation, synthesis and Boolean covers | [Read PDF](Day%2003%20-%20Simulation%20Synthesis%20and%20Logic%20Optimization.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2003%20-%20Simulation%20Synthesis%20and%20Logic%20Optimization.pdf) | 43 |
| [Day 04](Resources/Daily%20Notes/Day%2004.md) | 19–24 | Multilevel optimization and formal methods | [Read PDF](Day%2004%20-%20Multilevel%20Optimization%20and%20Formal%20Verification.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2004%20-%20Multilevel%20Optimization%20and%20Formal%20Verification.pdf) | 30 |
| [Day 05](Resources/Daily%20Notes/Day%2005.md) | 25–30 | Equivalence, libraries and STA | [Read PDF](Day%2005%20-%20Equivalence%20Libraries%20and%20Static%20Timing%20Analysis.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2005%20-%20Equivalence%20Libraries%20and%20Static%20Timing%20Analysis.pdf) | 28 |
| [Day 06](Resources/Daily%20Notes/Day%2006.md) | 31–36 | Constraints, mapping and timing optimization | [Read PDF](Day%2006%20-%20OpenSTA%20and%20Clock%20Constraints.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2006%20-%20OpenSTA%20and%20Clock%20Constraints.pdf) | 44 |
| [Day 07](Resources/Daily%20Notes/Day%2007.md) | 37–42 | Power, scan design and ATPG | [Read PDF](Day%2007%20-%20Power%20Scan%20Design%20and%20ATPG.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2007%20-%20Power%20Scan%20Design%20and%20ATPG.pdf) | 42 |
| [Day 08](Resources/Daily%20Notes/Day%2008.md) | 43–48 | BIST, physical foundations and chip planning | [Read PDF](Day%2008%20-%20BIST%20Physical%20Foundations%20and%20Chip%20Planning.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2008%20-%20BIST%20Physical%20Foundations%20and%20Chip%20Planning.pdf) | 44 |
| [Day 09](Resources/Daily%20Notes/Day%2009.md) | 49–54 | Placement, clocks, routing and signoff | [Read PDF](Day%2009%20-%20Placement%20Clocks%20Routing%20and%20Signoff.pdf) | [Download PDF](https://github.com/kapiltrip/RTL-to-GDS-Flow/raw/refs/heads/main/Day%2009%20-%20Placement%20Clocks%20Routing%20and%20Signoff.pdf) | 59 |

[Find handwritten pages](Resources/Handwritten%20Index.md) · [Corrections and doubts](Resources/Questions.md) · [Sources and timestamps](Resources/Sources.md) · [Study method](Resources/Study%20Guide.md) · [Coverage and depth review](Resources/Coverage%20Review.md)

[Week 7 and Week 8 practice questions](Resources/Week%2007%20and%2008%20-%20Practice%20Questions.md) · [Question-only worksheet PDF](Week%2007%20and%2008%20-%20Practice%20Questions.pdf). All 20 assignment questions, their unmarked options and six source figures are included.

<details>
<summary>Detailed course lesson index and editable sources</summary>

## Course lesson index

| Day | Week | Lesson and topic |
|---|---|---|
| 01 | 1 | [01 — Basic Concepts of Integrated Circuit I](Resources/Daily%20Notes/Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| 01 | 1 | [02 — Basic Concepts of Integrated Circuit II](Resources/Daily%20Notes/Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) |
| 01 | 1 | [03 — Overview of VLSI Design Flow I](Resources/Daily%20Notes/Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) |
| 01 | 1 | [04 — Overview of VLSI Design Flow II](Resources/Daily%20Notes/Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) |
| 01 | 1 | [05 — Tutorial 1 — Unix foundations for EDA](Resources/Daily%20Notes/Day%2001.md#lesson-05-tutorial-1--unix-foundations-for-eda) |
| 01 | 2 | [06 — Overview of VLSI Design Flow III — Logic synthesis](Resources/Daily%20Notes/Day%2001.md#lesson-06-overview-of-vlsi-design-flow-iii--logic-synthesis) |
| 02 | 2 | [07 — Overview of VLSI Design Flow IV — Physical design](Resources/Daily%20Notes/Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) |
| 02 | 2 | [08 — Overview of VLSI Design Flow V — Verification and test](Resources/Daily%20Notes/Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) |
| 02 | 2 | [09 — Overview of VLSI Design Flow VI — From layout to chip](Resources/Daily%20Notes/Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) |
| 02 | 2 | [10 — Introduction to Tcl](Resources/Daily%20Notes/Day%2002.md#lesson-10-introduction-to-tcl) |
| 02 | 3 | [11 — Hardware Modeling — Introduction to Verilog I](Resources/Daily%20Notes/Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) |
| 02 | 3 | [12 — Hardware Modeling — Introduction to Verilog II](Resources/Daily%20Notes/Day%2002.md#lesson-12-hardware-modeling--introduction-to-verilog-ii) |
| 03 | 3 | [13 — Functional Verification using Simulation](Resources/Daily%20Notes/Day%2003.md#lesson-13-functional-verification-using-simulation) |
| 03 | 3 | [14 — High-level synthesis using Bambu - Tutorial 3](Resources/Daily%20Notes/Day%2003.md#lesson-14-high-level-synthesis-using-bambu---tutorial-3) |
| 03 | 4 | [15 — RTL Synthesis - Part I](Resources/Daily%20Notes/Day%2003.md#lesson-15-rtl-synthesis---part-i) |
| 03 | 4 | [16 — RTL Synthesis - Part II](Resources/Daily%20Notes/Day%2003.md#lesson-16-rtl-synthesis---part-ii) |
| 03 | 4 | [17 — Logic Optimization - Part I](Resources/Daily%20Notes/Day%2003.md#lesson-17-logic-optimization---part-i) |
| 03 | 4 | [18 — Simulation-based Verification using Icarus](Resources/Daily%20Notes/Day%2003.md#lesson-18-simulation-based-verification-using-icarus) |
| 04 | 5 | [19 — Logic Optimization - Part II](Resources/Daily%20Notes/Day%2004.md#lesson-19-logic-optimization---part-ii) |
| 04 | 5 | [20 — Logic Optimization - Part III](Resources/Daily%20Notes/Day%2004.md#lesson-20-logic-optimization---part-iii) |
| 04 | 5 | [21 — Formal Verification - I](Resources/Daily%20Notes/Day%2004.md#lesson-21-formal-verification---i) |
| 04 | 5 | [22 — Logic Synthesis using Yosys](Resources/Daily%20Notes/Day%2004.md#lesson-22-logic-synthesis-using-yosys) |
| 04 | 6 | [23 — Formal Verification - II](Resources/Daily%20Notes/Day%2004.md#lesson-23-formal-verification---ii) |
| 04 | 6 | [24 — Formal Verification - III](Resources/Daily%20Notes/Day%2004.md#lesson-24-formal-verification---iii) |
| 05 | 6 | [25 — Formal Verification - IV](Resources/Daily%20Notes/Day%2005.md#lesson-25-formal-verification---iv) |
| 05 | 6 | [26 — Technology Library](Resources/Daily%20Notes/Day%2005.md#lesson-26-technology-library) |
| 05 | 6 | [27 — Logic Optimization using Yosys](Resources/Daily%20Notes/Day%2005.md#lesson-27-logic-optimization-using-yosys) |
| 05 | 7 | [28 — Static Timing Analysis - I](Resources/Daily%20Notes/Day%2005.md#lesson-28-static-timing-analysis---i) |
| 05 | 7 | [29 — Static Timing Analysis - II](Resources/Daily%20Notes/Day%2005.md#lesson-29-static-timing-analysis---ii) |
| 05 | 7 | [30 — Static Timing Analysis - III](Resources/Daily%20Notes/Day%2005.md#lesson-30-static-timing-analysis---iii) |
| 06 | 7 | [31 — Static Timing Analysis using OpenSTA](Resources/Daily%20Notes/Day%2006.md#lesson-31-static-timing-analysis-using-opensta) |
| 06 | 8 | [32 — Constraints I](Resources/Daily%20Notes/Day%2006.md#lesson-32-constraints-i) |
| 06 | 8 | [33 — Constraints II](Resources/Daily%20Notes/Day%2006.md#lesson-33-constraints-ii) |
| 06 | 8 | [34 — Technology Mapping](Resources/Daily%20Notes/Day%2006.md#lesson-34-technology-mapping) |
| 06 | 8 | [35 — Timing-driven Optimizations](Resources/Daily%20Notes/Day%2006.md#lesson-35-timing-driven-optimizations) |
| 06 | 8 | [36 — Technology Library and Constraints](Resources/Daily%20Notes/Day%2006.md#lesson-36-technology-library-and-constraints) |
| 07 | 9 | [37 — Power Analysis](Resources/Daily%20Notes/Day%2007.md#lesson-37-power-analysis) |
| 07 | 9 | [38 — Power Optimizations](Resources/Daily%20Notes/Day%2007.md#lesson-38-power-optimizations) |
| 07 | 9 | [39 — Basic Concepts of DFT](Resources/Daily%20Notes/Day%2007.md#lesson-39-basic-concepts-of-dft) |
| 07 | 9 | [40 — Scan Design Flow](Resources/Daily%20Notes/Day%2007.md#lesson-40-scan-design-flow) |
| 07 | 9 | [41 — Power Analysis using OpenSTA](Resources/Daily%20Notes/Day%2007.md#lesson-41-power-analysis-using-opensta) |
| 07 | 10 | [42 — Automatic Test Pattern Generation](Resources/Daily%20Notes/Day%2007.md#lesson-42-automatic-test-pattern-generation) |
| 08 | 10 | [43 — Built-in Self-Test](Resources/Daily%20Notes/Day%2008.md#lesson-43-built-in-self-test) |
| 08 | 10 | [44 — Basic Concepts of Physical Design I](Resources/Daily%20Notes/Day%2008.md#lesson-44-basic-concepts-of-physical-design-i) |
| 08 | 10 | [45 — Basic Concepts of Physical Design II](Resources/Daily%20Notes/Day%2008.md#lesson-45-basic-concepts-of-physical-design-ii) |
| 08 | 10 | [46 — Installation of OpenROAD](Resources/Daily%20Notes/Day%2008.md#lesson-46-installation-of-openroad) |
| 08 | 11 | [47 — Chip Planning I](Resources/Daily%20Notes/Day%2008.md#lesson-47-chip-planning-i) |
| 08 | 11 | [48 — Chip Planning II](Resources/Daily%20Notes/Day%2008.md#lesson-48-chip-planning-ii) |
| 09 | 11 | [49 — Placement](Resources/Daily%20Notes/Day%2009.md#lesson-49-placement) |
| 09 | 11 | [50 — Chip Planning and Placement](Resources/Daily%20Notes/Day%2009.md#lesson-50-chip-planning-and-placement) |
| 09 | 12 | [51 — Clock Tree Synthesis](Resources/Daily%20Notes/Day%2009.md#lesson-51-clock-tree-synthesis) |
| 09 | 12 | [52 — Routing](Resources/Daily%20Notes/Day%2009.md#lesson-52-routing) |
| 09 | 12 | [53 — Post-layout Verification and Signoff](Resources/Daily%20Notes/Day%2009.md#lesson-53-post-layout-verification-and-signoff) |
| 09 | 12 | [54 — Clock Tree Synthesis and Routing](Resources/Daily%20Notes/Day%2009.md#lesson-54-clock-tree-synthesis-and-routing) |

</details>

## Collection structure

```text
Day 01 - ...pdf to Day 09 - ...pdf    Daily reading and revision
Full Forms.pdf                      Terminology and meanings
RTL to GDS Flow.pdf                  Two-page flow reference
Synopsys ...pdf                      Project plan and one-page tool map
Week 07 and 08 - ...pdf              Practice worksheet
README.md                           Reading and download index
Resources/                          All supporting material
  Daily Notes/                      Editable sources for the nine daily PDFs
  sources/ and images/              Original pages and lecture figures
  examples/ and tools/              Checked examples and PDF maintenance
```

Read the PDF files in day order. Each contains its complete original handwritten pages, so revision does not require opening the supporting folders. The [resource guide](Resources/README.md) explains the editable sources and maintenance tools.

## Upload coverage

All **128 readable source pages** are indexed: 28 earlier pages, 32 pages from Scans A/B, and 68 October additions (Scans C/D/E contain 24/24/19 pages; the ATPG notebook adds one). The earlier zero-byte upload remains preserved separately and contributes no readable pages. Original source-PDF positions, handwritten numbers and generated PDF page numbers remain distinct.

The primary course is **VLSI Design Flow: RTL to GDS**, Prof. Sneh Saurabh, IIIT Delhi, NPTEL. Images are actual lecture captures from Chrome and scans of Kapil’s notes. Explanations and worked examples are study annotations.

## Notebook review and maintenance

The 4 October iteration checks all 128 handwritten pages and adds 26 worked explanations across all nine days. Examples develop assumptions, traces and counterexamples: operand ownership, X behavior, signed division, proof scope, multicycle schedules, scan ordering, signature collisions, macro pins, clock-skew limits, via pitch, RC topology and ECO timing budgets. [Coverage Review](Resources/Coverage%20Review.md) records validation and source limits.

Use the [maintenance workflow](Resources/tools/pdf/README.md) after editing. [Executable study checks](Resources/examples/README.md) verify the small models, while PDF checks validate source coverage and navigation. The [source inventory](Resources/sources/handwritten-inventory.json) supports published-image checks in a fresh clone and optional verification of the preserved local originals.
