# Resources

[Master reading index](../README.md) · [Daily PDFs](documents/README.md)

Use [Handwritten Index](Handwritten%20Index.md) to locate all 60 readable source pages, [Glossary](Glossary.md) for full forms, [Flow Map](Flow%20Map.md) for stage purposes, [Questions](Questions.md) for corrections, and [Sources](Sources.md) for lecture timestamps. [Coverage Review](Coverage%20Review.md) records the source-to-note depth review for every day and the remaining source limits.

Reader-facing PDFs live in `documents`. Editable daily notes live at the repository root. Complete handwritten images live in `sources/handwritten`; actual lecture frames and comparison crops live in `images/Day NN/Lesson NN`. Examples live in `examples`.

The PDFs use a formal reading style with concise source captions. The daily Markdown files are the single content source for all six PDFs, including definitions, page-specific reasoning, worked applications and code. The builder supplies layout and navigation; it does not append a second copy of lesson explanations.

Raw new scan PDFs are renamed and preserved in `Data`, which is local and ignored by Git. One upload is empty. Downloaded decks and review scratch files are local in `.work`, also ignored. PDF builders are maintained in `documents/.build`; caches, dependencies and rendered QA previews are ignored. The earlier course-position PDF is retained in the builder's history folder because its old progress marker is superseded by the master index.

To maintain the collection, append the next lesson to its six-lesson day, give every source page a stable identity and explanation, update sources and the handwritten index, rebuild the changed PDF, then check all affected navigation and page layouts. Counts must come from actual files. Do not mark a lecture complete because it appears in a playlist.

The verification scripts check Markdown links and anchors, all 60 original-page mappings and four readable source-PDF page counts, all 32 completed lesson identities, lecture capture hashes, PDF source coverage, complete code, bookmark and contents destinations, figure back-links, cross-day links and page geometry. Every PDF page is rendered for visual review. [Checked examples](examples/README.md) records what the executable examples establish.

For a maintained rebuild from the repository root, use Python with the builder's dependencies available:

```text
python Resources/documents/.build/build_notes.py
python Resources/documents/.build/check_notes.py
python Resources/documents/.build/check_navigation.py
python Resources/documents/.build/check_collection.py
python Resources/documents/.build/update_index.py
```

Pass a day number to the PDF builder and checker to update only that day. The builder needs ReportLab, pypdf, Pillow, Matplotlib, svglib and markdown-it-py; the PDF checker also needs pdfplumber and Poppler. Local dependencies and QA artifacts remain inside the hidden builder directories. Raw scans and temporary previews are preserved locally; they are excluded from the portable Git collection.
