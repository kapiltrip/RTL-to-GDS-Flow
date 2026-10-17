# Weekly revision and question sources

[Master index](../../README.md) · [Revision](../../Revision/README.md) · [Assignments](../../Assignments/README.md)

The course-week organization follows the [official NPTEL course](https://nptel.ac.in/courses/108106191), **VLSI Design Flow: RTL to GDS**, Prof. Sneh Saurabh, IIIT Delhi. It is separate from the six-lessons-per-day organization of the full reading notes.

Each `Week NN` folder contains a question-only capture in `original.json` and 50 newly authored practice questions in `practice.json`. Original questions were read from Kapil's enrolled **noc26_ee147** course on 17 October 2026. Captures retain source URLs, wording, option order, mathematical source parts and figure references. They omit account details, submission history, selected responses, accepted-answer text and feedback. The [figure register](figures.json) records hashes for all 19 original figure files.

The browser practice uses comparison digests to calculate a score. No human-readable answer index or answer key is included in the question files or PDFs. The interface displays marks only after finishing an attempt and choosing Show marks. Personal selections and histories remain in the user's browser or exported answers backup, not in the repository. Comparison data in a self-contained client file is not a secure examination backend.

Original NPTEL content: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), linked from [NPTEL's licence notice](https://archive.nptel.ac.in/footer.html). The question-only adaptation removes old choices and grading feedback; typographic encoding and mathematical presentation are cleaned without changing intended content. No endorsement by NPTEL is implied.

## Original course sources

| Week | Source record |
|---|---|
| 01 | [Week 01](Week%2001/original.json) |
| 02 | [Week 02](Week%2002/original.json) |
| 03 | [Week 03](Week%2003/original.json) |
| 04 | [Week 04](Week%2004/original.json) |
| 05 | [Week 05](Week%2005/original.json) |
| 06 | [Week 06](Week%2006/original.json) |
| 07 | [Week 07](Week%2007/original.json) |
| 08 | [Week 08](Week%2008/original.json) |
| 09 | [Week 09](Week%2009/original.json) |
| 10 | [Week 10](Week%2010/original.json) |
| 11 | [Week 11](Week%2011/original.json) |
| 12 | [Week 12](Week%2012/original.json) |

## Revision and exam-discussion evidence

Revision is ready through **Week 3**. The [Week 1 source](Week%2001/revision.md) cites the four Week 1 lectures, Unix tutorial and primary HLS documentation. The [Week 2 source](Week%2002/revision.md) covers Lessons 06-09 and the Tcl tutorial, combining Kapil's new handwritten points with the remaining topics. It adds worked checks and distinctions for synthesis, physical design, verification, test/yield, manufacturing and Tcl. The [complete new upload and page map](Week%2002/handwritten/README.md) preserve all six original pages; four Week 2 views appear after the nine typed revision pages. Numerical examples state their assumptions and do not print an original-assignment answer key.

The [Week 3 source](Week%2003/revision.md) covers Lessons 11-14: Verilog I/II, functional verification using simulation and the Bambu tutorial. Ten typed pages explain language semantics, worked values/timing traces, coverage and HLS trade-offs. Six canonical original page images form its appendix: Part 2 pages 2-4 and Scan A pages 1-3. The [example verifier](Week%2003/verify_revision.py) runs the printed complete Verilog snippets plus independent checks for widths, four-state operators/edges, NBA pipelines, delayed assignments, clock timing and precision. It records 38 semantic checks plus queue/clock/precision results in the ignored QA folder. The C branch examples are reviewed; a fresh Bambu synthesis run is not claimed.

A [student discussion about the RTL-to-GDS examination](https://www.reddit.com/r/NPTEL/comments/1oeecva/nptel_exam_vlsi_design_flow_rtl_to_gds/) reports assignment-style theory alongside numerical questions. This unverified recollection supplies neither an authenticated paper nor a reliable forecast of topic weights. A [2026 preparation discussion](https://www.reddit.com/r/NPTEL/comments/1x5tb2g/vlsi_rtl_to_gds_nptel_exam_preparation_advice/) asks for guidance but does not substantiate specific Week 1 past-exam items. These sources support using a mixed practice format, not labeling authored questions as actual PYQs.

## Rebuild and verification

The primary revision download is [Combined Revision.pdf](../../Revision/Combined%20Revision.pdf). Keep this filename stable. `combine_revisions.py` discovers every prepared `Revision/Week NN - Revision.pdf` in numeric order, preserves its complete pages and scoped navigation, and adds linked master contents, week bookmarks and combined page numbers. `build_weekly.py --revision-only --week N` rebuilds this combined file automatically after preparing week N. Thus adding Week 4 or a later requested week also expands the existing download. `update_index.py` discovers individual revision PDFs and refreshes the combined coverage/page-count blocks and download tables.

To combine existing guides without rebuilding them, run `python Resources/tools/pdf/combine_revisions.py`. Run `python Resources/tools/pdf/check_combined.py` after each combined build. It verifies every original page's text, embedded image bytes, internal/named destinations and bookmarks, then renders the combined file and all source guides and requires pixel-identical page bodies. Only the footer gains an All weeks link and a global page number. References to other files become public repository URLs so they work from a standalone downloaded copy. Inspect the rendered master index, section boundaries and folios before publishing.

Run `python Resources/tools/pdf/build_weekly.py` to build the two assignment PDFs and Week 1 revision. Use `--revision-only --week 3` to rebuild just Week 3, or select Week 2 (the revision week defaults to 1); `--practice-only` rebuilds just the 600-question PDF. The optional `revision.json` beside a revision source defines its navigation and handwritten appendix, including any explicit crop. Original page sources can be PDFs or canonical images. Run `python Resources/tools/pdf/build_practice.py` for the two browser files and their ZIP. Then run `python Resources/tools/pdf/check_weekly.py`, `python Resources/tools/pdf/update_index.py` and `python Resources/tools/pdf/check_collection.py --public-only`.

The checks require all 720 blank response groups and 3,319 blank widgets, preserve 19 original question figures pixel for pixel, check question/option text, mathematical source parts, local links, destinations, geometry and form save/reopen behavior, and render every page for visual review. Revision checks also verify source prose on its intended page, section destinations, original handwriting digests and embedded image fidelity: native JPEG streams are byte-identical; rendered PNG views are pixel-identical. Review the new renders before publishing. QA files stay under ignored `Resources/tools/pdf/qa/weekly`; private editorial references stay under ignored `.work/weekly-grading`.
