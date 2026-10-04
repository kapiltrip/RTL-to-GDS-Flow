# Build and verify the reading collection

[Maintenance tools](../README.md) · [Editable notes](../../../Daily%20Notes/README.md) · [Study examples](../../examples/README.md)

The nine daily Markdown files are authoritative content sources. `build_notes.py` exports them with contents, hierarchical bookmarks, embedded Cambria/Consolas fonts, vector formulas and figure/footer returns to contents. `build_references.py` exports the root glossary and two-page flow guide. `update_index.py` refreshes the three reader indexes from actual PDF page counts.

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
python Resources/tools/pdf/check_references.py
python Resources/tools/pdf/check_collection.py
```

The references resolve destinations into daily PDFs, so build the days first. To rebuild one day, pass its number to `build_notes.py`, `check_notes.py` and `check_navigation.py`; rebuild references too if a linked heading or destination changed. Recheck source hashes after editing rather than reusing evidence from an older export.

`check_collection.py` discovers maintained Markdown recursively and checks paths/anchors, 54 lessons, 128 original-page mappings/image hashes and lecture-capture hashes. It validates every available raw original against the inventory. Add `--require-originals` for all eight local raw PDFs, or `--public-only` for published material alone. A fresh clone does not require ignored later uploads.

The PDF checks compare source paragraphs, figures and complete code; verify bookmarks, destinations, footers and links; and inspect page geometry. They render every daily page into `qa/dayNN-pages-*` and four-page contact sheets into `qa/dayNN-sheet-*`. Current reference renders go into `qa/references/flow-pages-*` and `qa/references/glossary-pages-*`; match the page count and modification time to the current export. Open each changed page or legible contact sheet, inspect formulas/tables/figures/code, and record the review against the exact PDF hash before committing. Automated geometry and text checks cannot judge interpretation or visual quality by themselves.

`build_quiz.py` separately regenerates the Week 7/8 question-only worksheet. It preserves the original questions/options/figures and is not part of routine note edits. Historical import scripts are documented in [sources](../sources/README.md); they are not rebuild steps.
