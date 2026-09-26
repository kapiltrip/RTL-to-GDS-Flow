# RTL to GDS Flow

Kapil's study notes for **VLSI Design Flow: RTL to GDS**, taught by **Prof. Sneh Saurabh, IIIT Delhi**, on NPTEL. The Unix and Tcl tutorials are presented by Jasmine Kaur.

This collection covers **Weeks 1 and 2 and the first two lessons of Week 3**, ending at **Hardware Modeling: Introduction to Verilog II**. It combines the lecture material with all **28 pages from the two uploaded handwritten PDFs**. The next dedicated lesson, *Functional Verification Using Simulation*, is outside this batch.

Read a chapter in this order: **lecture frame → concept explanation → matching handwritten snippet → explanation of your note and questions**. Some sections add worked calculations or complete code. Every chapter has an outline and navigation links. **There are two study days, with six lessons in each. Day 2 is the current study day.** Lesson numbers identify the course sequence, including tutorials; they are separate from study-day numbers and the course’s theory-lecture numbering.

[Handwritten page index](Handwritten%20Index.md) · [Questions and corrections](Questions.md) · [Sources and frame timestamps](Sources.md) · [Runnable examples](examples/verilog/README.md)

## Start here

| What you want to do | Where to begin |
|---|---|
| Learn the material in order | [Study approach](#how-to-study-this-collection), then [Lesson 01](Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) |
| Understand what each folder contains | [Directory structure](#directory-structure) and [folder guide](#what-each-part-of-the-repository-is-for) |
| Revise a particular lecture | [Study days and lessons](#study-days-and-course-lessons) and that chapter's outline |
| Find something you wrote on paper | [Handwritten page index](Handwritten%20Index.md), using the PDF page or handwritten page number |
| Resolve a doubt or incomplete formula | [Questions and corrections](Questions.md) |
| Revisit the lecturer's explanation | The timestamp beneath the relevant video frame |
| Check a Verilog or Tcl example | [Practice with the examples](#practice-with-the-examples) |

## How to study this collection

Work through **one concept block at a time**. A chapter may contain several blocks, and a long chapter does not need to be finished in one sitting. Start with its outline so you know which question the next diagram or example is answering.

1. **Inspect the lecture frame.** Identify the labels, arrows, layers, signals, or table columns before reading the explanation. Use the timestamp to replay the corresponding segment when you need the lecturer's sequence of reasoning.
2. **Understand the definition and mechanism.** State what the term means, what it acts on, and what changes. For an equation, identify every quantity, its units, and the assumptions. For code, identify its inputs, stored state, outputs, and triggering events.
3. **Read your handwritten snippet.** Compare each sketch or statement with the explanation immediately below it. The source image preserves your original wording; the prose clarifies shorthand, completes missing steps, and points out corrections.
4. **Reproduce the example.** Trace one opening through lithography, one value through a datapath, or one signal through a clock edge. Calculate an illustrative result yourself before comparing it with the worked answer. Change one input or assumption and predict the consequence.
5. **Explain it without the page.** Give the definition in your own words, redraw the important diagram, and explain one mistake the concept helps you avoid. If you cannot explain a step, return to that step rather than rereading the whole chapter passively.

For example, in [photolithography](Day%2001.md#photolithography), first identify the substrate, deposited film, resist, and mask. Then follow one transparent mask region: exposure changes resist chemistry, development opens the positive resist, etching removes accessible film, and stripping removes the remaining resist. Finally, ask what reverses with negative resist and why development is different from etching. That is a stronger check of understanding than memorizing a list of process names.

For [blocking and nonblocking assignments](Day%2002.md#continuous-blocking-and-nonblocking-assignment), write a small time table. Separate **when the right-hand side is evaluated** from **when the destination changes**. Predict the settled values before running the supplied simulation. A correct simulation result is useful only when you can explain why it occurs.

### What the detailed explanations should give you

The notes build depth through a definition, the mechanism behind it, a reading of the actual diagram or handwriting, and a relevant example or correction. Definitions such as *net*, *pin*, *timing arc*, *slack*, *utilization*, and *simulation variable* are useful because they distinguish objects that look similar but play different roles. Extra detail stays attached to the current topic; later course material is introduced only when it is needed to understand the current explanation.

Treat worked numbers as **illustrative examples**, not foundry specifications. Distinguish a language rule from a coding convention, a model from a physical guarantee, and a design constraint from a result reported by a tool. These distinctions recur throughout RTL-to-GDS work.

### Check your understanding at each stage

| After studying | You should be able to explain or demonstrate |
|---|---|
| Lessons 01–02 | How geometry becomes a manufactured pattern; wafer versus die versus packaged chip; ASIC/FPGA choices; power, energy, performance, and area |
| Lessons 03–04 | Why abstraction changes; what partitioning and HLS decide; how latency differs from throughput; how a register path meets setup and hold |
| Lesson 05 | How the shell, current directory, paths, processes, and jobs affect a tool run |
| Lessons 06–07 | How behavior becomes cell instances, then placement and wires; which files provide function, timing, geometry, and constraints |
| Lessons 08–09 | Which checks address design errors and which address manufactured devices; what yield and fault coverage measure; how mask corrections and packaging fit the flow |
| Lesson 10 | When Tcl performs substitution, which commands receive variable names, and how the list example changes at each iteration |
| Lessons 11–12 | How widths and four-state values behave; why `reg` does not guarantee a flip-flop; when a process runs and when an assignment updates state |

## Study days and course lessons

| Study day | Lessons | Scope |
|---|---|---|
| [Day 1](Day%2001.md) | 01–06 | IC foundations through logic synthesis |
| [Day 2 — current](Day%2002.md) | 07–12 | Physical design through Verilog II |

The equal split is **six lessons per day**. Each row below opens the relevant lesson inside its day file.

| Study day | Course week | Lesson | Title |
|---|---|---|---|
| 1 | 1 | [Lesson 01](Day%2001.md#lesson-01-basic-concepts-of-integrated-circuit-i) | Basic Concepts of Integrated Circuit I |
| 1 | 1 | [Lesson 02](Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii) | Basic Concepts of Integrated Circuit II |
| 1 | 1 | [Lesson 03](Day%2001.md#lesson-03-overview-of-vlsi-design-flow-i) | Overview of VLSI Design Flow I |
| 1 | 1 | [Lesson 04](Day%2001.md#lesson-04-overview-of-vlsi-design-flow-ii) | Overview of VLSI Design Flow II |
| 1 | 1 | [Lesson 05](Day%2001.md#lesson-05-tutorial-1--unix-foundations-for-eda) | Tutorial 1 — Unix foundations for EDA |
| 1 | 2 | [Lesson 06](Day%2001.md#lesson-06-overview-of-vlsi-design-flow-iii--logic-synthesis) | Overview of VLSI Design Flow III — Logic synthesis |
| 2 | 2 | [Lesson 07](Day%2002.md#lesson-07-overview-of-vlsi-design-flow-iv--physical-design) | Overview of VLSI Design Flow IV — Physical design |
| 2 | 2 | [Lesson 08](Day%2002.md#lesson-08-overview-of-vlsi-design-flow-v--verification-and-test) | Overview of VLSI Design Flow V — Verification and test |
| 2 | 2 | [Lesson 09](Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip) | Overview of VLSI Design Flow VI — From layout to chip |
| 2 | 2 | [Lesson 10](Day%2002.md#lesson-10-introduction-to-tcl) | Introduction to Tcl |
| 2 | 3 | [Lesson 11](Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i) | Hardware Modeling — Introduction to Verilog I |
| 2 | 3 | [Lesson 12](Day%2002.md#lesson-12-hardware-modeling--introduction-to-verilog-ii) | Hardware Modeling — Introduction to Verilog II |

## Find a concept quickly

- **Accelerator communication and resource scheduling:** [Day 1's transfer-time calculation](Day%2001.md#trace-an-accelerator-request-and-calculate-its-communication-cost) and [HLS schedule](Day%2001.md#build-a-schedule-from-dependencies-and-resource-limits).
- **Fault activation and process execution:** [Day 2's fault-detection table](Day%2002.md#work-out-a-test-that-activates-and-exposes-a-fault) and [initial/always clock trace](Day%2002.md#trace-the-lecture-clock-generator).
- **Photolithography from start to finish:** [Lesson 01](Day%2001.md#photolithography), followed by [mask writing, OPC, and multiple patterning in Lesson 09](Day%2002.md#lesson-09-overview-of-vlsi-design-flow-vi--from-layout-to-chip).
- **ASIC versus FPGA and choosing an implementation:** [Lesson 02](Day%2001.md#lesson-02-basic-concepts-of-integrated-circuit-ii), including a worked break-even calculation.
- **Power versus energy per operation:** [Lesson 02's worked calculation](Day%2001.md#worked-example-power-is-not-energy-per-operation).
- **Timing and sharing hardware:** [Lesson 04](Day%2001.md#paths-and-the-clock-period-budget), including [why skew helps setup but can hurt hold](Day%2001.md#why-clock-skew-can-help-setup-and-hurt-hold) and three ways to compute a sum.
- **Timing arcs, slew, load, and PVT:** [Lesson 06's library explanation](Day%2001.md#timing-arcs-slew-load-and-operating-corners).
- **Utilization versus routing congestion:** [Lesson 07's capacity example](Day%2002.md#worked-example-placement-area-and-routing-capacity).
- **Yield, fault coverage, and escaped defective chips:** [Lesson 08](Day%2002.md#yield-fault-coverage-and-escapes).
- **Line width, pitch, and alignment:** [Lesson 09's patterning example](Day%2002.md#read-the-geometry-width-spacing-pitch-and-overlay).
- **Tcl substitution and list updates:** [Lesson 10's iteration trace](Day%2002.md#trace-the-list-instead-of-memorizing-the-output).
- **`reg`, `wire`, `x`, `z`, and `?`:** [Lesson 11](Day%2002.md#lesson-11-hardware-modeling--introduction-to-verilog-i), including [how unknowns propagate through operators](Day%2002.md#why-an-unknown-input-does-not-always-make-the-output-unknown).
- **Blocking versus nonblocking assignments:** [Lesson 12](Day%2002.md#continuous-blocking-and-nonblocking-assignment), including the 10/40/60 versus 10/30/20 ns example and a [cycle-by-cycle pipeline trace](Day%2002.md#follow-one-sample-through-both-registers).

## Directory structure

The local folder is named **`rtl to gdss`**; its GitHub repository is **`RTL-to-GDS-Flow`**. The structure below describes the existing collection. Number ranges group repeated files rather than indicating additional folders. Git's own `.git/` metadata is omitted.

```text
rtl to gdss/
├── README.md                       Study approach, two-day index, directory guide
├── Day 01.md                       Lessons 01–06, with all explanations and images
├── Day 02.md                       Lessons 07–12; current study day
├── Handwritten Index.md            All 28 PDF pages mapped to day/lesson sections
├── Questions.md                    Handwritten questions and correction links
├── Sources.md                      Lecture frame timestamps and primary references
│
├── images/
│   ├── Day 01/
│   │   ├── Lesson 01/              IC construction and photolithography
│   │   ├── Lesson 02/              IC types, implementation styles, cost, PPA
│   │   ├── Lesson 03/              Abstraction and hardware/software partition
│   │   ├── Lesson 04/              IP, HLS, timing, resource sharing
│   │   ├── Lesson 05/              Unix tutorial
│   │   └── Lesson 06/              Logic synthesis and libraries
│   └── Day 02/
│       ├── Lesson 07/              Physical design, clocks, routing
│       ├── Lesson 08/              Verification, yield, manufacturing test
│       ├── Lesson 09/              Masks, OPC, fabrication, packaging
│       ├── Lesson 10/              Tcl
│       ├── Lesson 11/              Verilog I
│       └── Lesson 12/              Verilog II
│
├── sources/
│   └── handwritten/
│       ├── Part-1-original.pdf     Preserved first PDF, 24 pages
│       ├── Part-2-original.pdf     Preserved second PDF, 4 pages
│       ├── part1/                  page-01.jpg through page-24.jpg
│       └── scan/                   page-01.jpg through page-04.jpg
│
├── examples/
│   ├── run_checks.py               Runs Verilog and Tcl example checks
│   ├── tcl_basics.tcl              Complete Lesson 10 scripts
│   └── verilog/
│       ├── README.md               File guide and execution commands
│       ├── select_register.v       Multiplexer feeding a flip-flop
│       ├── mux_forms.v             Two combinational descriptions
│       ├── counter.v               Parameterized counter and wrapper
│       ├── pipeline2.v             Two stages of clocked state
│       ├── initial_always_demo.v   Initialization and a timed clock generator
│       ├── function_task_demo.v    Function result and task invocation
│       ├── assignment_delays.v     Blocking/nonblocking timing example
│       ├── tb_language.v           Values, widths, events, and state checks
│       └── tb_delays.v             Assignment timing checks
│
├── Data/                           Local inbox for new uploads
│   ├── README.md                   Tracked upload instructions
│   └── (uploaded PDFs and images)  Local originals; excluded from Git here
└── .gitignore                      Inbox and generated-output exclusions
```

### What each part of the repository is for

| Location | How to use it |
|---|---|
| `Day 01.md` / `Day 02.md` | Read the explanation. Start at the outline; follow the frame, prose, handwriting, and worked example together. |
| `images/Day NN/Lesson NN/` | Find the exact image embedded in that chapter. Files such as `02-ic-layers.png` are lecture frames; files such as `h03-lithography.jpg` are handwritten crops. The `h` identifies handwriting. |
| `sources/handwritten/` | Recover the whole source when a crop does not show enough context. These complete PDFs and page images preserve everything uploaded in this batch. |
| `Handwritten Index.md` | Translate between PDF page position, the number written on paper, and the corresponding day chapter. |
| `Questions.md` | Jump directly to a doubt, unfinished calculation, or corrected interpretation. |
| `Sources.md` | Find the video timestamp for a frame or the reference supporting an additional explanation. |
| `examples/` | Open, change, and run editable code after predicting its behavior from the notes. |
| `Data/` | Add new source material locally. Its contents are an inbox, not a second set of finished chapters. |

There are currently **44 lecture frames, 40 handwritten snippets, 28 full-page handwritten images, and 2 original PDFs**. A handwritten page may supply several snippets or span more than one lesson, so snippet count and source-page count differ. Image filenames are local to each lesson folder; the caption gives the original video time or PDF page.

## Practice with the examples

First read the matching code in the chapter, then open the editable version under `examples/`. With Python including Tk/Tcl and Icarus Verilog installed, run this from the repository root:

```text
python examples/run_checks.py
```

The checker compiles into a temporary directory and runs the Tcl file-writing example there. [The example guide](examples/verilog/README.md) explains the individual files and expected messages. The deliberate `6'h88` truncation example can produce a warning; its resulting bits are checked. For revision, predict a changed input or parameter's effect before changing a file, and distinguish a failed expectation from a compiler or environment error.

## Handwriting and source preservation

Your original files remain in `Data/`. Reviewed copies are preserved under [sources/handwritten](sources/handwritten), with a full-page image for every page. Cropped snippets appear beside their explanations; a crop is never the only surviving copy of a page. The [handwritten index](Handwritten%20Index.md) distinguishes **PDF page numbers** from the numbers written on the paper.

The working upload folder is `Desktop/rtl to gdss/Data`. New uploads can be reviewed and integrated in the same format. The raw upload folder is excluded from Git so future files are not published accidentally; this batch's two reviewed originals and their page images are included in the archive.

For new material, place the original PDF or image in `Data/` and identify the course topic if you know it. The study collection can then add readable page images or crops, connect them to the matching lecture, answer questions written on the pages, and update the chapter and handwritten indexes. There is no need to rewrite or erase an original handwritten page when its explanation needs a correction.

## Reading and verification method

The explanations were prepared by reviewing the available transcripts for all twelve selected videos, checking selected segments in the video player, and capturing actual lecture frames in Chrome. This is a transcript-led review with targeted frame inspection, not a claim of uninterrupted playback of every minute. Supplemental primary references are linked beside relevant clarifications and collected in [Sources](Sources.md). Worked numerical examples introduced for teaching are identified as illustrative.

The Verilog checks passed with Icarus Verilog in explicit Verilog-2005 mode. They cover four-state values, signedness, wildcard case matching, parameter overrides, reset/wraparound, pipeline state, edge events, and delayed assignments. Tcl list updates, procedure results, grouping, and file I/O also passed. See [the runnable examples](examples/verilog/README.md) to repeat those checks.

The notes preserve the meaning of your handwriting while explaining shorthand and correcting ambiguous statements. The [question index](Questions.md) points directly to those discussions.
