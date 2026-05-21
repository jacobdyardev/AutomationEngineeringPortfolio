from bs4 import BeautifulSoup


def parse_elements(html: str, selector: str):

    soup = BeautifulSoup(html, "html.parser")
    return soup.select(selector)


def extract_configured(elements, fields_config, limit: int, source: str):

    extracted = []

    if limit:
        elements_to_process = elements[:limit]
    else:
        elements_to_process = elements

    for el in elements_to_process:

        row = {"source": source}

        for field in fields_config:

            name = field["name"]
            selector = field.get("selector")
            attribute = field["attribute"]

            target = el

            if selector:
                target = el.select_one(selector)

            if not target:
                value = None
            else:
                if attribute == "text":
                    value = target.get_text(strip=True)

                elif isinstance(attribute, list):
                    value = None
                    for attr in attribute:
                        value = target.get(attr)
                        if value:
                            break

                else:
                    value = target.get(attribute)

            row[name] = value

        extracted.append(row)

    return extracted