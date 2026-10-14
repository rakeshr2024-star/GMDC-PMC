"""Custom ReportLab flowables: flowcharts, network diagram, Gantt and charts."""
from __future__ import annotations

import math

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable, Paragraph

# ---------------------------------------------------------------- palette ---
INK = HexColor("#1d2433")
INK2 = HexColor("#52514e")
MUTED = HexColor("#8a8985")
GRID = HexColor("#e4e3df")
SURF = HexColor("#fcfcfb")
NAVY = HexColor("#12355b")
CRIT = HexColor("#d03b3b")
GOOD = HexColor("#0ca30c")
WARN = HexColor("#fab219")
SERIOUS = HexColor("#ec835a")

PHASE_COL = {
    "AUC": HexColor("#2a78d6"),
    "MOB": HexColor("#eb6834"),
    "MPL": HexColor("#1baf7a"),
    "ENV": HexColor("#eda100"),
    "FOR": HexColor("#e87ba4"),
    "LAR": HexColor("#008300"),
    "OPN": HexColor("#6250d6"),
}
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

FONT = "Carlito"
FONT_B = "Carlito-Bold"
FONT_I = "Carlito-Italic"
SYM = "DejaVuSans"


def tint(c, f=0.85):
    """Mix colour c with white; f = share of white."""
    return colors.Color(c.red + (1 - c.red) * f, c.green + (1 - c.green) * f, c.blue + (1 - c.blue) * f)


def shade(c, f=0.25):
    return colors.Color(c.red * (1 - f), c.green * (1 - f), c.blue * (1 - f))


def _ps(size=8, leading=None, color=INK, font=FONT, align=TA_LEFT):
    return ParagraphStyle("x", fontName=font, fontSize=size, leading=leading or size * 1.18,
                          textColor=color, alignment=align)


def arrow(c, x1, y1, x2, y2, col=INK2, w=0.8, head=4.0):
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(w)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2 - y1, x2 - x1)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - head * math.cos(ang - 0.4), y2 - head * math.sin(ang - 0.4))
    p.lineTo(x2 - head * math.cos(ang + 0.4), y2 - head * math.sin(ang + 0.4))
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def poly_arrow(c, pts, col=INK2, w=0.8, head=4.0, dash=None):
    c.setStrokeColor(col)
    c.setLineWidth(w)
    if dash:
        c.setDash(*dash)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.drawPath(p, fill=0, stroke=1)
    c.setDash()
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    c.setFillColor(col)
    q = c.beginPath()
    q.moveTo(x2, y2)
    q.lineTo(x2 - head * math.cos(ang - 0.4), y2 - head * math.sin(ang - 0.4))
    q.lineTo(x2 - head * math.cos(ang + 0.4), y2 - head * math.sin(ang + 0.4))
    q.close()
    c.drawPath(q, fill=1, stroke=0)


def diamond(c, x, y, r, fill, stroke=None):
    p = c.beginPath()
    p.moveTo(x, y + r)
    p.lineTo(x + r, y)
    p.lineTo(x, y - r)
    p.lineTo(x - r, y)
    p.close()
    c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.8)
    c.drawPath(p, fill=1, stroke=1 if stroke is not None else 0)


# ============================================================ FlowChart ===
class FlowChart(Flowable):
    """Snake-layout process flow. steps: list of dict(t, who, d, crit, ms, par)."""

    def __init__(self, steps, color, width, cols=4, gap_x=16, gap_y=16, font_size=7.6):
        super().__init__()
        self.steps = steps
        self.col = color
        self.W = width
        self.cols = cols
        self.gx = gap_x
        self.gy = gap_y
        self.fs = font_size
        self.bw = (width - (cols - 1) * gap_x) / cols
        self._layout()

    def _layout(self):
        self.paras = []
        hs = []
        for i, s in enumerate(self.steps):
            p = Paragraph(s["t"], _ps(self.fs, self.fs * 1.16, INK, FONT_B if s.get("crit") else FONT))
            tag_w = (stringWidth(s["ms"], FONT_B, 6) + 22) if s.get("ms") else 0
            w, h = p.wrap(self.bw - 24 - tag_w, 400)
            sub = Paragraph(f'{s.get("who", "")}' + (f' · <font color="#12355b">{s["d"]}</font>' if s.get("d") else ""),
                            _ps(self.fs - 1.2, (self.fs - 1.2) * 1.15, INK2))
            w2, h2 = sub.wrap(self.bw - 22 - (34 if s.get("crit") else 0), 200)
            self.paras.append((p, h, sub, h2))
            hs.append(h + h2 + 11)
        self.rows = math.ceil(len(self.steps) / self.cols)
        self.rh = []
        for r in range(self.rows):
            seg = hs[r * self.cols:(r + 1) * self.cols]
            self.rh.append(max(max(seg), 34))
        self.H = sum(self.rh) + (self.rows - 1) * self.gy + 8

    def wrap(self, aw, ah):
        return self.W, self.H

    def _pos(self, i):
        r, k = divmod(i, self.cols)
        col = k if r % 2 == 0 else self.cols - 1 - k
        x = col * (self.bw + self.gx)
        ytop = self.H - 4 - sum(self.rh[:r]) - r * self.gy
        return x, ytop, self.rh[r], r, col

    def draw(self):
        c = self.canv
        n = len(self.steps)
        # connectors first
        for i in range(n - 1):
            x, yt, h, r, col = self._pos(i)
            x2, yt2, h2, r2, col2 = self._pos(i + 1)
            if r == r2:
                ym = yt - h / 2
                if col2 > col:
                    arrow(c, x + self.bw, ym, x2 - 1, ym, shade(self.col, 0.2), 1.0)
                else:
                    arrow(c, x, ym, x2 + self.bw + 1, ym, shade(self.col, 0.2), 1.0)
            else:
                xm = x + self.bw / 2
                arrow(c, xm, yt - h, xm, yt2 + 1, shade(self.col, 0.2), 1.0)
        for i, s in enumerate(self.steps):
            x, yt, h, r, col = self._pos(i)
            crit = s.get("crit")
            c.setFillColor(tint(self.col, 0.88))
            c.setStrokeColor(CRIT if crit else tint(self.col, 0.35))
            c.setLineWidth(1.6 if crit else 0.7)
            c.roundRect(x, yt - h, self.bw, h, 4, fill=1, stroke=1)
            c.setFillColor(self.col)
            c.rect(x + 0.4, yt - h + 3, 3, h - 6, fill=1, stroke=0)
            # number badge
            c.setFillColor(shade(self.col, 0.15))
            c.circle(x + 12, yt - 9, 6.2, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont(FONT_B, 6.6)
            c.drawCentredString(x + 12, yt - 11.3, str(i + 1))
            p, ph, sub, h2 = self.paras[i]
            p.drawOn(c, x + 20, yt - 4 - ph)
            sub.drawOn(c, x + 20, yt - h + 4)
            if s.get("ms"):
                diamond(c, x + self.bw - 8, yt - 8, 5.5, NAVY)
                c.setFont(FONT_B, 6)
                c.setFillColor(NAVY)
                c.drawRightString(x + self.bw - 15, yt - 10, s["ms"])
            if crit:
                c.setFillColor(CRIT)
                c.setFont(FONT_B, 5.8)
                c.drawRightString(x + self.bw - 4, yt - h + 4, "CRITICAL")


# ======================================================= Master lane map ===
class LaneMap(Flowable):
    """Swimlane process map. lanes: [(code,label)], boxes: dict id->(lane, x0, x1, text, kind),
    links: [(from,to, crit)] ; x in 0..100 units."""

    def __init__(self, width, height, lanes, boxes, links, gates=None, title_w=78):
        super().__init__()
        self.W, self.H = width, height
        self.lanes, self.boxes, self.links = lanes, boxes, links
        self.gates = gates or []
        self.tw = title_w

    def wrap(self, aw, ah):
        return self.W, self.H

    def _geom(self, bid):
        lane, x0, x1, text, kind = self.boxes[bid]
        li = [l[0] for l in self.lanes].index(lane)
        lh = (self.H - 22) / len(self.lanes)
        y_top = self.H - 22 - li * lh
        sx = (self.W - self.tw - 6) / 100.0
        bx0 = self.tw + 4 + x0 * sx
        bx1 = self.tw + 4 + x1 * sx
        return bx0, bx1, y_top - lh * 0.18, y_top - lh * 0.82, lane, kind

    def draw(self):
        c = self.canv
        lh = (self.H - 22) / len(self.lanes)
        sx = (self.W - self.tw - 6) / 100.0
        # lanes
        for i, (code, label) in enumerate(self.lanes):
            y = self.H - 22 - (i + 1) * lh
            col = PHASE_COL.get(code, NAVY)
            c.setFillColor(tint(col, 0.94) if i % 2 == 0 else colors.white)
            c.rect(0, y, self.W, lh, fill=1, stroke=0)
            c.setFillColor(col)
            c.rect(0, y + 1, 4, lh - 2, fill=1, stroke=0)
            p = Paragraph(label, _ps(7.6, 8.6, INK, FONT_B))
            w, h = p.wrap(self.tw - 10, lh)
            p.drawOn(c, 8, y + lh / 2 - h / 2)
        # gates
        for gx, glabel in self.gates:
            x = self.tw + 4 + gx * sx
            c.setStrokeColor(NAVY)
            c.setDash(2, 2)
            c.setLineWidth(0.6)
            c.line(x, 4, x, self.H - 18)
            c.setDash()
            diamond(c, x, self.H - 12, 5, NAVY)
            c.setFont(FONT_B, 6.5)
            c.setFillColor(NAVY)
            c.drawCentredString(x, self.H - 4, glabel)
        # links
        for a, b, crit in self.links:
            ax0, ax1, at, ab, al, _ = self._geom(a)
            bx0, bx1, bt, bb, bl, _ = self._geom(b)
            col = CRIT if crit else INK2
            w = 1.3 if crit else 0.6
            ay = (at + ab) / 2
            by = (bt + bb) / 2
            if al == bl:
                arrow(c, ax1, ay, bx0 - 1, by, col, w, 3.6)
            else:
                xm = max(ax1 + 3, min(bx0 - 4, (ax1 + bx0) / 2))
                if bx0 - ax1 < 8:
                    xm = ax1 - 6 if bx0 < ax1 else ax1 + 3
                    # vertical drop from box bottom/top
                    sx0 = (ax0 + ax1) / 2 if bx0 < ax1 else ax1 - 4
                    if by < ay:
                        poly_arrow(c, [(sx0, ab), (sx0, (ab + bt) / 2), (bx0 + 6, (ab + bt) / 2), (bx0 + 6, bt + 1)], col, w, 3.4)
                    else:
                        poly_arrow(c, [(sx0, at), (sx0, (at + bb) / 2), (bx0 + 6, (at + bb) / 2), (bx0 + 6, bb - 1)], col, w, 3.4)
                else:
                    poly_arrow(c, [(ax1, ay), (xm, ay), (xm, by), (bx0 - 1, by)], col, w, 3.4)
        # boxes
        for bid in self.boxes:
            x0, x1, yt, yb, lane, kind = self._geom(bid)
            col = PHASE_COL.get(lane, NAVY)
            text = self.boxes[bid][3]
            if kind == "ms":
                c.setFillColor(NAVY)
                c.setStrokeColor(NAVY)
            elif kind == "crit":
                c.setFillColor(colors.white)
                c.setStrokeColor(CRIT)
            else:
                c.setFillColor(colors.white)
                c.setStrokeColor(col)
            c.setLineWidth(1.5 if kind == "crit" else 0.9)
            c.roundRect(x0, yb, x1 - x0, yt - yb, 3, fill=1, stroke=1)
            if kind != "ms":
                c.setFillColor(col)
                c.rect(x0 + 0.5, yb + 2, 2.5, yt - yb - 4, fill=1, stroke=0)
            p = Paragraph(text, _ps(6.5, 7.3, colors.white if kind == "ms" else INK,
                                    FONT_B if kind in ("ms", "crit") else FONT, TA_CENTER))
            w, h = p.wrap(x1 - x0 - 6, yt - yb)
            p.drawOn(c, x0 + 4, (yt + yb) / 2 - h / 2)


# ======================================================= Network (AON) ===
class NetworkDiagram(Flowable):
    """Time-scaled activity-on-node diagram with phase swimlanes."""

    def __init__(self, acts, width, height, phases, months=None, title_w=70):
        super().__init__()
        self.acts = acts
        self.W, self.H = width, height
        self.phases = phases
        self.tw = title_w
        self.T = months or math.ceil(max(a.ef for a in acts) / 6) * 6

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        by = {a.id: a for a in self.acts}
        top_axis = 18
        plot_w = self.W - self.tw - 10
        sx = plot_w / self.T
        nw, nh = 25, 13
        # sub-row assignment per lane
        lanes = {p[0]: [] for p in self.phases}
        for a in sorted(self.acts, key=lambda z: z.es):
            lanes[a.phase].append(a)
        place = {}
        lane_rows = {}
        for code, items in lanes.items():
            rows_end = []
            for a in items:
                x = self.tw + a.es * sx
                for ri, end in enumerate(rows_end):
                    if x >= end + 3:
                        rows_end[ri] = x + nw
                        place[a.id] = (code, ri)
                        break
                else:
                    rows_end.append(x + nw)
                    place[a.id] = (code, len(rows_end) - 1)
            lane_rows[code] = max(1, len(rows_end))
        total_rows = sum(lane_rows.values())
        avail = self.H - top_axis - 6
        rh = avail / total_rows
        ytop = {}
        y = self.H - top_axis
        for code, _ in self.phases:
            ytop[code] = y
            y -= lane_rows[code] * rh
        # lane backgrounds
        for i, (code, label) in enumerate(self.phases):
            h = lane_rows[code] * rh
            yb = ytop[code] - h
            col = PHASE_COL[code]
            c.setFillColor(tint(col, 0.93) if i % 2 == 0 else colors.white)
            c.rect(0, yb, self.W, h, fill=1, stroke=0)
            c.setFillColor(col)
            c.rect(0, yb + 1, 3.5, h - 2, fill=1, stroke=0)
            safe = label if "&amp;" in label else label.replace("&", "&amp;")
            p = Paragraph(safe, _ps(7, 8, INK, FONT_B))
            w, hh = p.wrap(self.tw - 10, h)
            p.drawOn(c, 7, yb + h / 2 - hh / 2)
        # time axis
        c.setFont(FONT, 6.5)
        for m in range(0, self.T + 1, 6):
            x = self.tw + m * sx
            c.setStrokeColor(GRID)
            c.setLineWidth(0.4)
            c.line(x, 4, x, self.H - top_axis + 2)
            c.setFillColor(INK2)
            c.drawCentredString(x, self.H - top_axis + 6, f"M{m}")
        c.setFont(FONT_B, 6.5)
        c.drawString(self.tw - 64, self.H - top_axis + 6, "Months from T0")

        def node_xy(a):
            code, ri = place[a.id]
            x = self.tw + a.es * sx
            yc = ytop[code] - (ri + 0.5) * rh
            return x, yc

        # edges
        for a in self.acts:
            x2, y2 = node_xy(a)
            for p in a.preds:
                pa = by[p]
                x1, y1 = node_xy(pa)
                crit = pa.crit and a.crit and abs(pa.ef - a.es) < 1e-6
                col = CRIT if crit else HexColor("#9a9893")
                w = 1.4 if crit else 0.45
                xs = x1 + nw
                if x2 - xs > 6:
                    xm = x2 - 4
                    poly_arrow(c, [(xs, y1), (xm, y1), (xm, y2), (x2 - 0.5, y2)], col, w, 3.0)
                else:
                    poly_arrow(c, [(xs, y1), (xs + 2, y1), (xs + 2, y2 + (nh / 2 if y2 < y1 else -nh / 2)),
                                   (x2 + nw / 2, y2 + (nh / 2 if y2 < y1 else -nh / 2))], col, w, 3.0)
        # nodes
        for a in self.acts:
            x, yc = node_xy(a)
            col = PHASE_COL[a.phase]
            c.setFillColor(colors.white)
            c.setStrokeColor(CRIT if a.crit else col)
            c.setLineWidth(1.5 if a.crit else 0.8)
            c.roundRect(x, yc - nh / 2, nw, nh, 2.5, fill=1, stroke=1)
            c.setFillColor(CRIT if a.crit else shade(col, 0.2))
            c.setFont(FONT_B, 6.6)
            c.drawCentredString(x + nw / 2, yc + 0.2, a.id)
            c.setFont(FONT, 4.9)
            c.setFillColor(INK2)
            c.drawCentredString(x + nw / 2, yc - nh / 2 + 1.6, f"{a.te:.1f} m")
            if a.milestone and a.milestone.startswith("MS"):
                diamond(c, x + nw, yc + nh / 2, 3.6, NAVY)


# ================================================================ Gantt ===
class Gantt(Flowable):
    def __init__(self, acts, width, phases, row_h=10.6, label_w=205, months=None, start_label="T0",
                 date_fn=None):
        super().__init__()
        self.acts = acts
        self.W = width
        self.phases = phases
        self.rh = row_h
        self.lw = label_w
        self.T = months or math.ceil(max(a.lf for a in acts) / 6) * 6
        rows = len(acts) + len(phases)
        self.H = rows * row_h + 30
        self.date_fn = date_fn

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        pw = self.W - self.lw - 4
        sx = pw / self.T
        x0 = self.lw
        ytop = self.H - 22
        # axis
        for m in range(0, self.T + 1, 3):
            x = x0 + m * sx
            c.setStrokeColor(GRID if m % 6 else HexColor("#cfcdc7"))
            c.setLineWidth(0.35)
            c.line(x, 0, x, ytop)
            if m % 6 == 0:
                c.setFillColor(INK2)
                c.setFont(FONT, 6.5)
                c.drawCentredString(x, ytop + 4, f"M{m}")
        y = ytop
        for code, label in self.phases:
            items = [a for a in self.acts if a.phase == code]
            if not items:
                continue
            col = PHASE_COL[code]
            y -= self.rh
            c.setFillColor(tint(col, 0.86))
            c.rect(0, y + 1, self.W, self.rh - 1, fill=1, stroke=0)
            c.setFillColor(shade(col, 0.35))
            c.setFont(FONT_B, 7.2)
            c.drawString(3, y + 3.2, label.upper())
            es = min(a.es for a in items)
            ef = max(a.ef for a in items)
            c.setFillColor(col)
            c.rect(x0 + es * sx, y + 3.5, (ef - es) * sx, 2.4, fill=1, stroke=0)
            for a in items:
                y -= self.rh
                c.setFillColor(CRIT if a.crit else INK)
                c.setFont(FONT_B if a.crit else FONT, 6.6)
                c.drawString(3, y + 3, a.id)
                name = a.name
                maxw = self.lw - 26
                while stringWidth(name, FONT, 6.4) > maxw and len(name) > 4:
                    name = name[:-2]
                if name != a.name:
                    name = name.rstrip(" ,;-") + "…"
                c.setFont(FONT, 6.4)
                c.setFillColor(INK)
                c.drawString(22, y + 3, name)
                bx = x0 + a.es * sx
                bw = max(a.te * sx, 1.2)
                # float
                if a.tf > 0.05:
                    c.setStrokeColor(HexColor("#b9b7b1"))
                    c.setLineWidth(0.6)
                    c.setDash(1.5, 1.5)
                    c.line(bx + bw, y + self.rh / 2, x0 + a.lf * sx, y + self.rh / 2)
                    c.setDash()
                    c.line(x0 + a.lf * sx, y + 2.5, x0 + a.lf * sx, y + self.rh - 2.5)
                c.setFillColor(CRIT if a.crit else col)
                c.roundRect(bx, y + 2, bw, self.rh - 4, 1.6, fill=1, stroke=0)
                if a.milestone:
                    diamond(c, bx + bw, y + self.rh / 2, 3.4, NAVY)
                    c.setFont(FONT_B, 5.8)
                    c.setFillColor(NAVY)
                    c.drawString(bx + bw + 5, y + 2.8, a.milestone)


# =========================================================== Charts ===
class Donut(Flowable):
    def __init__(self, data, width, height, title=None, center_text=None):
        super().__init__()
        self.data, self.W, self.H, self.title, self.ct = data, width, height, title, center_text

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        r = min(self.H - 10, self.W * 0.45) / 2
        cx, cy = r + 6, self.H / 2
        tot = sum(v for _, v, _ in self.data)
        ang = 90
        for lab, v, col in self.data:
            ext = -360 * v / tot
            c.setFillColor(col)
            c.setStrokeColor(colors.white)
            c.setLineWidth(1.6)
            p = c.beginPath()
            p.moveTo(cx, cy)
            p.arcTo(cx - r, cy - r, cx + r, cy + r, ang, ext)
            p.close()
            c.drawPath(p, fill=1, stroke=1)
            ang += ext
        c.setFillColor(colors.white)
        c.circle(cx, cy, r * 0.58, fill=1, stroke=0)
        if self.ct:
            c.setFillColor(INK)
            c.setFont(FONT_B, 13)
            c.drawCentredString(cx, cy + 1, self.ct[0])
            c.setFont(FONT, 7)
            c.setFillColor(INK2)
            c.drawCentredString(cx, cy - 9, self.ct[1])
        # legend with values
        lx = cx + r + 16
        ly = cy + len(self.data) * 9
        for lab, v, col in self.data:
            c.setFillColor(col)
            c.roundRect(lx, ly - 1, 8, 8, 1.5, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont(FONT_B, 7.6)
            c.drawString(lx + 12, ly + 0.5, lab)
            c.setFont(FONT, 7.4)
            c.setFillColor(INK2)
            c.drawString(lx + 12, ly - 8, f"{v:,.1f} ha  ({100 * v / tot:.1f}%)")
            ly -= 22


class Columns(Flowable):
    """Simple single-series column chart with optional second series as line."""

    def __init__(self, xs, ys, width, height, color, ylab="", xlab="", ys2=None, col2=None, lab1="", lab2="",
                 every=2, ymax=None):
        super().__init__()
        self.xs, self.ys, self.W, self.H = xs, ys, width, height
        self.col, self.ylab, self.xlab = color, ylab, xlab
        self.ys2, self.col2, self.lab1, self.lab2 = ys2, col2, lab1, lab2
        self.every = every
        self.ymax = ymax

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        L, B, R, T = 30, 22, 6, 16
        pw, ph = self.W - L - R, self.H - B - T
        ymax = self.ymax or max(max(self.ys), max(self.ys2) if self.ys2 else 0) * 1.1
        step = 5 if ymax <= 30 else 10
        c.setFont(FONT, 6.5)
        for v in range(0, int(ymax) + 1, step):
            y = B + ph * v / ymax
            c.setStrokeColor(GRID)
            c.setLineWidth(0.4)
            c.line(L, y, L + pw, y)
            c.setFillColor(INK2)
            c.drawRightString(L - 3, y - 2, str(v))
        n = len(self.xs)
        bw = pw / n
        for i, (x, v) in enumerate(zip(self.xs, self.ys)):
            if v > 0:
                h = ph * v / ymax
                c.setFillColor(self.col)
                c.roundRect(L + i * bw + 1, B, bw - 2, h, 1.2, fill=1, stroke=0)
                c.rect(L + i * bw + 1, B, bw - 2, min(h, 2), fill=1, stroke=0)
            if i % self.every == 0:
                c.setFillColor(INK2)
                c.setFont(FONT, 6.2)
                c.drawCentredString(L + i * bw + bw / 2, B - 9, str(x))
        if self.ys2:
            c.setStrokeColor(self.col2)
            c.setLineWidth(1.6)
            pts = [(L + i * bw + bw / 2, B + ph * v / ymax) for i, v in enumerate(self.ys2)]
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            c.drawPath(p, fill=0, stroke=1)
        c.setFillColor(INK2)
        c.setFont(FONT, 6.8)
        c.drawString(L, self.H - 8, self.ylab)
        c.drawRightString(L + pw, 1, self.xlab)
        if self.ys2:
            lx = L + pw - 150
            c.setFillColor(self.col)
            c.rect(lx, self.H - 9, 8, 6, fill=1, stroke=0)
            c.setFillColor(INK)
            c.drawString(lx + 11, self.H - 9, self.lab1)
            c.setStrokeColor(self.col2)
            c.setLineWidth(1.6)
            c.line(lx + 75, self.H - 6, lx + 85, self.H - 6)
            c.drawString(lx + 88, self.H - 9, self.lab2)


class SCurve(Flowable):
    """CDF lines (Monte Carlo + PERT normal) with target markers."""

    def __init__(self, series, width, height, xlim, targets=(), xlabel="", hist=None):
        super().__init__()
        self.series, self.W, self.H = series, width, height
        self.xlim, self.targets, self.xlabel, self.hist = xlim, targets, xlabel, hist

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        L, B, R, T = 32, 26, 10, 18
        pw, ph = self.W - L - R, self.H - B - T
        x0, x1 = self.xlim

        def X(v):
            return L + pw * (v - x0) / (x1 - x0)

        def Y(p):
            return B + ph * p
        # histogram (background)
        if self.hist is not None:
            edges, counts = self.hist
            mx = max(counts)
            for i, cnt in enumerate(counts):
                xa, xb = X(edges[i]), X(edges[i + 1])
                if xb < L or xa > L + pw:
                    continue
                c.setFillColor(HexColor("#dbe9fb"))
                c.rect(max(xa, L) + 0.4, B, min(xb, L + pw) - max(xa, L) - 0.8, ph * 0.55 * cnt / mx, fill=1, stroke=0)
        c.setFont(FONT, 6.5)
        for p in [0, .2, .4, .6, .8, 1.0]:
            c.setStrokeColor(GRID)
            c.setLineWidth(0.4)
            c.line(L, Y(p), L + pw, Y(p))
            c.setFillColor(INK2)
            c.drawRightString(L - 3, Y(p) - 2, f"{int(p * 100)}%")
        stepx = 3 if (x1 - x0) <= 36 else 6
        v = math.ceil(x0 / stepx) * stepx
        while v <= x1:
            c.setFillColor(INK2)
            c.drawCentredString(X(v), B - 9, str(int(v)))
            v += stepx
        c.drawCentredString(L + pw / 2, B - 19, self.xlabel)
        for tx, tl in self.targets:
            c.setStrokeColor(NAVY)
            c.setDash(2, 2)
            c.setLineWidth(0.8)
            c.line(X(tx), B, X(tx), B + ph)
            c.setDash()
            c.setFillColor(NAVY)
            c.setFont(FONT_B, 6.6)
            c.drawCentredString(X(tx), B + ph + 4, tl)
        ly = self.H - 12
        for lab, xs, ps, col, dash in self.series:
            c.setStrokeColor(col)
            c.setLineWidth(1.8)
            if dash:
                c.setDash(3, 2)
            p = c.beginPath()
            started = False
            for xv, pv in zip(xs, ps):
                if xv < x0 or xv > x1:
                    continue
                if not started:
                    p.moveTo(X(xv), Y(pv))
                    started = True
                else:
                    p.lineTo(X(xv), Y(pv))
            c.drawPath(p, fill=0, stroke=1)
            c.setDash()
        # legend
        lx = L + 6
        for lab, xs, ps, col, dash in self.series:
            c.setStrokeColor(col)
            c.setLineWidth(1.8)
            if dash:
                c.setDash(3, 2)
            c.line(lx, ly, lx + 14, ly)
            c.setDash()
            c.setFillColor(INK)
            c.setFont(FONT, 6.8)
            c.drawString(lx + 17, ly - 2.3, lab)
            ly -= 10
        if self.hist is not None:
            c.setFillColor(HexColor("#dbe9fb"))
            c.rect(lx, ly - 3, 14, 6, fill=1, stroke=0)
            c.setFillColor(INK)
            c.drawString(lx + 17, ly - 2.3, "Simulated distribution (histogram)")


class HBars(Flowable):
    def __init__(self, items, width, row_h=12, label_w=190, maxv=1.0, fmt="{:.0%}", color=None):
        super().__init__()
        self.items, self.W, self.rh, self.lw, self.maxv, self.fmt = items, width, row_h, label_w, maxv, fmt
        self.color = color
        self.H = len(items) * row_h + 14

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        pw = self.W - self.lw - 34
        y = self.H - 4
        for lab, v, col in self.items:
            y -= self.rh
            c.setFillColor(INK)
            c.setFont(FONT, 6.9)
            t = lab
            while stringWidth(t, FONT, 6.9) > self.lw - 6 and len(t) > 4:
                t = t[:-2]
            if t != lab:
                t = t.rstrip() + "…"
            c.drawString(0, y + 3, t)
            c.setFillColor(HexColor("#f0efec"))
            c.rect(self.lw, y + 2, pw, self.rh - 4, fill=1, stroke=0)
            c.setFillColor(col)
            c.roundRect(self.lw, y + 2, max(pw * v / self.maxv, 1), self.rh - 4, 1.5, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont(FONT_B, 6.9)
            c.drawString(self.lw + pw + 3, y + 3, self.fmt.format(v))


class HeatMap(Flowable):
    """5x5 likelihood x impact grid with numbered risks."""

    def __init__(self, risks, width, height):
        super().__init__()
        self.risks, self.W, self.H = risks, width, height

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        L, B = 40, 28
        cw = (self.W - L - 8) / 5
        ch = (self.H - B - 10) / 5
        ramp = ["#f6f1e6", "#fbe3c4", "#f6c48d", "#ec835a", "#d03b3b"]
        for i in range(5):
            for j in range(5):
                score = (i + 1) * (j + 1)
                k = 0 if score <= 3 else 1 if score <= 6 else 2 if score <= 10 else 3 if score <= 15 else 4
                c.setFillColor(HexColor(ramp[k]))
                c.setStrokeColor(colors.white)
                c.setLineWidth(1.5)
                c.rect(L + i * cw, B + j * ch, cw, ch, fill=1, stroke=1)
        c.setFont(FONT, 6.5)
        c.setFillColor(INK2)
        for i, t in enumerate(["Rare", "Unlikely", "Possible", "Likely", "Almost\ncertain"]):
            c.drawCentredString(L + i * cw + cw / 2, B - 9, t.replace("\n", " "))
        for j, t in enumerate(["Minor", "Moderate", "Major", "Severe", "Critical"]):
            c.drawRightString(L - 3, B + j * ch + ch / 2 - 2, t)
        c.setFont(FONT_B, 7)
        c.drawCentredString(L + 2.5 * cw, 4, "LIKELIHOOD  →")
        c.saveState()
        c.translate(9, B + 2.5 * ch)
        c.rotate(90)
        c.drawCentredString(0, 0, "IMPACT ON MINE OPENING  →")
        c.restoreState()
        cells = {}
        for num, li, im in self.risks:
            cells.setdefault((li, im), []).append(num)
        for (li, im), nums in cells.items():
            cx = L + (li - 1) * cw + cw / 2
            cy = B + (im - 1) * ch + ch / 2
            n = len(nums)
            for k, num in enumerate(nums):
                ox = (k - (n - 1) / 2) * 15
                c.setFillColor(NAVY)
                c.circle(cx + ox, cy, 6.3, fill=1, stroke=0)
                c.setFillColor(colors.white)
                c.setFont(FONT_B, 6.8)
                c.drawCentredString(cx + ox, cy - 2.3, str(num))


class Dumbbell(Flowable):
    """Planned vs actual/forecast dates per milestone on a time axis (dates as month offsets)."""

    def __init__(self, rows, width, row_h, x0, x1, tick_labels, today=None, label_w=150):
        super().__init__()
        self.rows, self.W, self.rh = rows, width, row_h
        self.x0, self.x1, self.ticks, self.today, self.lw = x0, x1, tick_labels, today, label_w
        self.H = len(rows) * row_h + 34

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        pw = self.W - self.lw - 10
        L = self.lw

        def X(v):
            return L + pw * (v - self.x0) / (self.x1 - self.x0)
        ytop = self.H - 20
        for v, lab in self.ticks:
            c.setStrokeColor(GRID)
            c.setLineWidth(0.4)
            c.line(X(v), 12, X(v), ytop)
            c.setFillColor(INK2)
            c.setFont(FONT, 6.4)
            c.drawCentredString(X(v), ytop + 4, lab)
        if self.today is not None:
            c.setStrokeColor(NAVY)
            c.setDash(2, 2)
            c.line(X(self.today), 12, X(self.today), ytop)
            c.setDash()
            c.setFillColor(NAVY)
            c.setFont(FONT_B, 6.4)
            c.drawCentredString(X(self.today), 3, "Status 14-Oct-26")
        y = ytop
        for lab, plan, act, kind in self.rows:
            y -= self.rh
            c.setFillColor(INK)
            c.setFont(FONT, 7)
            c.drawString(0, y + self.rh / 2 - 2.5, lab)
            yc = y + self.rh / 2
            if act is not None:
                late = act > plan + 0.05
                c.setStrokeColor(CRIT if late else GOOD)
                c.setLineWidth(2.2)
                c.line(X(plan), yc, X(act), yc)
            c.setFillColor(HexColor("#2a78d6"))
            c.circle(X(plan), yc, 3.6, fill=1, stroke=0)
            if act is not None:
                if kind == "forecast":
                    c.setFillColor(colors.white)
                    c.setStrokeColor(HexColor("#eb6834"))
                    c.setLineWidth(1.6)
                    c.circle(X(act), yc, 3.4, fill=1, stroke=1)
                else:
                    c.setFillColor(HexColor("#eb6834"))
                    c.circle(X(act), yc, 3.6, fill=1, stroke=0)
        # legend
        lx = L
        ly = 3
        c.setFillColor(HexColor("#2a78d6"))
        c.circle(lx + 3, ly + 2.5, 3, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont(FONT, 6.6)
        c.drawString(lx + 9, ly, "CMDPA due date")
        c.setFillColor(HexColor("#eb6834"))
        c.circle(lx + 78, ly + 2.5, 3, fill=1, stroke=0)
        c.setFillColor(INK)
        c.drawString(lx + 84, ly, "Actual")
        c.setFillColor(colors.white)
        c.setStrokeColor(HexColor("#eb6834"))
        c.circle(lx + 118, ly + 2.5, 3, fill=1, stroke=1)
        c.setFillColor(INK)
        c.drawString(lx + 124, ly, "Forecast (P50)")


class Stakeholders(Flowable):
    """Hub-and-spoke stakeholder map (neutral colours)."""

    def __init__(self, groups, width, height, hub="GMDC\n(Successful Bidder)"):
        super().__init__()
        self.groups, self.W, self.H, self.hub = groups, width, height, hub

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        cx, cy = self.W / 2, self.H / 2
        n = len(self.groups)
        gw, gh = 160, None
        pos = [(0.03, 0.52), (0.69, 0.52), (0.03, 0.02), (0.69, 0.02)]
        for (title, items), (px, py) in zip(self.groups, pos):
            x = px * self.W
            y = py * self.H
            w = self.W * 0.28
            h = self.H * 0.46
            # connector
            c.setStrokeColor(HexColor("#b9c6d6"))
            c.setLineWidth(1.2)
            c.line(x + w / 2, y + h / 2, cx, cy)
            c.setFillColor(HexColor("#f4f6f9"))
            c.setStrokeColor(HexColor("#b9c6d6"))
            c.setLineWidth(0.8)
            c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
            c.setFillColor(NAVY)
            c.roundRect(x, y + h - 16, w, 16, 6, fill=1, stroke=0)
            c.rect(x, y + h - 16, w, 8, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont(FONT_B, 8)
            c.drawCentredString(x + w / 2, y + h - 11.5, title.replace("&amp;", "&"))
            yy = y + h - 26
            for it in items:
                p = Paragraph("• " + it, _ps(6.7, 7.6, INK))
                ww, hh = p.wrap(w - 10, 60)
                p.drawOn(c, x + 6, yy - hh + 7)
                yy -= hh + 1.2
        # hub
        c.setFillColor(NAVY)
        c.circle(cx, cy, 44, fill=1, stroke=0)
        c.setFillColor(HexColor("#2a78d6"))
        c.circle(cx, cy, 38, fill=1, stroke=0)
        c.setFillColor(colors.white)
        lines = self.hub.split("\n")
        c.setFont(FONT_B, 11)
        c.drawCentredString(cx, cy + 3, lines[0])
        c.setFont(FONT, 7)
        for k, ln in enumerate(lines[1:]):
            c.drawCentredString(cx, cy - 8 - k * 8, ln)
        c.setFillColor(INK2)
        c.setFont(FONT_I, 6.8)
        c.drawCentredString(cx, cy - 56, "PMC: single-point coordination")


class PhaseBand(Flowable):
    """Thin legend band of phase colours."""

    def __init__(self, phases, width, height=16, crit=True):
        super().__init__()
        self.phases, self.W, self.H, self.crit = phases, width, height, crit

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        x = 0
        c.setFont(FONT, 6.8)
        for code, label in self.phases:
            c.setFillColor(PHASE_COL[code])
            c.roundRect(x, 4, 9, 9, 1.5, fill=1, stroke=0)
            c.setFillColor(INK)
            c.drawString(x + 12, 5.5, label)
            x += 16 + stringWidth(label, FONT, 6.8)
        if self.crit:
            c.setStrokeColor(CRIT)
            c.setLineWidth(1.5)
            c.setFillColor(colors.white)
            c.roundRect(x, 4, 9, 9, 1.5, fill=1, stroke=1)
            c.setFillColor(INK)
            c.drawString(x + 12, 5.5, "Critical path")
            x += 16 + stringWidth("Critical path", FONT, 6.8)
            diamond(c, x + 4, 8.5, 4, NAVY)
            c.drawString(x + 11, 5.5, "Milestone / CMDPA gate")
