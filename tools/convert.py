"""Turn AFC's flat intake PDFs into fillable PDFs.

Detects, per page:
  - runs of typed underscores  -> text fields (short runs -> checkboxes)
  - box glyphs (U+25A1, U+206F) -> checkboxes over the existing box
  - "( )" pairs                 -> checkboxes inside the parentheses
  - bare Yes / No answers       -> small checkboxes beside the word (massage form)
  - empty table cells           -> text fields (family history table)
  - "1 2 3 ... 10" pain scales  -> a small "pain level" field after the 10
Usage: convert.py in.pdf out.pdf [--yesno]
"""
import sys, re, pdfplumber, pymupdf

src, dst = sys.argv[1], sys.argv[2]
YESNO = "--yesno" in sys.argv
BOXES = {"□", "⁯"}
FILL = (0.90, 0.94, 0.99)

def line_key(c):
    return round(c["bottom"] * 2) / 2

def group_lines(chars, tol=2.0):
    lines = []
    for c in sorted(chars, key=lambda c: (c["bottom"], c["x0"])):
        if lines and abs(lines[-1][0] - c["bottom"]) <= tol:
            lines[-1][1].append(c)
        else:
            lines.append([c["bottom"], [c]])
    return [sorted(l[1], key=lambda c: c["x0"]) for l in lines]

def label_for(line_chars, x0):
    txt = "".join(c["text"] for c in line_chars if c["x1"] <= x0 + 0.5)
    txt = re.sub(r"[_□⁯]+", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip(" :#.")
    words = txt.split(" ")
    return " ".join(words[-6:]) or "Field"

doc = pymupdf.open(src)
counts = {"text": 0, "check": 0}

def add_text(page, rect, name, label, size=9):
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.rect = pymupdf.Rect(rect)
    w.field_name = name
    w.field_label = label
    w.text_font = "Helv"
    w.text_fontsize = size
    w.fill_color = FILL
    w.border_width = 0
    page.add_widget(w)
    counts["text"] += 1

def add_check(page, rect, name, label, border=False):
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.rect = pymupdf.Rect(rect)
    w.field_name = name
    w.field_label = label
    w.field_value = False
    w.border_width = 0.8 if border else 0
    if border:
        w.border_color = (0.2, 0.2, 0.2)
        w.fill_color = (1, 1, 1)
    page.add_widget(w)
    counts["check"] += 1

with pdfplumber.open(src) as pdf:
    for pno, pp in enumerate(pdf.pages):
        page = doc[pno]
        n = 0
        def nm():
            global n
        taken = []  # rects already used, to avoid overlaps
        def free(r):
            for t in taken:
                # allow ~1.5pt of overlap: tightly spaced lines touch slightly
                if not (r[2] <= t[0] + 1.5 or r[0] >= t[2] - 1.5 or r[3] <= t[1] + 1.5 or r[1] >= t[3] - 1.5):
                    return False
            return True

        idx = [0]
        def fname(kind):
            idx[0] += 1
            return f"p{pno+1}_{kind}{idx[0]}"

        # ---- table cells (do first so underscores inside tables are skipped)
        def cell_text(cell):
            if not cell: return ""
            x0, top, x1, bottom = cell
            cs = [c for c in pp.chars if x0 <= (c["x0"] + c["x1"]) / 2 <= x1 and top <= (c["top"] + c["bottom"]) / 2 <= bottom]
            cs.sort(key=lambda c: (round(c["top"]), c["x0"]))
            return re.sub(r"\s+", " ", "".join(c["text"] for c in cs)).strip()
        for tb in pp.find_tables():
            for row in tb.rows[1:]:
                first = None
                for ci, cell in enumerate(row.cells):
                    if cell is None:
                        continue
                    x0, top, x1, bottom = cell
                    txt = cell_text(cell)
                    if ci == 0:
                        first = txt
                        continue
                    if txt:
                        continue
                    hdr = tb.rows[0].cells[ci]
                    htxt = cell_text(hdr)
                    r = (x0 + 1, top + 1, x1 - 1, bottom - 1)
                    add_text(page, r, fname("cell"), f"{first} - {htxt}", 8)
                    taken.append(r)

        lines = group_lines(pp.chars)
        for lc in lines:
            # ---- underscore runs
            runs, cur = [], []
            for c in lc:
                if c["text"] == "_" and (not cur or c["x0"] - cur[-1]["x1"] <= 1.5):
                    cur.append(c)
                else:
                    if cur: runs.append(cur)
                    cur = [c] if c["text"] == "_" else []
            if cur: runs.append(cur)
            for run in runs:
                x0, x1 = run[0]["x0"], run[-1]["x1"]
                size = run[0]["size"]
                base = max(c["bottom"] for c in run) - size * 0.18
                label = label_for(lc, x0)
                if x1 - x0 < 18:
                    s = min(9, size * 0.85)
                    r = (x0 + (x1 - x0 - s) / 2, base - s - 0.5, x0 + (x1 - x0 + s) / 2, base - 0.5)
                    if free(r):
                        add_check(page, r, fname("chk"), label, border=True)
                        taken.append(r)
                    continue
                h = max(10.5, size * 1.15)
                r = (x0, base - h + 1.5, x1, base + 1.5)
                if free(r):
                    add_text(page, r, fname("txt"), label, min(9.5, size))
                    taken.append(r)

            # ---- box glyphs
            for c in lc:
                if c["text"] in BOXES:
                    cx = (c["x0"] + c["x1"]) / 2
                    # tiny Calibri boxes (U+25A1): draw a bigger bordered box over them
                    small = c["text"] == "□"
                    s = 8.5 if small else max(6.5, min(10, c["x1"] - c["x0"]))
                    cy = c["bottom"] - c["size"] * (0.46 if small else 0.42)
                    r = (cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)
                    if free(r):
                        nxt = "".join(x["text"] for x in lc if x["x0"] > c["x1"])[:40]
                        add_check(page, r, fname("box"), re.sub(r"[□⁯_]", "", nxt).strip()[:40] or "Check", border=small)
                        taken.append(r)

            # ---- "( )" pairs
            for i, c in enumerate(lc):
                if c["text"] == "(":
                    for d in lc[i + 1:i + 7]:
                        if d["text"] == ")" and d["x0"] - c["x1"] < 12:
                            s = 7
                            cx = (c["x1"] + d["x0"]) / 2
                            cy = (c["top"] + c["bottom"]) / 2
                            r = (cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)
                            if free(r):
                                nxt = "".join(x["text"] for x in lc if x["x0"] > d["x1"])[:40].strip()
                                add_check(page, r, fname("paren"), nxt or label_for(lc, c["x0"]))
                                taken.append(r)
                            break
                        if d["text"] not in " ":
                            break

            # ---- words on this line (for Yes/No and pain scales)
            words, w = [], []
            for c in lc + [None]:
                if c is None or c["text"].isspace() or (w and c["x0"] - w[-1]["x1"] > 1.2):
                    if w: words.append(w)
                    w = [] if (c is None or c["text"].isspace()) else [c]
                else:
                    w.append(c)
            texts = ["".join(x["text"] for x in ww) for ww in words]

            if YESNO:
                for ww, t in zip(words, texts):
                    if t in ("Yes", "No"):
                        s = 8
                        x = ww[-1]["x1"] + 2
                        cy = (ww[0]["top"] + ww[0]["bottom"]) / 2 + 0.5
                        r = (x, cy - s / 2, x + s, cy + s / 2)
                        if free(r):
                            add_check(page, r, fname("yn"), f"{label_for(lc, ww[0]['x0'])} - {t}", border=True)
                            taken.append(r)

            # pain scale "1 2 3 4 5 6 7 8 9 10"
            seq = [str(i) for i in range(1, 11)]
            for k in range(len(texts) - 9):
                if texts[k:k + 10] == seq:
                    last = words[k + 9][-1]
                    r = (last["x1"] + 10, last["bottom"] - 11, last["x1"] + 60, last["bottom"] + 1)
                    if free(r):
                        add_text(page, r, fname("pain"), "Pain level 1 to 10", 9)
                        taken.append(r)

doc.save(dst, garbage=3, deflate=True)
print(dst, counts)
