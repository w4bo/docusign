import os
import yaml
from datetime import date
from pathlib import Path
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm

ITALIAN_MONTHS = [
    "gennaio",
    "febbraio",
    "marzo",
    "aprile",
    "maggio",
    "giugno",
    "luglio",
    "agosto",
    "settembre",
    "ottobre",
    "novembre",
    "dicembre",
]


def italian_date(d: date) -> str:
    return f"{d.day} {ITALIAN_MONTHS[d.month - 1]} {d.year}"


def load_config(path: str = "config.yaml") -> tuple[str, str]:
    with open(path, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    return cfg["name"], cfg["signature_path"]


def build_overlay(
    page_width: float,
    page_height: float,
    name: str,
    date_str: str,
    sig_path: str,
) -> BytesIO:
    """Return a single-page PDF (BytesIO) containing the signature block."""
    buf = BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(page_width, page_height))

    # --- layout constants ---
    margin_right = 0 * mm
    margin_bottom = 12 * mm
    block_w = 36 * mm

    font_size = 6
    line_h = 4 * mm
    img_h = 20 * mm

    # Block layout (bottom → top):
    #   margin_bottom
    #   "on: …"          line_h
    #   "by: …"          line_h
    #   [signature img]  img_h + gap
    #   "Digitally signed" line_h
    gap = 1.5 * mm
    total_h = line_h + img_h + gap + line_h + line_h  # label + img + gap + by + on

    x = page_width - margin_right - block_w
    y = margin_bottom  # bottom of the block

    c.setFont("Helvetica", font_size)

    # signature image
    if os.path.exists(sig_path):
        img = ImageReader(sig_path)
        c.drawImage(
            img,
            x,
            y - line_h,
            width=block_w,
            height=img_h,
            mask="auto",
            preserveAspectRatio=True,
            anchor="sw",
        )
    # y += img_h + gap

    # "on: {date}"  — lowest line
    c.drawString(x, y, f"on: {date_str}")
    y += line_h

    # "by: {name}"
    c.drawString(x, y, f"by: {name}")
    y += line_h

    # "Digitally signed"  — top label
    c.drawString(x, y, "Digitally signed")

    c.save()
    buf.seek(0)
    return buf


def sign_pdf(
    input_path: Path,
    output_path: Path,
    name: str,
    date_str: str,
    sig_path: str,
) -> None:
    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    total = len(reader.pages)
    for idx, page in enumerate(reader.pages):
        if idx == total - 1:  # last page only
            w = float(page.mediabox.width)
            h = float(page.mediabox.height)
            overlay_buf = build_overlay(w, h, name, date_str, sig_path)
            overlay_page = PdfReader(overlay_buf).pages[0]
            page.merge_page(overlay_page)
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as fh:
        writer.write(fh)
    print(f"  ✓  {input_path.name}  →  {output_path}")


def main() -> None:
    name, sig_path = load_config()
    date_str = italian_date(date.today())
    print(f"Signer : {name}")
    print(f"Date   : {date_str}")
    print(f"Sig    : {sig_path}")
    print()

    tosign_dir = Path("tosign")
    signed_dir = Path("signed")

    pdfs = sorted(tosign_dir.glob("*.pdf"))
    if not pdfs:
        print("No PDF files found in 'tosign/'. Nothing to do.")
        return

    for pdf_path in pdfs:
        sign_pdf(pdf_path, signed_dir / pdf_path.name, name, date_str, sig_path)

    print(f"\nDone — {len(pdfs)} file(s) signed. Output in: {signed_dir}/")


if __name__ == "__main__":
    main()
