# Study method

[Master index](../README.md)

## How to study this collection

Work through **one concept block at a time**. A chapter may contain several blocks, and a long chapter does not need to be finished in one sitting. Start with its outline so you know which question the next diagram or example is answering.

1. **Inspect the lecture frame.** Identify the labels, arrows, layers, signals, or table columns before reading the explanation. Use the timestamp to replay the corresponding segment when you need the lecturer's sequence of reasoning.
2. **Understand the definition and mechanism.** State what the term means, what it acts on, and what changes. For an equation, identify every quantity, its units, and the assumptions. For code, identify its inputs, stored state, outputs, and triggering events.
3. **Read your handwritten snippet.** Compare each sketch or statement with the explanation immediately below it. The source image preserves your original wording; the prose clarifies shorthand, completes missing steps, and points out corrections.
4. **Reproduce the example.** Trace one opening through lithography, one value through a datapath, or one signal through a clock edge. Calculate an illustrative result yourself before comparing it with the worked answer. Change one input or assumption and predict the consequence.
5. **Explain it without the page.** Give the definition in your own words, redraw the important diagram, and explain one mistake the concept helps you avoid. If you cannot explain a step, return to that step rather than rereading the whole chapter passively.

For example, in [photolithography](../Day%2001.md#photolithography), first identify the substrate, deposited film, resist, and mask. Then follow one transparent mask region: exposure changes resist chemistry, development opens the positive resist, etching removes accessible film, and stripping removes the remaining resist. Finally, ask what reverses with negative resist and why development is different from etching. That is a stronger check of understanding than memorizing a list of process names.

For [blocking and nonblocking assignments](../Day%2002.md#continuous-blocking-and-nonblocking-assignment), write a small time table. Separate **when the right-hand side is evaluated** from **when the destination changes**. Predict the settled values before running the supplied simulation. A correct simulation result is useful only when you can explain why it occurs.

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
