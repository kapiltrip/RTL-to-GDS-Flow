# RTL to GDS study notes

**Current position: Week 8, Constraints I — Day 06, Lesson 02 of the day (course Lesson 32).** Updated from Kapil's reported progress on 30 September 2026. Tutorials count in the sequence. These are study blocks, not claims about calendar days or completed laboratory work.

Open [Daily Notes](Daily%20Notes/README.md) for the day-wise RTL-to-GDS notes or [PDFs](PDFs/README.md) for the reading collection. The two reference PDFs at the top level provide quick revision: [Full Forms](Full%20Forms.pdf) explains terminology, and [RTL to GDS Flow](RTL%20to%20GDS%20Flow.pdf) outlines the stages, their purpose and the NPTEL teaching sequence.

The references emphasize implementation theory, requirements and design artifacts, which carry over to a Synopsys workflow. Each daily PDF has clickable contents, hierarchical bookmarks and figure/footer links back to contents. Markdown figures return to their day index. Detailed mechanisms, original handwriting, lecture timestamps, corrections and worked applications remain together in the daily notes.

The equal allocation is **six lessons per day**: `day = floor((lesson−1)/6)+1`. Thus 32 lessons give five full days and two lessons in Day 06. The next item is Constraints II, Lesson 33, Day 06 Lesson 03. Equal lesson counts do not imply equal video durations or equal study effort.

## Daily reading index

| Day | Lessons | Topic | PDF | Pages |
|---|---|---|---|---:|
| [Day 01](Daily%20Notes/Day%2001.md) | 01–06 | IC foundations and synthesis | [Read PDF](PDFs/Day%2001%20-%20IC%20Foundations%20and%20Logic%20Synthesis.pdf) | 63 |
| [Day 02](Daily%20Notes/Day%2002.md) | 07–12 | Physical design and Verilog | [Read PDF](PDFs/Day%2002%20-%20Physical%20Design%20and%20Verilog%20Foundations.pdf) | 65 |
| [Day 03](Daily%20Notes/Day%2003.md) | 13–18 | Simulation, synthesis and Boolean covers | [Read PDF](PDFs/Day%2003%20-%20Simulation%20Synthesis%20and%20Logic%20Optimization.pdf) | 40 |
| [Day 04](Daily%20Notes/Day%2004.md) | 19–24 | Multilevel optimization and formal methods | [Read PDF](PDFs/Day%2004%20-%20Multilevel%20Optimization%20and%20Formal%20Verification.pdf) | 27 |
| [Day 05](Daily%20Notes/Day%2005.md) | 25–30 | Equivalence, libraries and STA | [Read PDF](PDFs/Day%2005%20-%20Equivalence%20Libraries%20and%20Static%20Timing%20Analysis.pdf) | 26 |
| [Day 06](Daily%20Notes/Day%2006.md) | 31–32 | OpenSTA and Constraints I | [Read PDF](PDFs/Day%2006%20-%20OpenSTA%20and%20Clock%20Constraints.pdf) | 14 |

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

## Collection structure

```text
README.md                 Master reading index and current position
Full Forms.pdf            Indexed terminology and concise meanings
RTL to GDS Flow.pdf        Two-page technical sequence and course approach
Daily Notes/              Day 01.md to Day 06.md and the daily index
PDFs/                     Six daily PDFs, practice worksheet and PDF index
Resources/                Supporting material and maintained sources
  sources/                Original PDFs and complete handwritten page images
  images/                 Lecture frames and comparison crops by day/lesson
  examples/               Verilog, Tcl and checked study examples
  tools/pdf/              PDF builders, checks and ignored local QA/dependencies
  Data/                   Preserved raw uploads (local, ignored by Git)
  *.md                    Source register, handwriting index and reference sources
```

The outermost reading level contains three folders, the master index and the two reference PDFs. [Resource guide](Resources/README.md) explains the supporting sources, builders and verification.

## Upload coverage

All 28 earlier handwritten pages and all 32 readable pages from the two new scans are indexed. The third new PDF has **zero bytes** and no recoverable pages. It is preserved as `Resources/Data/Scan-Empty-Upload.pdf`; its content cannot be inferred. Source PDF page numbers remain distinct from handwritten numbers and the generated PDF page numbers.

The primary course is **VLSI Design Flow: RTL to GDS**, Prof. Sneh Saurabh, IIIT Delhi, NPTEL. Images are actual lecture captures from Chrome and scans of Kapil’s notes. Explanations and worked examples are study annotations.
