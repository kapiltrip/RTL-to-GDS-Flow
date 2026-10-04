"""Locate the external renderer without embedding one user's runtime path."""
from pathlib import Path
import os
import shutil


def pdftoppm():
    candidate = os.environ.get('PDFTOPPM') or shutil.which('pdftoppm')
    if candidate and Path(candidate).is_file():
        return Path(candidate)
    raise SystemExit('Poppler pdftoppm is required: add its bin directory to PATH '
                     'or set PDFTOPPM to the executable path.')
