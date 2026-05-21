def extract_text(pdf):

    text = ""

    for page in pdf.pages:
        text += page.extract_text() or ""

    return text