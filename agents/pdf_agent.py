from tika import parser
import re

def process_pdf(file_content: bytes):
    parsed = parser.from_buffer(file_content)
    text = parsed.get("content", "")

    flags = []
    total_value = 0

    # Look for total invoice amount
    match = re.search(r"Total\s*[:=\s]\s*\$?([\d,]+\.\d{2})", text, re.IGNORECASE)
    if match:
        try:
            total_value = float(match.group(1).replace(",", ""))
            if total_value > 10000:
                flags.append("Invoice total exceeds $10,000")
        except ValueError:
            pass

    # Look for regulation keywords
    keywords = ["GDPR", "HIPAA", "FDA", "ISO", "SOX"]
    found_keywords = [kw for kw in keywords if kw in text.upper()]
    if found_keywords:
        flags.append(f"Mentions regulation(s): {', '.join(found_keywords)}")

    return {
        "source": "pdf",
        "invoice_total": total_value,
        "regulations_found": found_keywords,
        "action": "flag_risk" if flags else "log",
        "flags": flags,
        "summary": text[:500]  # Optional
    }
