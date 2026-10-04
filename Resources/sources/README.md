# Source material and provenance

[Resource guide](../README.md) · [Handwritten index](../Handwritten%20Index.md) · [Lecture sources](../Sources.md)

`handwritten/` contains all 128 complete readable notebook-page images. `part1` and `scan` preserve the earlier 24- and four-page notebooks; `scan-a` through `scan-e` preserve the later scans; `notebook-atpg` preserves the separate backtracking/redundancy page. Keep these filenames stable because the handwritten index and daily notes use them as source identities.

[handwritten-inventory.json](handwritten-inventory.json) records the SHA-256 and page count of eight readable original PDFs, plus a hash and original page position for every image. [study-register.json](study-register.json) maps newer pages to days and explanation anchors and records completion through course Lesson 54. The [October upload register](october-source-register.json) preserves the original incoming names.

The earlier [Part 1 original](handwritten/Part-1-original.pdf) and [Part 2 original](handwritten/Part-2-original.pdf) are published here. Later raw PDFs remain in the [local archive](../Data/README.md); their complete page images remain published. The inventory distinguishes those storage roles so a clone can verify its images without claiming to have reread an absent raw PDF.

`lectures/week12/` holds the official decks used for clock-tree synthesis, routing, signoff and the final tutorial. [lecture-captures.json](lecture-captures.json) records maintained frame hashes; [wrapup-lessons.json](wrapup-lessons.json) records the final lesson/video identities; [wrapup-captures.json](wrapup-captures.json) preserves the October crop provenance, including local raw-capture paths. Those local raw files are optional import inputs, not reader dependencies.

Add or correct mappings alongside the note that uses the source. A captured slide supports what is visible at its timestamp; authored calculations state their own assumptions. Raw transcript reviews and render reports stay in the ignored QA directory.
