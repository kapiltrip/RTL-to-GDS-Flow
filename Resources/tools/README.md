# Maintenance tools

[Resource guide](../README.md) · [Study checks](../examples/README.md)

| Folder | Role |
|---|---|
| [pdf](pdf/README.md) | Maintained reader/reference/worksheet builders, index updates and PDF checks |
| [sources](sources/README.md) | Historical October import helpers, separated from ordinary rebuilding |

Run commands from the repository root. Content belongs in the daily Markdown and resource references; production scripts supply formatting and verification. Numerical and HDL teaching checks live with the executable examples.

PDF tools use ignored `vendor`, `cache`, `qa`, `logs` and `history` folders for local dependencies and work products. Generated final reader PDFs are versioned in the root and `PDFs`; temporary page renders and simulation outputs are not published.
