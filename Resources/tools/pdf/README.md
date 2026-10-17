# Build and verify the reading collection

[Maintenance tools](../README.md) · [Editable notes](../../Daily%20Notes/README.md) · [Study examples](../../examples/README.md)

The nine Markdown files in `Resources/Daily Notes` are authoritative content sources. `build_notes.py` exports them with contents, hierarchical bookmarks, embedded Cambria/Consolas fonts, vector formulas, revision routes, worked revision answers and an internal handwritten-page finder. `build_references.py` exports the glossary and two-page flow guide alongside the daily PDFs in `PDFs`. All editable material and tools remain inside `Resources`.

`update_index.py` refreshes the master, daily and complete-PDF indexes from actual page counts, includes individual download links and a complete-repository ZIP link, and retains the Synopsys guides. It can refresh indexes in a fresh clone without local QA manifests. `check_handwriting.py` matches every original handwritten JPEG byte for byte against the actual image stream embedded at its named PDF destination; all 128 complete pages must be present without resizing or recompression.

`build_synopsys_plan.py` separately builds the [Synopsys project plan](../../Synopsys%20RTL%20to%20GDS%20Project%20Plan.md) into its indexed PDF. Run it with the Codex bundled Python runtime and its ReportLab/pypdf packages. It records actual section destinations, page count, source/PDF hashes and link counts under ignored `qa/synopsys-plan`; render the current PDF with Poppler and inspect every page before delivery. If pagination changes, update its page references in the reader indexes.

`build_synopsys_tool_map.py` builds the separate single-page [process and tool map](../../Synopsys%20RTL%20to%20GDS%20Tool%20Map.md), using the same bundled runtime and font setup. It verifies one-page output and confirms that the full project plan and its source retain their original hashes.

The checked production environment uses Windows with Cambria and Consolas installed, Python and the versions in [requirements.txt](requirements.txt). Poppler's `pdftoppm` must be on PATH, or `PDFTOPPM` must name its executable. The numerical/HDL checks additionally need Icarus Verilog; Tcl examples use Python's Tcl/Tk support. Fonts and Poppler are external prerequisites, not installed by the builder.

For a new environment, install the Python requirements into a suitable virtual environment. Existing bundled dependencies can remain in ignored `vendor`. Run the following from the repository root in order:

```text
python Resources/examples/run_checks.py
python Resources/examples/check_new_study_examples.py
python Resources/examples/check_wrapup_examples.py
python Resources/examples/check_depth_examples.py
python Resources/tools/pdf/build_notes.py
python Resources/tools/pdf/build_references.py
python Resources/tools/pdf/update_index.py
python Resources/tools/pdf/check_notes.py
python Resources/tools/pdf/check_navigation.py
python Resources/tools/pdf/check_handwriting.py
python Resources/tools/pdf/check_references.py
python Resources/tools/pdf/check_quiz.py
python Resources/tools/pdf/check_collection.py
```

The references resolve destinations into daily PDFs, so build the days first. To rebuild one day, pass its number to `build_notes.py`, `check_notes.py` and `check_navigation.py`; rebuild references too if a linked heading or destination changed. Recheck source hashes after editing rather than reusing evidence from an older export.

`check_collection.py` discovers maintained Markdown recursively and checks paths/anchors, 54 lessons, 128 original-page mappings/image hashes and lecture-capture hashes. It validates every available raw original against the inventory. Add `--require-originals` for all eight local raw PDFs, or `--public-only` for published material alone. A fresh clone does not require ignored later uploads.

The PDF checks compare source paragraphs, figures and complete code; verify bookmarks, destinations, footers and links; and inspect page geometry. They render every daily page into `qa/dayNN-pages-*` and four-page contact sheets into `qa/dayNN-sheet-*`. Current reference renders go into `qa/references/flow-pages-*` and `qa/references/glossary-pages-*`; match the page count and modification time to the current export. Open each changed page or legible contact sheet, inspect formulas/tables/figures/code, and record the review against the exact PDF hash before committing. Automated geometry and text checks cannot judge interpretation or visual quality by themselves.

Check representative notes in the published GitHub preview too, including an image and its following explanation, inline math and display equations. For percentages, write the decimal ratio inside math and the percentage in ordinary text, such as `$300/400=0.75$, or 75%`; this is the notation verified in the published collection. Display yield models as fractions and explain conversion to percent in the following paragraph.

`check_quiz.py` checks the existing Week 7/8 worksheet without changing it: the exact question/option sequence, six embedded figure pixel sets, 161 empty option circles, bookmark destinations, index/footer/source links and page bounds. It renders all nine pages in `qa/quiz/pages-9` for visual review and compares against the original local capture when available. This closes the separate worksheet's verification gap in the reading-collection workflow.

`build_quiz.py` separately regenerates the question-only worksheet when its source is intentionally edited. It is not part of routine note edits. Historical import scripts are documented in [sources](../sources/README.md); they are not rebuild steps.

The [weekly collection](../../weekly/README.md) uses `build_weekly.py` for the 12-week original-question PDF, the 600-question practice PDF and selected weekly revision. Week 1 is eight pages; Week 2 is nine typed pages plus four handwritten appendix pages; Week 3 is ten typed pages plus six original handwritten pages. Their editable sources and original figures live in `Resources/weekly`. Use `--revision-only --week 3` to rebuild Week 3 without changing other PDFs; the default revision week is 1. Use `--practice-only` for just the practice export. An optional `revision.json` defines section links and original handwritten-page views from PDFs or canonical image files, with source digests. `build_practice.py` generates two self-contained browser files and their download ZIP in `Assignments/Practice`; each offers independent weekly attempts, saved choices, backup import/export and score-only marking after the attempt is finished. Rebuild these after editing either question bank. `check_weekly.py` verifies blank forms, source text, source figure pixels, revision text and handwriting (including native JPEG-byte preservation), links, destinations, page geometry and form save/reopen behavior, and creates contact sheets for visual review. Week 3's `verify_revision.py` separately checks its Verilog semantics with the installed Icarus tools. Refresh the indexes with `update_index.py` after pagination changes.

The primary reader download is `Revision/Combined Revision.pdf`, currently 38 pages: a master index and all 37 pages from Weeks 1-3. `combine_revisions.py` discovers prepared weeks automatically, prefixes their named destinations to avoid collisions, imports each outline under its week, and adds global folios and All weeks footer links. Weekly builds call it automatically; run it separately to refresh just the combined download. Its filename stays stable when Week 4 or later weeks are requested. `check_combined.py` validates every original internal link, named destination, source text and image stream, bookmarks and page geometry. It renders the combined and individual PDFs at the same resolution and requires each page body to be pixel-identical to its weekly source. QA renders, source digests and checks remain under ignored `qa/weekly/combined`. Run this checker and inspect the new index and every changed footer after a combined rebuild. The index updater refreshes coverage, page counts and all revision download tables from the actual PDFs.
