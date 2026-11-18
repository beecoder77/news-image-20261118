#!/usr/bin/env python3
"""Build the front page for the 18 November 2026 world-news image entry.

Takes the six-panel text-free collage (generated in-session) and lays it
out as a newspaper front page: masthead, date line, the six panels in a
2 x 3 grid, each with a short factual caption drawn from the research
notes for Wednesday 18 November 2026.

Usage:
    python3 composite.py [panels.png] [entry.png]

Defaults: panels image is ../work/media-generation-news-panels-18nov-0-0f687632-6973-4c22-b36d-f0d89ce6d1ac.png
relative to this script; output is entry.png next to this script.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DEFAULT_PANELS = (
    HERE.parent
    / "work"
    / "media-generation-news-panels-18nov-0-0f687632-6973-4c22-b36d-f0d89ce6d1ac.png"
)

W = H = 1024
MARGIN = 16
GUTTER = 10
COL_W = 324
MASTHEAD_H = 118
GRID_Y0 = 124
ROW_H = 436
IMG_H = 330

PAPER = (247, 244, 236)
INK = (20, 20, 20)
RULE = (140, 29, 24)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
TITLE_FONT = ImageFont.truetype(str(FONT_DIR / "DejaVuSerif-Bold.ttf"), 46)
DATE_FONT = ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 22)
CAPTION_FONT = ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 18)

# One short factual caption per panel, in grid order (left to right,
# top row then bottom row). Facts match the research notes exactly.
CAPTIONS = [
    "Kerch Bridge road arch collapses; Russia hits Kyiv bridges",
    "Iran drones hit US radar base in Bahrain, third attack in days",
    "Tanker MT TARA GAS hit twice in Hormuz; one seafarer missing",
    "Nvidia posts $115.8B quarter; board says Huang will not return",
    "APEC opens in Shenzhen; first Trump\u2013Xi\u2013Putin meeting Thursday",
    "Cyclone Akvan forecast to hit India's east coast Friday",
]


def white_runs(lengths):
    """Group consecutive indexes in `lengths` into (start, end) runs."""
    runs = []
    start = None
    prev = None
    for i in lengths:
        if start is None:
            start = prev = i
        elif i == prev + 1:
            prev = i
        else:
            runs.append((start, prev + 1))
            start = prev = i
    if start is not None:
        runs.append((start, prev + 1))
    return runs


def find_panels(img):
    """Locate the 3 x 2 panel rectangles by their white gutters.

    A column (or row) counts as gutter when at least 98% of its pixels
    are near-white. The white runs split the image into panel spans.
    Falls back to equal thirds/halves if detection fails.
    """
    gray = img.convert("L")
    px = gray.load()
    w, h = img.size

    white_cols = [
        x for x in range(w)
        if sum(1 for y in range(h) if px[x, y] > 235) >= 0.98 * h
    ]
    white_rows = [
        y for y in range(h)
        if sum(1 for x in range(w) if px[x, y] > 235) >= 0.98 * w
    ]
    col_runs = white_runs(white_cols)
    row_runs = white_runs(white_rows)

    def spans(runs, size):
        if len(runs) < 2:
            return None
        out = []
        for (a_start, a_end), (b_start, _b_end) in zip(runs, runs[1:]):
            out.append((a_end, b_start))
        if len(out) != 3 and len(runs) == 4:
            # outer frame + two gutters -> three panels
            pass
        return out

    # Columns: expect outer frame, gutter, gutter, outer frame -> 3 spans.
    # Rows: expect outer frame, gutter, outer frame -> 2 spans.
    x_spans = spans(col_runs, w)
    y_spans = spans(row_runs, h)
    if not x_spans or len(x_spans) != 3:
        x_spans = [(w * i // 3, w * (i + 1) // 3) for i in range(3)]
    if not y_spans or len(y_spans) != 2:
        y_spans = [(h * i // 2, h * (i + 1) // 2) for i in range(2)]
    return [
        (x0, y0, x1, y1)
        for (y0, y1) in y_spans
        for (x0, x1) in x_spans
    ]


def crop_to_ratio(img, ratio):
    """Centre-crop `img` to width/height == ratio."""
    w, h = img.size
    cur = w / h
    if cur > ratio:  # too wide: trim sides
        nw = int(h * ratio)
        x0 = (w - nw) // 2
        return img.crop((x0, 0, x0 + nw, h))
    nw_h = int(w / ratio)
    y0 = (h - nw_h) // 2
    return img.crop((0, y0, w, y0 + nw_h))


def wrap_caption(draw, text, max_w):
    """Wrap `text` into lines that fit `max_w` pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=CAPTION_FONT) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build(panels_path, out_path):
    src = Image.open(panels_path).convert("RGB")
    panels = find_panels(src)
    assert len(panels) == 6, f"expected 6 panels, found {len(panels)}"

    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead.
    title = "THE WORLD IN A DAY"
    tw = draw.textlength(title, font=TITLE_FONT)
    draw.text(((W - tw) / 2, 12), title, font=TITLE_FONT, fill=INK)
    date_line = "Wednesday 18 November 2026"
    dw = draw.textlength(date_line, font=DATE_FONT)
    draw.text(((W - dw) / 2, 70), date_line, font=DATE_FONT, fill=RULE)
    draw.line([(MARGIN, 106), (W - MARGIN, 106)], fill=INK, width=2)
    draw.line([(MARGIN, 111), (W - MARGIN, 111)], fill=INK, width=1)

    # Panels + captions.
    for idx, (x0, y0, x1, y1) in enumerate(panels):
        col = idx % 3
        row = idx // 3
        cell_x = MARGIN + col * (COL_W + GUTTER)
        cell_y = GRID_Y0 + row * (ROW_H + GUTTER)

        panel = crop_to_ratio(src.crop((x0, y0, x1, y1)), COL_W / IMG_H)
        panel = panel.resize((COL_W, IMG_H), Image.LANCZOS)
        page.paste(panel, (cell_x, cell_y))
        draw.rectangle(
            [cell_x, cell_y, cell_x + COL_W - 1, cell_y + IMG_H - 1],
            outline=INK,
            width=1,
        )

        lines = wrap_caption(draw, CAPTIONS[idx], COL_W - 8)
        line_h = 23
        total_h = line_h * len(lines)
        text_y = cell_y + IMG_H + 10 + max(0, (ROW_H - IMG_H - 10 - total_h) // 2)
        for line in lines:
            lw = draw.textlength(line, font=CAPTION_FONT)
            draw.text(
                (cell_x + (COL_W - lw) / 2, text_y),
                line,
                font=CAPTION_FONT,
                fill=INK,
            )
            text_y += line_h

    page.save(out_path, format="PNG", optimize=True)
    size = Path(out_path).stat().st_size
    if size > 1048576:
        # Same pixels, JPEG bytes in entry.png: the rules allow a JPEG
        # told apart by its first bytes under the name entry.png.
        page.save(out_path, format="JPEG", quality=90, optimize=True)
        size = Path(out_path).stat().st_size
    print(f"wrote {out_path}: {page.size[0]}x{page.size[1]} px, {size} bytes")
    return size


if __name__ == "__main__":
    panels_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PANELS
    out_arg = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "entry.png"
    build(panels_arg, out_arg)
