def parse_text(raw_text: str, mode: str, source: str):

    # CLEAN RAW TEXT
    cleaned = raw_text.replace("\n", " ")
    cleaned = " ".join(cleaned.split())  # normalize spacing

    if mode == "text":
        return [{
            "source": source,
            "content": cleaned
        }]

    elif mode == "lines":
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

        return [
            {
                "source": source,
                "content": line
            }
            for line in lines
        ]

    elif mode == "sentences":
        import re

        # Split into sentences using punctuation
        sentences = re.split(r'(?<=[.!?])\s+', cleaned)

        results = []

        for i, s in enumerate(sentences):

            s = s.strip()
            if not s:
                continue

            if i == 0:
                results.append({
                    "source": source,
                    "content": s
                })
            else:
                results.append({
                    "content": s
                })

        return results

    else:
        return []