from bs4 import BeautifulSoup

def parse_measurements(html: str):
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if not table:
        return []

    header_cells = table.find_all("th")
    headers = [h.get_text(strip=True) for h in header_cells]
    if not headers:
        first_row = table.find("tr")
        if first_row:
            headers = [c.get_text(strip=True) for c in first_row.find_all(["th", "td"])]

    rows = table.find_all("tr")
    data_rows = rows[1:] if len(rows) > 1 else []

    measurements = []
    for r in data_rows:
        cols = [c.get_text(" ", strip=True) for c in r.find_all("td")]
        if not cols:
            continue

        item = {}
        for i, val in enumerate(cols):
            key = headers[i] if i < len(headers) and headers[i] else f"col_{i}"
            item[key] = val

        measurements.append(item)

    return measurements
