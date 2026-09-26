# RTL to GDS Flow

Kapil's study notes for **VLSI Design Flow: RTL to GDS**, taught by **Prof. Sneh Saurabh, IIIT Delhi**, on NPTEL. The Unix and Tcl tutorials are presented by Jasmine Kaur.

This collection covers **Weeks 1 and 2 and the first two lessons of Week 3**, ending at **Hardware Modeling: Introduction to Verilog II**. It combines the lecture material with all **28 pages from the two uploaded handwritten PDFs**. The next dedicated lesson, *Functional Verification Using Simulation*, is outside this batch.

Read a chapter in this order: **lecture frame → concept explanation → matching handwritten snippet → explanation of your note and questions**. Some sections add worked calculations or complete code. Every chapter has an outline and navigation links. “Day” identifies the study sequence, not a claim about the calendar day on which you completed a lesson. Tutorial entries are included in the sequence, so these numbers differ from the course's theory-lecture numbers.

[Handwritten page index](Handwritten%20Index.md) · [Questions and corrections](Questions.md) · [Sources and frame timestamps](Sources.md) · [Runnable examples](examples/verilog/README.md)

## Course chapters

| Week | Study entry | Lecture | Main topics |
|---|---|---|---|
| 1 | [Day 01](Day%2001.md) | Basic Concepts of Integrated Circuit I | Integration, layers, photolithography, wafers, yield, industry, PDK |
| 1 | [Day 02](Day%2002.md) | Basic Concepts of Integrated Circuit II | ASIC/GPIC, custom design, standard cells, FPGA, cost, PPA |
| 1 | [Day 03](Day%2003.md) | Overview of VLSI Design Flow I | Flow, abstraction, hardware/software partitioning, estimates |
| 1 | [Day 04](Day%2004.md) | Overview of VLSI Design Flow II | IP reuse, HLS, setup/hold timing, scheduling, resource sharing |
| 1 | [Day 05](Day%2005.md) | Tutorial 1: Unix Commands | Linux/WSL, paths, files, permissions, processes, package commands |
| 2 | [Day 06](Day%2006.md) | Overview of VLSI Design Flow III | RTL synthesis, Liberty/SDC, library pins, generic logic, mapping |
| 2 | [Day 07](Day%2007.md) | Overview of VLSI Design Flow IV | LEF, floorplan, power, placement, CTS, routing, ECO |
| 2 | [Day 08](Day%2008.md) | Overview of VLSI Design Flow V | Verification, STA, DRC/ERC/LVS, defects, yield, test, fault coverage |
| 2 | [Day 09](Day%2009.md) | Overview of VLSI Design Flow VI | Mask preparation, OPC, multiple patterning, fabrication, packaging |
| 2 | [Day 10](Day%2010.md) | Introduction to Tcl | Substitution, lists, loops, procedures, file channels, external programs |
| 3 | [Day 11](Day%2011.md) | Hardware Modeling: Introduction to Verilog I | HDL, four-state values, literals, widths, nets, variables, wildcard cases |
| 3 | [Day 12](Day%2012.md) | Hardware Modeling: Introduction to Verilog II | Modules, parameters, operators, events, functions/tasks, assignments |

## Find a concept quickly

- **Photolithography from start to finish:** [Day 01](Day%2001.md#photolithography), followed by [mask writing, OPC, and multiple patterning in Day 09](Day%2009.md).
- **ASIC versus FPGA and choosing an implementation:** [Day 02](Day%2002.md), including a worked break-even calculation.
- **Timing and sharing hardware:** [Day 04](Day%2004.md#paths-and-the-clock-period-budget), including setup/hold equations and three ways to compute a sum.
- **Synthesis and physical design:** [Day 06](Day%2006.md) and [Day 07](Day%2007.md).
- **Yield, fault coverage, and escaped defective chips:** [Day 08](Day%2008.md#yield-fault-coverage-and-escapes).
- **`reg`, `wire`, `x`, `z`, and `?`:** [Day 11](Day%2011.md).
- **Blocking versus nonblocking assignments:** [Day 12](Day%2012.md#continuous-blocking-and-nonblocking-assignment), including the 10/40/60 versus 10/30/20 ns example.

## Handwriting and source preservation

Your original files remain in `Data/`. Reviewed copies are preserved under [sources/handwritten](sources/handwritten), with a full-page image for every page. Cropped snippets appear beside their explanations; a crop is never the only surviving copy of a page. The [handwritten index](Handwritten%20Index.md) distinguishes **PDF page numbers** from the numbers written on the paper.

The working upload folder is `Desktop/rtl to gdss/Data`. New uploads can be reviewed and integrated in the same format. The raw upload folder is excluded from Git so future files are not published accidentally; this batch's two reviewed originals and their page images are included in the archive.

## Reading and verification method

The explanations were prepared by reviewing the available transcripts for all twelve selected videos, checking selected segments in the video player, and capturing actual lecture frames in Chrome. This is a transcript-led review with targeted frame inspection, not a claim of uninterrupted playback of every minute. Supplemental primary references are linked beside relevant clarifications and collected in [Sources](Sources.md). Worked numerical examples introduced for teaching are identified as illustrative.

The Verilog checks passed with Icarus Verilog in explicit Verilog-2005 mode. They cover four-state values, signedness, wildcard case matching, parameter overrides, reset/wraparound, pipeline state, edge events, and delayed assignments. Tcl list updates, procedure results, grouping, and file I/O also passed. See [the runnable examples](examples/verilog/README.md) to repeat those checks.

The notes preserve the meaning of your handwriting while explaining shorthand and correcting ambiguous statements. The [question index](Questions.md) points directly to those discussions.
