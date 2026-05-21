from pathlib import Path
from PyPDF2 import PdfReader


def load_pdf(path: Path):

    reader = PdfReader(str(path))

    return reader