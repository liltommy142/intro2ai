from pathlib import Path
import json

import pymupdf
from PIL import Image, ImageDraw


ROOT = Path(r"D:\Study\intro2ai")
PDF_DIR = ROOT / "output" / "pdf"
RENDER_ROOT = ROOT / "tmp" / "pdfs" / "renders"
RENDER_ROOT.mkdir(parents=True, exist_ok=True)

pdfs = [
    PDF_DIR / "DE-CUONG-ON-FINAL-CSC14003.pdf",
    PDF_DIR / "CHEATSHEET-FINAL-CSC14003.pdf",
]

results = []
for pdf_path in pdfs:
    doc = pymupdf.open(pdf_path)
    target = RENDER_ROOT / pdf_path.stem
    target.mkdir(parents=True, exist_ok=True)
    page_files = []
    chars = []
    blocks_outside = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        chars.append(len(text.strip()))
        rect = page.rect
        for block in page.get_text("blocks"):
            x0, y0, x1, y1 = block[:4]
            if x0 < -1 or y0 < -1 or x1 > rect.width + 1 or y1 > rect.height + 1:
                blocks_outside.append({"page": i + 1, "bbox": [x0, y0, x1, y1]})
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.55, 1.55), alpha=False)
        page_file = target / f"page-{i+1:02d}.png"
        pix.save(page_file)
        page_files.append(page_file)

    thumbs = []
    thumb_w = 380
    label_h = 26
    for idx, pf in enumerate(page_files, start=1):
        img = Image.open(pf).convert("RGB")
        thumb_h = round(img.height * thumb_w / img.width)
        img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        card = Image.new("RGB", (thumb_w, img.height + label_h), "white")
        card.paste(img, (0, label_h))
        draw = ImageDraw.Draw(card)
        draw.text((8, 6), f"Trang {idx}", fill="black")
        thumbs.append(card)

    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    cell_h = max(t.height for t in thumbs)
    sheet = Image.new("RGB", (cols * thumb_w, rows * cell_h), "#D0D0D0")
    for i, thumb in enumerate(thumbs):
        x = (i % cols) * thumb_w
        y = (i // cols) * cell_h
        sheet.paste(thumb, (x, y))
    contact = RENDER_ROOT / f"{pdf_path.stem}-CONTACT.png"
    sheet.save(contact, quality=92)

    results.append({
        "file": str(pdf_path),
        "size_bytes": pdf_path.stat().st_size,
        "pages": len(doc),
        "page_text_chars": chars,
        "empty_pages": [i + 1 for i, n in enumerate(chars) if n < 80],
        "blocks_outside_page": blocks_outside,
        "contact_sheet": str(contact),
    })

manifest = RENDER_ROOT / "validation.json"
manifest.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(manifest.read_text(encoding="utf-8"))
