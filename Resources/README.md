# Resources

[Master index](../README.md) · [Daily notes](../Daily%20Notes/README.md) · [PDF collection](../PDFs/README.md)

The reader references are [Full Forms](../Full%20Forms.pdf) and [RTL to GDS Flow](../RTL%20to%20GDS%20Flow.pdf). Their maintained content sources are [Glossary](Glossary.md) and [Flow Map](Flow%20Map.md). The flow guide explains implementation theory and the NPTEL teaching approach; detailed tool tutorials remain in the relevant daily lessons.

[Handwritten Index](Handwritten%20Index.md) locates all 60 readable source pages. [Sources](Sources.md) records lecture frames, timestamps and primary references. [Questions](Questions.md) collects corrections and doubts, and [Coverage Review](Coverage%20Review.md) records the depth review and source limits. Complete handwritten images live in `sources/handwritten`, course captures in `images/Day NN/Lesson NN`, and executable study material in [examples](examples/README.md).

The daily Markdown files in `../Daily Notes` are the content sources for all six daily PDFs in `../PDFs`. They retain the explanations, complete handwriting, worked applications and code. The PDF builder supplies typography and navigation. The [Week 7 and Week 8 practice-question source](Week%2007%20and%2008%20-%20Practice%20Questions.md) produces the [question-only worksheet](../PDFs/Week%2007%20and%2008%20-%20Practice%20Questions.pdf): 20 original questions, 161 unmarked options and six original figures. Quiz coverage does not advance the completed-lecture marker.

Raw scan PDFs remain in `Data`, locally preserved and ignored by Git. One upload is empty. Downloaded lecture decks and scratch files remain in the ignored `.work` directory. Maintained builders and checks live in `tools/pdf`; their `vendor`, `cache`, `qa`, `logs` and `history` subdirectories are ignored. The earlier course-position PDF is preserved in local history because its progress marker is superseded.

Append each completed lesson to its six-lesson study day, preserve each source-page identity and explanation, update sources and the handwriting index, and rebuild the affected PDF. Counts come from actual files; playlist availability does not establish completion.

Run the maintained workflow from the repository root, with Python and the dependencies available:

```text
python Resources/tools/pdf/build_references.py
python Resources/tools/pdf/build_notes.py
python Resources/tools/pdf/check_notes.py
python Resources/tools/pdf/check_navigation.py
python Resources/tools/pdf/check_references.py
python Resources/tools/pdf/check_collection.py
python Resources/tools/pdf/update_index.py
```

Run `python Resources/tools/pdf/build_quiz.py` to rebuild the worksheet. Pass a day number to the daily builder and checker to update only that day. Daily builds need ReportLab, pypdf, Pillow, Matplotlib, svglib and markdown-it-py; checks also use pdfplumber and Poppler. The reference builder needs ReportLab and pypdf. Local dependencies and QA artifacts stay inside `tools/pdf`.

Verification covers Markdown paths and anchors, all 60 original-page mappings, four readable source-PDF page counts, 32 completed lessons, lecture-capture hashes, complete code, paragraph coverage, bookmarks, contents links, figure back-links, cross-document destinations and page geometry. Render the latest changed pages for visual inspection before publishing.
