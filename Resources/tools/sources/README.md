# Historical October source import

[Maintenance tools](../README.md) · [Routine PDF workflow](../pdf/README.md) · [Provenance](../../sources/README.md)

These scripts preserve how the October course wrap-up was imported. They contain specific incoming names, screenshot rectangles and text migration rules from that import. They are not a general notebook importer and must not run during routine explanation edits.

| Script | Historical role |
|---|---|
| [prepare_wrapup_sources.py](prepare_wrapup_sources.py) | Preserve incoming PDFs, copy page images and retain original identities |
| [process_wrapup_captures.py](process_wrapup_captures.py) | Crop observed Chrome player rectangles and record frame hashes |
| [finalize_wrapup.py](finalize_wrapup.py) | Migrate the final lessons and their source/index metadata |
| [update_wrapup_review.py](update_wrapup_review.py) | Add the original wrap-up reference and review text |

Running a historical importer requires the explicit `--apply-historical-import` command-line flag. Review its input paths and migration rules first: some use ignored raw captures, transcripts or downloads, and the text migrations could replace subsequent editorial work. Current maintenance edits Markdown/registers directly and uses the PDF builders and checks. Original uploads are never reconstructed from the edited study notes.
