"""Build 'Coal Mining PMC.pdf' - bid-to-operationalisation process map with PERT/CPM.

Run:  python3 pmc_report/build.py
"""
from __future__ import annotations

import copy
import datetime as dt
import math
import os
import sys

import numpy as np
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import charts as ch  # noqa: E402
import content as ct  # noqa: E402
import model as md  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "Coal Mining PMC.pdf")

# ------------------------------------------------------------------ fonts ---
FD = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("Carlito", FD + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Bold", FD + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Italic", FD + "Carlito-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-BoldItalic", FD + "Carlito-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("Carlito", normal="Carlito", bold="Carlito-Bold", italic="Carlito-Italic",
                              boldItalic="Carlito-BoldItalic")

INK, INK2, NAVY, CRIT = ch.INK, ch.INK2, ch.NAVY, ch.CRIT
PW, PH = A4
LM = RM = 40
TM, BM = 54, 44
FW = PW - LM - RM
LW_, LH_ = landscape(A4)
LFW = LW_ - LM - RM

# ----------------------------------------------------------------- styles ---
S = {}
S["body"] = ParagraphStyle("body", fontName="Carlito", fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=5)
S["bodyj"] = ParagraphStyle("bodyj", parent=S["body"])
S["small"] = ParagraphStyle("small", parent=S["body"], fontSize=8, leading=10.2, textColor=INK2, spaceAfter=3)
S["cap"] = ParagraphStyle("cap", parent=S["body"], fontSize=7.8, leading=9.6, textColor=INK2, fontName="Carlito-Italic",
                          spaceBefore=2, spaceAfter=8)
S["h1"] = ParagraphStyle("h1", fontName="Carlito-Bold", fontSize=19, leading=23, textColor=NAVY, spaceAfter=4,
                         spaceBefore=0)
S["h2"] = ParagraphStyle("h2", fontName="Carlito-Bold", fontSize=12.6, leading=15.5, textColor=NAVY, spaceBefore=9,
                         spaceAfter=4)
S["h3"] = ParagraphStyle("h3", fontName="Carlito-Bold", fontSize=10, leading=12.5, textColor=INK, spaceBefore=6,
                         spaceAfter=3)
S["kicker"] = ParagraphStyle("kicker", fontName="Carlito-Bold", fontSize=8, leading=10, textColor=HexColor("#2a78d6"),
                             spaceAfter=1)
S["td"] = ParagraphStyle("td", fontName="Carlito", fontSize=7.5, leading=8.9, textColor=INK)
S["tdb"] = ParagraphStyle("tdb", parent=S["td"], fontName="Carlito-Bold")
S["th"] = ParagraphStyle("th", fontName="Carlito-Bold", fontSize=7.6, leading=9, textColor=colors.white)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=11, bulletIndent=2, spaceAfter=2.5)
S["toc1"] = ParagraphStyle("toc1", fontName="Carlito-Bold", fontSize=9.8, leading=11.6, textColor=INK, leftIndent=4,
                           spaceBefore=2.6)
S["toc2"] = ParagraphStyle("toc2", fontName="Carlito", fontSize=8.4, leading=9.5, textColor=INK2, leftIndent=20)


def P(t, s="body"):
    return Paragraph(t, S[s])


def bullets(items, s="bullet"):
    return [Paragraph(t, S[s], bulletText="•") for t in items]


H1_COUNT = [0]


def H1(title, kicker=None):
    H1_COUNT[0] += 1
    out = []
    if kicker:
        out.append(P(kicker.upper(), "kicker"))
    p = Paragraph(f"{H1_COUNT[0]}&nbsp;&nbsp;{title}", S["h1"])
    p._toc = (0, f"{H1_COUNT[0]}  {title}")
    out.append(p)
    out.append(Rule(FW, NAVY, 1.2))
    out.append(Spacer(1, 6))
    return out


def H2(title, toc=True):
    p = Paragraph(title, S["h2"])
    if toc:
        p._toc = (1, title)
    return p


class Rule(ch.Flowable):
    def __init__(self, w, col, th=0.6, space=2):
        super().__init__()
        self.w, self.col, self.th, self.sp = w, col, th, space

    def wrap(self, aw, ah):
        return min(self.w, aw), self.th + self.sp

    def draw(self):
        self.canv.setStrokeColor(self.col)
        self.canv.setLineWidth(self.th)
        self.canv.line(0, self.sp / 2, min(self.w, self._frame_w if hasattr(self, "_frame_w") else self.w), self.sp / 2)


def table(rows, widths, header=True, zebra=True, font=7.5, hdr_bg=NAVY, align_right_cols=(), bold_first=False,
          extra=None, repeat=1, crit_rows=(), pad=2.2):
    data = []
    for i, r in enumerate(rows):
        cells = []
        for j, v in enumerate(r):
            if isinstance(v, ch.Flowable) or isinstance(v, Paragraph):
                cells.append(v)
                continue
            st = S["th"] if (header and i == 0) else (S["tdb"] if (bold_first and j == 0) else S["td"])
            if font != 7.5 and not (header and i == 0):
                st = ParagraphStyle("t", parent=st, fontSize=font, leading=font * 1.18)
            if j in align_right_cols and not (header and i == 0):
                st = ParagraphStyle("tr", parent=st, alignment=2)
            if i in crit_rows:
                st = ParagraphStyle("tcr", parent=st, textColor=CRIT, fontName="Carlito-Bold")
            cells.append(Paragraph(str(v), st))
        data.append(cells)
    t = Table(data, colWidths=widths, repeatRows=repeat if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, HexColor("#e4e3df")),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), hdr_bg), ("VALIGN", (0, 0), (-1, 0), "MIDDLE")]
    if zebra:
        for i in range(1 if header else 0, len(data)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), HexColor("#f6f7f9")))
    if extra:
        style += extra
    t.setStyle(TableStyle(style))
    return t


def callout(text, col=HexColor("#2a78d6"), bg=None, title=None, width=None):
    bg = bg or ch.tint(col, 0.9)
    inner = []
    if title:
        inner.append(Paragraph(title, ParagraphStyle("ct", parent=S["h3"], textColor=ch.shade(col, 0.3), spaceBefore=0)))
    if isinstance(text, (list, tuple)):
        inner += list(text)
    else:
        inner.append(Paragraph(text, ParagraphStyle("cb", parent=S["body"], spaceAfter=0)))
    t = Table([["", inner]], colWidths=[4, (width or FW) - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), col),
        ("BACKGROUND", (1, 0), (1, 0), bg),
        ("LEFTPADDING", (1, 0), (1, 0), 8), ("RIGHTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (0, 0), 0), ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def tiles(items, width=None, cols=None):
    """items: (big, caption, colour)"""
    width = width or FW
    n = cols or len(items)
    w = width / n
    cells = []
    for big, cap, col in items:
        cells.append([Paragraph(big, ParagraphStyle("tb", fontName="Carlito-Bold", fontSize=19, leading=22,
                                                    textColor=col)),
                      Paragraph(cap, ParagraphStyle("tc", fontName="Carlito", fontSize=7.6, leading=9.3,
                                                    textColor=INK2))])
    rows = [cells[i:i + n] for i in range(0, len(cells), n)]
    t = Table(rows, colWidths=[w] * n)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8),
          ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]
    for r in range(len(rows)):
        for c_ in range(n):
            st.append(("BACKGROUND", (c_, r), (c_, r), HexColor("#f4f6f9")))
            st.append(("LINEBEFORE", (c_, r), (c_, r), 2.5, items[r * n + c_][2] if r * n + c_ < len(items) else NAVY))
            st.append(("LINEAFTER", (c_, r), (c_, r), 3, colors.white))
            st.append(("LINEBELOW", (c_, r), (c_, r), 3, colors.white))
    t.setStyle(TableStyle(st))
    return t


# ============================================================ ANALYSIS ===
def run_analysis():
    R = {}
    acts = copy.deepcopy(md.GENERIC)
    T, _ = md.cpm(acts)
    by = {a.id: a for a in acts}
    ef, ci = md.monte_carlo(acts, n=20000, seed=11)
    for a in acts:
        a.ci = ci[a.id]
    R["acts"], R["by"], R["T"] = acts, by, T
    R["cp"] = md.critical_path(acts, "K15")
    R["cp_var"] = sum(by[k].var for k in md.critical_path(acts, "K12"))
    ms5 = ef["K12"] - ef["A8"]
    fc = ef["K15"]
    R["ms5_samples"] = ms5
    R["fc_samples"] = fc
    R["ms5_te"] = by["K12"].ef - by["A8"].ef
    R["p51"] = float((ms5 <= 51).mean())
    R["ms5_p50"], R["ms5_p80"] = np.percentile(ms5, 50), np.percentile(ms5, 80)
    R["fc_p50"], R["fc_p80"] = np.percentile(fc, 50), np.percentile(fc, 80)
    # milestone timing after vesting (deterministic)
    R["ms_after_vest"] = {k: by[k].ef - by["A8"].ef for k in ["C3", "D8", "L13", "K12", "K15"]}

    # scenarios
    def scen(mod_preds=None, mod_dur=None, seed=11):
        a2 = copy.deepcopy(md.GENERIC)
        b2 = {x.id: x for x in a2}
        for k, v in (mod_dur or {}).items():
            b2[k].a, b2[k].m, b2[k].b = v
            b2[k].__post_init__()
        for k, v in (mod_preds or {}).items():
            b2[k].preds = v
        md.cpm(a2)
        e, c_ = md.monte_carlo(a2, n=12000, seed=seed)
        s = e["K12"] - e["A8"]
        cp = md.critical_path(a2, "K12")
        return dict(p50=np.percentile(s, 50), p80=np.percentile(s, 80), p51=(s <= 51).mean(),
                    te=b2["K12"].ef - b2["A8"].ef, cp=cp)

    k12_fast = [p for p in by["K12"].preds if p != "L13"] + ["L10", "L11"]
    R["scen"] = [
        ("S0", "Baseline - CMDPA sequence (mine opening after full MS-4 possession incl. R&R shifting)", scen()),
        ("S1", "Early SES: start SES/genealogy at s.4(1) instead of s.7(1)", scen(mod_preds={"L7": ["L2"]})),
        ("S2", "R&R plan & RPDAC prepared in parallel with SES (overlap ~50%)", scen(mod_dur={"L9": (2, 4, 9)})),
        ("S3", "Phased possession: box cut on a no-habitation patch; colony & shifting continue", scen(mod_preds={"K12": k12_fast})),
        ("S4", "S1 + S2 + S3 combined", scen(mod_preds={"L7": ["L2"], "K12": k12_fast}, mod_dur={"L9": (2, 4, 9)})),
        ("S5", "S4 + CA land pre-identified at bid stage + dedicated FC liaison", scen(
            mod_preds={"L7": ["L2"], "K12": k12_fast},
            mod_dur={"L9": (2, 4, 9), "F2": (1, 2, 4), "F5": (3, 5, 9), "F8": (2, 4, 8)})),
    ]
    # BW remaining work
    bw = copy.deepcopy(md.BW_REM)
    md.cpm(bw)
    byw = {a.id: a for a in bw}
    efw, ciw = md.monte_carlo(bw, n=20000, seed=5)
    for a in bw:
        a.ci = ciw[a.id]
    strict_preds = {"W14": ["W5", "W8", "W9", "W10", "W11", "W12", "W13", "W3"]}
    efs, cis = md.monte_carlo(bw, n=20000, seed=5, override_preds=strict_preds)
    R["bw"], R["bw_by"], R["bw_cp"] = bw, byw, md.critical_path(bw, "W16")
    sd = md.STATUS_DATE

    def mo_to(d):
        return (d - sd).days / 30.4375

    ms5_cmdpa = dt.date(2027, 3, 8)
    win51 = dt.date(2027, 9, 8)
    R["bw_targets"] = dict(ms5=ms5_cmdpa, win=win51, sdp=dt.date(2029, 9, 8))

    def summ(e):
        return dict(
            p50=md.add_months(sd, np.percentile(e["W14"], 50)), p80=md.add_months(sd, np.percentile(e["W14"], 80)),
            p_ms5=float((e["W14"] <= mo_to(ms5_cmdpa)).mean()), p_win=float((e["W14"] <= mo_to(win51)).mean()),
            fc50=md.add_months(sd, np.percentile(e["W16"], 50)), fc80=md.add_months(sd, np.percentile(e["W16"], 80)),
            samples=e["W14"])

    R["bw_phased"] = summ(efw)
    R["bw_strict"] = summ(efs)
    R["bw_ms4"] = dict(p50=md.add_months(sd, np.percentile(np.maximum(efs["W8"], efs["W9"]), 50)),
                       p80=md.add_months(sd, np.percentile(np.maximum(efs["W8"], efs["W9"]), 80)))
    # rail check for BW: needed before 6 MTPA (~24 months after first coal per production plan yrs 3->5)
    rail = sum((a + 4 * m + b) / 6 for _, _, a, m, b in md.RAIL[1:])  # IPA already received
    R["rail_te"] = rail
    R["rail_done"] = md.add_months(sd, rail)
    R["rail_need"] = md.add_months(R["bw_phased"]["fc50"], 24)
    return R


# ============================================================== PAGES ===
def on_page_end(c, doc):
    c.saveState()
    w, h = c._pagesize
    c.setFillColor(colors.white)
    c.setFont("Carlito", 8.5)
    c.drawRightString(w - RM, h - 17, getattr(doc, "_cur_section", ""))
    c.restoreState()


def on_cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    # phase band
    x = 0
    w = PW / 7
    for code, _ in md.PHASES:
        c.setFillColor(ch.PHASE_COL[code])
        c.rect(x, PH * 0.38, w, 7, fill=1, stroke=0)
        x += w
    # network motif
    import random
    rnd = random.Random(4)
    pts = [(rnd.uniform(40, PW - 40), rnd.uniform(PH * 0.06, PH * 0.33)) for _ in range(26)]
    pts.sort()
    c.setLineWidth(0.6)
    for i in range(len(pts) - 1):
        for j in range(i + 1, min(i + 3, len(pts))):
            c.setStrokeColor(HexColor("#2c5684"))
            c.line(*pts[i], *pts[j])
    for i, (px, py) in enumerate(pts):
        col = ch.PHASE_COL[md.PHASES[i % 7][0]] if i % 4 else CRIT
        c.setFillColor(col)
        c.circle(px, py, 3.2 if i % 4 else 4.2, fill=1, stroke=0)
    c.setStrokeColor(CRIT)
    c.setLineWidth(1.6)
    crit_pts = pts[::4]
    for i in range(len(crit_pts) - 1):
        c.line(*crit_pts[i], *crit_pts[i + 1])
    c.setFillColor(colors.white)
    c.setFont("Carlito-Bold", 11)
    c.drawString(LM, PH - 70, "PROJECT MANAGEMENT CONSULTANCY  |  GMDC COAL BLOCKS, ODISHA")
    c.setFont("Carlito-Bold", 46)
    c.drawString(LM, PH - 165, "Coal Mining PMC")
    c.setFont("Carlito", 19)
    c.setFillColor(HexColor("#cde2fb"))
    c.drawString(LM, PH - 198, "From block auction to mine operationalisation in Odisha")
    c.setFont("Carlito", 13)
    c.setFillColor(colors.white)
    lines = [
        "End-to-end process map (CBA Act land route)  •  ~200 granular activities",
        "PERT three-point estimates  •  CPM forward/backward pass  •  Monte Carlo risk",
        "Critical-activity register  •  Baitarani West status & forecast",
    ]
    for i, ln in enumerate(lines):
        c.drawString(LM, PH - 240 - i * 19, ln)
    # info box
    c.setFillColor(HexColor("#0d2a49"))
    c.roundRect(LM, PH * 0.38 + 40, PW - 2 * LM, 120, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#9ec5f4"))
    c.setFont("Carlito-Bold", 9)
    c.drawString(LM + 16, PH * 0.38 + 136, "CASE STUDY")
    c.setFillColor(colors.white)
    c.setFont("Carlito-Bold", 16)
    c.drawString(LM + 16, PH * 0.38 + 114, "Baitarani West Coal Block - Talcher Coalfield, Angul, Odisha")
    c.setFont("Carlito", 10.5)
    c.setFillColor(HexColor("#dbe9fb"))
    c.drawString(LM + 16, PH * 0.38 + 94, "15 MTPA opencast  •  1,196 ha  •  468 Mt extractable  •  G12  •  37-year life")
    c.drawString(LM + 16, PH * 0.38 + 78, "Successful bidder: Gujarat Mineral Development Corporation Ltd (GMDC)")
    c.drawString(LM + 16, PH * 0.38 + 62, "CMDPA 29-Mar-2023  •  Vesting order 08-Jun-2023  •  Final Offer 33.50% revenue share")
    c.setFont("Carlito", 9)
    c.setFillColor(HexColor("#9ec5f4"))
    c.drawString(LM, 40, "Status date: 14 October 2026   •   Prepared with public sources (MoC, PIB, PARIVESH, CCO, Railways) and project records")
    c.restoreState()


def on_page(c, doc):
    c.saveState()
    w, h = c._pagesize
    c.setFillColor(NAVY)
    c.rect(0, h - 26, w, 26, fill=1, stroke=0)
    x = 0
    seg = w / 7
    for code, _ in md.PHASES:
        c.setFillColor(ch.PHASE_COL[code])
        c.rect(x, h - 29, seg, 3, fill=1, stroke=0)
        x += seg
    c.setFillColor(colors.white)
    c.setFont("Carlito-Bold", 8.5)
    c.drawString(LM, h - 17, "Coal Mining PMC")
    c.setFont("Carlito", 8.5)
    c.drawString(LM + 74, h - 17, "Auction-to-operationalisation playbook  |  Baitarani West, Odisha")
    c.setFillColor(INK2)
    c.setFont("Carlito", 7.5)
    c.drawString(LM, 22, "Status 14-Oct-2026. Durations are planning estimates; verify statutory provisions against current notifications.")
    c.setFont("Carlito-Bold", 8.5)
    c.setFillColor(NAVY)
    c.drawRightString(w - RM, 22, f"{doc.page}")
    c.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM, **kw)
        fr = Frame(LM, BM, FW, PH - TM - BM, id="p", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        frl = Frame(LM, BM, LFW, LH_ - TM - BM, id="l", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        frc = Frame(LM, BM, FW, PH - TM - BM, id="c")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frc], onPage=on_cover, pagesize=A4),
            PageTemplate(id="portrait", frames=[fr], onPage=on_page, onPageEnd=on_page_end, pagesize=A4),
            PageTemplate(id="landscape", frames=[frl], onPage=on_page, onPageEnd=on_page_end, pagesize=landscape(A4)),
        ])
        self._cur_section = ""

    def beforeDocument(self):
        self._cur_section = ""

    def afterFlowable(self, f):
        if hasattr(f, "_toc"):
            lvl, text = f._toc
            if lvl == 0:
                self._cur_section = text
            key = f"toc-{id(f)}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=lvl, closed=lvl > 0)
            self.notify("TOCEntry", (lvl, text, self.page, key))


# ============================================================== STORY ===
def build():
    R = run_analysis()
    acts, by = R["acts"], R["by"]
    bw, byw = R["bw"], R["bw_by"]
    story = []
    # ---------------- cover
    story += [Spacer(1, 10), NextPageTemplate("portrait"), PageBreak()]

    # ---------------- contents + about
    story.append(P("CONTENTS", "kicker"))
    story.append(Paragraph("Contents", S["h1"]))
    story.append(Rule(FW, NAVY, 1.2))
    story.append(Spacer(1, 4))
    toc = TableOfContents()
    toc.levelStyles = [S["toc1"], S["toc2"]]
    toc.dotsMinLevel = 0
    story.append(toc)
    story.append(Spacer(1, 8))
    story.append(callout([
        P("<b>What this report is.</b> A practitioner's playbook for taking a commercial coal block in Odisha from "
          "the auction notice to the first tonne of coal, when land is acquired by a Government company under the "
          "<b>Coal Bearing Areas (Acquisition &amp; Development) Act, 1957</b>. Every statutory and practical step is "
          "listed (about 200 granular activities), organised into nine process flows, then rolled up into a "
          "62-activity network analysed with <b>PERT</b> (three-point time estimates), <b>CPM</b> (critical path and "
          "float) and a 20,000-run <b>Monte Carlo</b> simulation.", "small"),
        P("<b>How to read it.</b> Colours identify the seven work phases throughout (legend below). A red outline "
          "or bar always means <b>critical</b> (zero float); a navy diamond marks a CMDPA milestone (MS-2 to MS-5) or "
          "another gate. Durations are in months unless stated. Section 10 applies the method to Baitarani West with "
          "status as on 14-Oct-2026.", "small"),
        P("<b>Sources.</b> Project records in the repository (CMDPA, final EIA/EMP, MIS of 30-Sep-2026, 2023 "
          "tracker, bidding deck, Acts and Rules) and web research on Ministry of Coal, PIB, PARIVESH, Coal "
          "Controller, Railway Board, CGWA and Odisha Government sites (Annex B). The 2023 tracker was used for its "
          "activity lists only; its dates and several procedures are superseded (Section 12).", "small"),
    ], col=NAVY, bg=HexColor("#f4f6f9")))
    story.append(Spacer(1, 6))
    story.append(ch.PhaseBand(md.PHASES[:4], FW, crit=False))
    story.append(ch.PhaseBand(md.PHASES[4:], FW, crit=True))
    story.append(Spacer(1, 10))
    story.append(H2("The nine processes on one page", toc=False))
    dash = [["Process", "Legal basis", "Sanctioning authority", "Typical span*", "CMDPA link", "Baitarani West (Oct-26)"],
            ["1  Auction &amp; vesting", "CM(SP) Act 2015; MMDR Act", "Nominated Authority (MoC)", "6-9 months", "Zero date", "Done - CMDPA 29-Mar-23; vesting 08-Jun-23"],
            ["2  Mobilisation &amp; surveys", "MP Guidelines 2025 (DGPS)", "CMPDI / ORSAC; Tehsildar", "3-6 months", "Feeds all", "Done - DGPS certified 12-Jan-24"],
            ["3  Mining plan &amp; closure plan", "MCR 2016/2020; MP Guidelines 2025", "CCO / MoC", "4-8 months", "MS-2", "Done - OMC plan transferred 13-Oct-23"],
            ["4  Environment clearance", "EP Act 1986; EIA Notification 2006", "MoEFCC (EAC Coal)", "14-24 months", "MS-3", "Done - EC 03-Dec-25 (~12 months late)"],
            ["5  Forest clearance (+FRA, CA, WLCP)", "VSSR 2023; FRA 2006; WPA 1972", "MoEFCC; Odisha Forest Dept", "24-40 months", "Feeds MS-5", "Stage-I 02-Dec-25; Stage-II at MoEFCC; FRA pending"],
            ["6  Land acquisition (CBA)", "CBA Act 1957", "MoC; Collector as competent authority", "12-26 months", "MS-4", "s.4/7/9/11 notified 13-Oct-23; payments ongoing"],
            ["7  Resettlement &amp; rehabilitation", "RFCTLARR Sch. I-III (S.O. 2368(E)); ORRP 2006", "Collector / RPDAC", "26-45 months", "MS-4", "RPDAC held 07-Oct-26; colony &amp; shifting pending"],
            ["8  Consents &amp; infrastructure", "Water/Air Acts; CGWA; GCT Circular", "OSPCB, WRD, CGWA, ECoR, PESO", "6-30 months", "Feeds MS-5", "CTE 29-Apr-26; CTO &amp; nala NOC pending; MDO signed 17-Sep-26"],
            ["9  Mine opening &amp; first coal", "Mines Act s.16; CMR 2017; CCR 2004 (amended)", "GMDC Board; DGMS; CCO (intimation)", "1-6 months", "MS-5", "CMDPA date 08-Mar-27; P50 forecast in Section 10"],
            ]
    story.append(table(dash, [104, 104, 92, 50, 44, FW - 394], font=7.2, bold_first=True))
    story.append(P("* Elapsed span of the process for a fresh block, from the CPM model (Section 7); processes overlap "
                   "heavily, so spans are not additive.", "cap"))
    story.append(PageBreak())

    # ---------------- 1 Executive summary
    story += H1("Executive summary", "At a glance")
    p51 = R["p51"]
    story.append(tiles([
        (f"{R['T']:.0f} months", "Expected duration, tender launch to first coal, for a fresh Odisha block (CPM on PERT means)", ch.PHASE_COL["AUC"]),
        (f"{R['ms5_te']:.1f} months", "Expected vesting-to-mine-opening (MS-5) time vs 51 months allowed by the CMDPA", ch.PHASE_COL["LAR"]),
        (f"{p51 * 100:.0f}%", "Probability of opening within the 51-month window (Monte Carlo, 20,000 runs)", CRIT),
        (f"{by['L7'].ci * 100:.0f}%", "Criticality index of the land &amp; R&amp;R chain - it drives the finish in almost every run", ch.PHASE_COL["OPN"]),
    ]))
    story.append(Spacer(1, 8))
    story.append(H2("Key messages", toc=False))
    cp_names = " → ".join(R["cp"])
    msgs = [
        "<b>The path from bid to coal has nine interlocking processes and ~200 steps</b>: auction &amp; vesting, "
        "mobilisation &amp; surveys, mining plan, environment clearance, forest clearance (with FRA, CA land, tree "
        "enumeration and wildlife plan), CBA land acquisition, R&amp;R, other consents, and mine opening. Only four "
        "milestones are policed by the CMDPA (MS-2 mining plan, MS-3 EC, MS-4 land &amp; R&amp;R, MS-5 mine opening), "
        "but every other step feeds them.",
        f"<b>The critical path runs through land, not clearances</b>: {cp_names}. Under the CBA route the "
        "slowest items are SES/genealogy/YADAST, RPDAC approval of the R&amp;R plan, and building the R&amp;R colony "
        "and shifting families before possession (MS-4).",
        f"<b>Forest clearance is the near-critical path</b> (total float ≈ {by['F5'].tf:.0f} months): CA land "
        "suitability, the multi-tier State processing, Stage-I compliance and the FRA certificate. It becomes "
        "critical as soon as land is fast-tracked (scenarios S3-S5).",
        "<b>EC, mining plan, MDO tendering and most consents carry large float</b> - they should still be started "
        "early, because their real risk is rework (e.g., EAC returning a proposal) rather than duration.",
        f"<b>Fast-tracking works</b>: starting the SES at s.4(1), overlapping R&amp;R planning with the SES and "
        f"phasing possession (box cut on a no-habitation patch) lift the probability of meeting the 51-month window "
        f"from {R['scen'][0][2]['p51'] * 100:.0f}% to {R['scen'][4][2]['p51'] * 100:.0f}% (S4).",
        f"<b>Baitarani West (status 14-Oct-2026)</b>: mining plan, EC (03-Dec-25), FC Stage-I (02-Dec-25), CTE "
        f"(29-Apr-26) and the MDO contract (17-Sep-26) are done; FC Stage-II, FRA certificate, nala NOC, CTO, "
        f"compensation for the 5-year area and R&amp;R shifting remain. Our P50 forecast for mine opening (MS-5) is "
        f"<b>{md.fmt_date(R['bw_phased']['p50'])}</b> with phased possession (P = {R['bw_phased']['p_ms5'] * 100:.0f}% of "
        f"meeting the CMDPA date 08-Mar-27) but <b>{md.fmt_date(R['bw_strict']['p50'])}</b> if R&amp;R shifting must "
        f"precede opening (P = {R['bw_strict']['p_win'] * 100:.0f}% of opening inside the 51-month window, 08-Sep-27).",
        "<b>Money is attached to the dates</b>: up to ₹386.8 Cr of performance security (MS-3 10% + MS-4 25%) can be "
        "appropriated for BW's delays but becomes refundable if MS-5 is reached within 51 months of vesting; every "
        "tonne produced before 08-Sep-2029 attracts only half the 33.5% revenue share.",
    ]
    story += bullets(msgs)
    story.append(Spacer(1, 4))
    story.append(callout(
        "<b>Top five actions for Baitarani West (next 90 days):</b> (1) close FC Stage-II at MoEFCC and the FRA "
        "certificate at DLC Angul in parallel; (2) keep CTO 'ready except FC-II' so it issues within days; (3) finish "
        "the 199-ha case files and disbursement camps and take possession of the box-cut patch; (4) notify the R&amp;R "
        "scheme after the 07-Oct-26 RPDAC and lock colony and gochar land; (5) file an extension representation to "
        "the Nominated Authority for delays not attributable to GMDC, and plan MS-5 well before 08-Sep-2027.",
        col=CRIT, title="Bottom line"))
    story.append(PageBreak())

    # ---------------- 2 Baitarani West at a glance
    story += H1("Baitarani West at a glance", "Case study")
    facts = [
        ["Parameter", "Value", "Parameter", "Value"],
        ["Location", "Chhendipada tehsil, Angul district, Odisha; north-central Talcher coalfield",
         "Villages", "Chhendipada Jangal, Handigora, Machhakuta, Porapara, Tentuloi Korasahi and others"],
        ["Mine type / capacity", "Opencast; 15 MTPA (surface miner 93%, drill-blast 7%)", "Lease area", "1,196 ha (tenancy 908.65; Govt 222.98; forest 64.37)"],
        ["Reserves", "Gross GR 662.9 Mt; net GR 602.1 Mt; extractable 468.3 Mt", "Grade / strip ratio", "G12 (~3,946 kcal/kg); 1.53 m³/t"],
        ["Depth / seams", "160-245 m; seam thickness 0.08-33.94 m", "Life", "37 years; peak 15 MTPA from year 7"],
        ["Dumps", "External 215.8 ha (140 Mm³, 90 m); internal 623.7 ha (573 Mm³)", "Evacuation", "12 MTPA conveyor + silo + siding to ECoR (Jarpara); 3 MTPA road"],
        ["Project cost", "₹3,855 Cr (R&amp;R ₹727.94 Cr; EMP capex ₹100.7 Cr)", "Cost of production", "₹337.11/t (EIA)"],
        ["Manpower", "1,752 direct (269 departmental, 1,483 contractual); ~5,000 indirect", "Affected families", "3,402 original families in SES (Jan-25)"],
        ["Auction", "16th tranche CM(SP) Act; Final Offer 33.50%", "CMDPA / vesting", "29-Mar-2023 / 08-Jun-2023 (NA-104/4/2023-NA)"],
        ["Upfront amount", "₹500 Cr in 4 × ₹125 Cr instalments", "Performance security", "₹1,105.19 Cr; fixed amount ₹49.40 Cr"],
        ["History", "Cancelled 2014 (SC); OMC allotment 2016; OMC mine plan approved 10-Nov-21", "Land route", "CBA Act: s.4(1), 7(1), 9(1), 11(1) in GMDC's favour 13-Oct-23"],
    ]
    story.append(table(facts, [72, FW / 2 - 72, 72, FW / 2 - 72], bold_first=False,
                       extra=[("FONTNAME", (0, 1), (0, -1), "Carlito-Bold"), ("FONTNAME", (2, 1), (2, -1), "Carlito-Bold")]))
    story.append(P("Sources: CMDPA (29-Mar-2023); Final EIA/EMP (GRC India) Tables 2.3, 2.12, 10.2; MIS 30-Sep-2026.", "cap"))
    land = [("Tenancy (private)", 908.65, ch.PHASE_COL["AUC"]), ("Govt non-forest", 222.98, ch.PHASE_COL["MOB"]),
            ("Forest", 64.37, ch.PHASE_COL["MPL"])]
    prod_years = list(range(1, 38))
    prod = [0, 0, 0.9, 3, 6, 10.5] + [15] * 28 + [12, 9, 6.87]
    ob = [0, 0, 3.55, 4.54, 11.22, 15.99, 15.84, 16.07, 18.2, 18.2, 20.88] + [24.75] * 14 + [22.4] * 9 + [22.4, 11.54, 8.87]
    ob = ob[:37]
    left = ch.Donut(land, FW * 0.42, 128, center_text=("1,196 ha", "mining lease"))
    right = ch.Columns(prod_years, prod, FW * 0.56, 150, ch.PHASE_COL["AUC"], ylab="Mt coal / Mm³ OB",
                       xlab="Year of operation", ys2=ob, col2=ch.PHASE_COL["MOB"], lab1="Coal (Mt)",
                       lab2="OB (Mm³)", every=3, ymax=27)
    t = Table([[left, right]], colWidths=[FW * 0.43, FW * 0.57])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(t)
    story.append(P("Left: land composition of the lease (EIA Table 2.3). Right: approved production and overburden "
                   "schedule - first coal in operating year 3, 6 MTPA in year 5 (rail needed), 15 MTPA from year 7.", "cap"))
    story.append(H2("Money tied to milestones", toc=False))
    pay = [
        ["Payment / security", "Trigger (CMDPA)", "Amount", "BW status"],
        ["Upfront 1st (25%) to NA", "≤40 business days of CMDPA", "₹125 Cr", "Paid 02-May-23 (due 08-May-23)"],
        ["Upfront 2nd (25%) to State", "≤15 business days of s.11(1) order", "₹125 Cr", "Paid 04-Jan-24 (due 28-Oct-23; State-side delay)"],
        ["Upfront 3rd (25%) to State", "≤15 business days of mine-opening permission", "₹125 Cr", "Due ~Mar-27 (CMDPA basis)"],
        ["Upfront 4th (25%) to State", "≤15 business days of first coal", "₹125 Cr", "To be scheduled"],
        ["Performance security", "65% × (1-yr royalty + 1-yr revenue share) at PRC", "₹1,105.19 Cr", "With NA; moves to State at mine opening"],
        ["PS appropriation risk", "MS-2 10% / MS-3 10% / MS-4 25% / MS-5 25%", "₹110.5 / 110.5 / 276.3 / 276.3 Cr", "MS-3 late (EC 03-Dec-25); MS-4 overdue since 08-Sep-26"],
        ["Monthly revenue share", "33.5% × royalty quantity × max(notional, actual price)", "-", "Upfront adjusted ≤50% of monthly payment"],
    ]
    story.append(table(pay, [118, 160, 92, FW - 370]))
    story.append(P("Note 6 of CMDPA Schedule D: if MS-5 is achieved within 51 months of vesting (BW: 08-Sep-2027), "
                   "performance security appropriated for earlier milestone delays may be refunded.", "cap"))
    story.append(PageBreak())

    # ---------------- 3 Regulatory framework
    story += H1("Regulatory and institutional framework", "Who decides what")
    rows = [["Law / instrument", "What it governs for the project", "Authority", "Stage"]] + [list(r) for r in ct.LEGAL]
    story.append(table(rows, [150, FW - 150 - 105 - 70, 105, 70], font=7.3))
    story.append(Spacer(1, 6))
    story.append(H2("Stakeholder map", toc=False))
    groups = [
        ("Central Government", ["MoC - Nominated Authority (CMDPA, vesting, CBA notifications)", "Coal Controller (mining plan, escrow, grade)",
                                "MoEFCC - EAC, FAC, IRO Bhubaneswar", "DGMS (safety), PESO (explosives)", "CGWA (groundwater)",
                                "Railway Board / ECoR (GCT siding)"]),
        ("Government of Odisha", ["Revenue &amp; DM Dept; Collector &amp; RDC (CBA competent authority, RPDAC)", "Forest Dept: DFO Angul, RCCF, PCCF, CWLW",
                                  "OSPCB (PH, CTE, CTO)", "WRD (water, nala diversion)", "Steel &amp; Mines / DoM (royalty, i3MS)",
                                  "Energy: OPTCL / TPCODL", "ORSAC (DGPS, maps)"]),
        ("Community", ["Gram Sabhas (FRA, CA villages, PH)", "Project affected &amp; displaced families", "Panchayats, MLAs, MPs (RPDAC members)",
                       "Forest Rights Committees", "Local employment &amp; CSR beneficiaries"]),
        ("Contractors &amp; advisors", ["PMC (programme control, MIS)", "MPPA / QP (mining plan)", "EIA &amp; FC consultants (NABET)",
                                     "LA &amp; R&amp;R agency (SES, case files)", "MDO / turnkey contractor", "IPRCL / EPC (rail, road)"]),
    ]
    story.append(ch.Stakeholders(groups, FW, 262))
    story.append(P("GMDC sits at the centre; the PMC's job is to keep ~25 counterparties moving on one integrated "
                   "schedule.", "cap"))
    story.append(CondPageBreak(330))
    story.append(H2("Responsibility matrix (RACI)", toc=False))
    raci_rows = [["Process"] + ct.RACI_COLS]
    for proc, vals in ct.RACI:
        raci_rows.append([proc] + vals)
    rx = []
    fills = {"S": (NAVY, colors.white), "A": (HexColor("#2a78d6"), colors.white), "R": (HexColor("#1baf7a"), colors.white),
             "C": (HexColor("#dbe9fb"), INK), "I": (HexColor("#f0efec"), INK2)}
    for i, (_, vals) in enumerate(ct.RACI, 1):
        for j, v in enumerate(vals, 1):
            if v:
                bg, fg = fills[v.split()[-1] if v.split()[-1] == "S" else v.split()[0]]
                rx += [("BACKGROUND", (j, i), (j, i), bg)]
    cw = (FW - 112) / len(ct.RACI_COLS)
    rt = table(raci_rows, [112] + [cw] * len(ct.RACI_COLS), zebra=False, font=7.6, extra=rx +
               [("ALIGN", (1, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
    for i, (_, vals) in enumerate(ct.RACI, 1):
        for j, v in enumerate(vals, 1):
            key = v.split()[-1] if v.split() and v.split()[-1] == "S" else (v.split()[0] if v else "")
            fg = fills[key][1] if key else INK
            rt._cellvalues[i][j] = Paragraph(f"<b>{v}</b>", ParagraphStyle("rc", parent=S["td"], alignment=TA_CENTER,
                                                                            textColor=fg, fontSize=8))
    story.append(rt)
    story.append(P("A = accountable, R = responsible (does the work), S = sanctions / approves, C = consulted, "
                   "I = informed. Government agencies 'sanction'; GMDC stays accountable for every row - including "
                   "the Board's own sanction of mine opening under the amended Colliery Control Rules.", "cap"))
    story.append(NextPageTemplate("landscape"))
    story.append(PageBreak())

    # ---------------- 4 Master flow (landscape)
    story += H1("End-to-end process map", "Flow of all processes")
    lanes = [("AUC", "Auction &amp; vesting", "AUC"), ("MOB", "Mobilisation &amp; surveys", "MOB"),
             ("MPL", "Mining plan", "MPL"), ("ENV", "Environment clearance", "ENV"), ("FOR", "Forest clearance", "FOR"),
             ("LA1", "Land acquisition (CBA Act)", "LAR"), ("LA2", "R&amp;R (RFCTLARR Sch. + ORRP 2006)", "LAR"),
             ("CON", "Consents &amp; infrastructure", "OPN"), ("OPN", "Mine opening &amp; coal", "OPN")]
    boxes = {
        "au1": ("AUC", 0, 9, "Tender study, site visit, due diligence &amp; bid", "n"),
        "au2": ("AUC", 10, 18.5, "e-auction, CMDPA, upfront, PBG", "crit"),
        "au3": ("AUC", 19.5, 27, "Vesting order (zero date)", "ms"),
        "mo1": ("MOB", 19.5, 28, "SWCS, PMC, consultants onboard", "crit"),
        "mo2": ("MOB", 29, 37.5, "DGPS + certified land schedule", "crit"),
        "mp1": ("MPL", 38.5, 47, "Mining plan + closure plan on SWCS", "n"),
        "mp2": ("MPL", 48, 55, "Approval (MS-2)", "ms"),
        "en1": ("ENV", 48, 56.5, "ToR + one-season baseline", "n"),
        "en2": ("ENV", 57.5, 66, "Studies, draft EIA, public hearing", "n"),
        "en3": ("ENV", 67, 74, "EC (MS-3)", "ms"),
        "fo1": ("FOR", 38.5, 47, "Tree enumeration, CA land, FRA", "n"),
        "fo2": ("FOR", 48, 57, "Form-A > State > FAC > Stage-I", "n"),
        "fo3": ("FOR", 58, 67, "Levies + Stage-I compliance", "n"),
        "fo4": ("FOR", 68, 76, "Stage-II, State order, felling", "n"),
        "la1": ("LA1", 38.5, 46.5, "s.4(1) notification", "crit"),
        "la2": ("LA1", 47.5, 55.5, "s.7(1) intent to acquire", "crit"),
        "la3": ("LA1", 56.5, 64.5, "s.8 objections; s.9(1) declaration", "n"),
        "la4": ("LA1", 65.5, 73, "s.11(1) vesting; 2nd upfront", "n"),
        "lr1": ("LA2", 56.5, 65, "SES, genealogy, YADAST", "crit"),
        "lr2": ("LA2", 66, 74, "R&amp;R plan &amp; RPDAC", "crit"),
        "lr3": ("LA2", 75, 83.5, "Compensation, colony &amp; shifting", "crit"),
        "lr4": ("LA2", 84.5, 91, "Possession (MS-4)", "ms"),
        "co1": ("CON", 48, 56.5, "MDO tender &amp; award", "n"),
        "co2": ("CON", 57.5, 66, "CGWA, water, nala, power, licences", "n"),
        "co3": ("CON", 77, 85, "CTE > CTO", "n"),
        "op1": ("OPN", 92, 100, "MS-5 Board approval > box cut > first coal", "ms"),
    }
    links = [("au1", "au2", True), ("au2", "au3", False), ("au2", "mo1", True), ("mo1", "mo2", True),
             ("au3", "mo2", False), ("mo2", "mp1", False), ("mp1", "mp2", False), ("mp1", "en1", False),
             ("mp1", "fo2", False), ("mo2", "fo1", False), ("fo1", "fo2", False), ("fo2", "fo3", False),
             ("fo3", "fo4", False), ("mo2", "la1", True), ("la1", "la2", True), ("la2", "la3", False),
             ("la3", "la4", False), ("la2", "lr1", True), ("lr1", "lr2", True), ("lr2", "lr3", True),
             ("la4", "lr3", False), ("lr3", "lr4", True), ("en1", "en2", False), ("en2", "en3", False),
             ("en3", "co3", False), ("fo4", "co3", False), ("mp2", "co1", False), ("co1", "co2", False),
             ("co2", "op1", False), ("co3", "op1", False), ("fo4", "op1", False), ("lr4", "op1", True)]
    story.append(ch.LaneMap(LFW, 410, [(l[0], l[1]) for l in lanes], boxes, links, title_w=92)
                 if False else LaneMap9(LFW, 428, lanes, boxes, links))
    story.append(P("Logic of the whole programme. Red = critical chain from the CPM; navy boxes = milestones. "
                   "Horizontal position is indicative of sequence, not to scale. Section 5 expands every box into "
                   "its detailed flow and step list.", "cap"))
    story.append(NextPageTemplate("portrait"))
    story.append(PageBreak())

    # CMDPA gates page
    story.append(H2("CMDPA efficiency parameters - the four policed milestones", toc=False))
    gates = [
        ["MS", "Main activity monitored", "Time allowed (fully explored)", "PS appropriated if late", "BW due date", "BW actual / forecast"],
        ["MS-1", "Geological Report (partially explored only)", "Not applicable", "-", "-", "-"],
        ["MS-2", "Approval of Mining Plan", "6 months from allocation", "10%", "08-Dec-23", "Met - OMC plan deemed transferred"],
        ["MS-3", "Environment Clearance", "18 months after MS-2", "10%", "08-Dec-24", "03-Dec-25 (~12 months late)"],
        ["MS-4", "Land acquisition, possession &amp; R&amp;R for rated capacity", "21 months after MS-3", "25%", "08-Sep-26",
         f"Overdue; P50 {md.fmt_date(R['bw_ms4']['p50'])} incl. shifting"],
        ["MS-5", "Mine opening permission", "6 months after MS-4", "25%", "08-Mar-27",
         f"P50 {md.fmt_date(R['bw_phased']['p50'])} (phased)"],
        ["Total", "All milestones", "51 months (66 if partially explored)", "Refund of earlier PS if MS-5 in 51 months", "08-Sep-27", "-"],
    ]
    story.append(table(gates, [34, 132, 98, 92, 56, FW - 412]))
    story.append(P("Non-monitored Schedule D activities (no penalty, but tracked for early development): mining lease "
                   "application, FC and EC applications, FC Stage-I/II, wildlife clearance, PESA approval, nala/river "
                   "diversion, diversion of power line/rail/road, permission to draw water and power, CTE/CTO, "
                   "grant of ML or s.11 CBA order, DGMS intimation, explosives and petroleum licences, Factories Act "
                   "permission, RF communication licence, labour permissions and the escrow account. Schedule D note 3 "
                   "expressly allows clearances to be obtained concurrently.", "small"))
    story.append(callout(
        "<b>Reading the clock.</b> The MIS (and this report) treats each milestone's due date as fixed from the vesting "
        "date (MS-2 at vesting since the plan was transferred; MS-3 = vesting + 18 months, and so on). Schedule D says "
        "'from completion of previous MS', which a late MS-3 could arguably reset; this conservative reading should be "
        "confirmed with the Nominated Authority before any extension request.", col=ch.PHASE_COL["ENV"]))
    story.append(Spacer(1, 4))
    story.append(H2("Statutory and contractual clocks - quick reference"))
    ck = [["Area", "Step", "Time limit", "Source"]] + [list(r) for r in ct.CLOCKS]
    story.append(table(ck, [70, 128, FW - 70 - 128 - 100, 100], font=7.2, pad=1.8))
    story.append(P("Desk-wise limits are the PMC's best escalation tool: a file idle beyond its published limit can "
                   "be raised with the next level by citing the rule.", "cap"))
    story.append(PageBreak())

    # ---------------- 5 Detailed processes
    story += H1("Detailed process flows and step lists", "Every activity, however small")
    story.append(P("Each sub-section gives the purpose and legal basis, a flowchart of the main steps (actor and "
                   "typical time on each card; red outline = on the critical path of the generic network) and a "
                   "granular checklist that can be lifted straight into the PMC tracker."))
    for i, pr in enumerate(ct.PROCESSES):
        col = ch.PHASE_COL[pr["code"]]
        story.append(KeepTogether([H2(f"5.{i + 1}  {pr['title']}"), P(pr["intro"]),
                                   ch.FlowChart(pr["flow"], col, FW, cols=4)]))
        story.append(Spacer(1, 5))
        rows = [["#", "Activity / step", "Responsible", "Legal basis / reference", "Typical time"]]
        for k, (a_, r_, l_, t_) in enumerate(pr["table"], 1):
            rows.append([str(k), a_, r_, l_, t_])
        story.append(table(rows, [16, FW - 16 - 92 - 98 - 68, 92, 98, 68], font=7.3,
                           hdr_bg=ch.shade(col, 0.35)))
        story.append(Spacer(1, 3))
        if pr["code"] == "LAR" and "CBA" in pr["title"]:
            story.append(Spacer(1, 3))
            story.append(P("<b>Entitlements that flow to affected families</b> (RFCTLARR 2013 Schedules applied to CBA "
                           "acquisitions by S.O. 2368(E), 28-Aug-2015):", "small"))
            story.append(table([["Head", "Entitlement"]] + [list(r) for r in ct.RR_ENT], [110, FW - 110], font=7.2,
                               hdr_bg=ch.shade(col, 0.35), pad=1.8))
            story.append(Spacer(1, 3))
        story += bullets([f"<i>{t}</i>" for t in pr["tips"]], "bullet")
        story.append(Spacer(1, 4))

    # ---------------- 6 PERT/CPM method
    story.append(PageBreak())
    story += H1("PERT and CPM - method", "How the schedule was computed")
    story.append(P("The ~200 steps were rolled up into <b>62 activities</b> that each have one accountable owner and "
                   "clear predecessors (activity-on-node, finish-to-start). Time zero (T0) is the launch of the "
                   "auction tranche. For every activity three estimates were set from statutory time limits, the "
                   "durations actually observed on Baitarani West and the MoC's July-2025 review of Odisha blocks:"))
    meth = [
        ["Quantity", "Formula", "Meaning"],
        ["Expected time t<sub>e</sub>", "(a + 4m + b) / 6", "Beta-PERT mean of optimistic a, most likely m, pessimistic b"],
        ["Variance σ²", "((b − a) / 6)²", "Uncertainty of the activity; summed along a path"],
        ["Forward pass", "ES = max(EF of predecessors); EF = ES + t<sub>e</sub>", "Earliest the activity can start / finish"],
        ["Backward pass", "LF = min(LS of successors); LS = LF − t<sub>e</sub>", "Latest without delaying the finish"],
        ["Total float", "TF = LS − ES", "Slack; TF = 0 defines the critical path"],
        ["Free float", "FF = min(ES of successors) − EF", "Slack that does not disturb any successor"],
        ["Probability", "Z = (T<sub>target</sub> − T<sub>E</sub>) / √Σσ²<sub>CP</sub>", "Classical PERT (critical path only)"],
        ["Monte Carlo", "20,000 beta-PERT samples per activity", "Captures merge bias of near-critical paths; criticality index = share of runs in which an activity is critical"],
    ]
    story.append(table(meth, [90, 170, FW - 260]))
    story.append(Spacer(1, 6))
    ex = by["L12"]
    story.append(callout(
        f"<b>Worked example - L12 R&amp;R colony and shifting:</b> a = {ex.a:g}, m = {ex.m:g}, b = {ex.b:g} months → "
        f"t<sub>e</sub> = ({ex.a:g} + 4×{ex.m:g} + {ex.b:g}) / 6 = <b>{ex.te:.2f}</b> months; σ = ({ex.b:g} − {ex.a:g}) / 6 "
        f"= {math.sqrt(ex.var):.2f}. ES = EF of L9 = {ex.es:.1f}; EF = {ex.ef:.1f}; LS = {ex.ls:.1f}; TF = {ex.tf:.1f} "
        f"→ critical.", col=ch.PHASE_COL["LAR"]))
    story.append(Spacer(1, 6))
    story.append(H2("Key modelling assumptions", toc=False))
    story += bullets([
        "Fully explored block (no GR to prepare), opencast, Government company buyer, so land vests through CBA s.11(1); "
        "a mining-lease route (private bidder) would replace L2-L6 with the State ML process.",
        "Mine opening (MS-5) follows full MS-4 (possession and R&amp;R for the rated-capacity area) in the baseline, mirroring the "
        "CMDPA sequence; scenario S3 relaxes this to phased possession.",
        "EC appraisal waits for the FC proposal to be on PARIVESH (EAC routinely asks for FC status); CTO waits for EC-linked "
        "CTE, CGWA NOC and FC Stage-II.",
        "Rail siding is excluded from the first-coal network (initial road dispatch) and tested separately against the "
        "6 MTPA year (Section 10).",
        "No resource constraints, no calendar effects (monsoon, elections) beyond what is embedded in the pessimistic values.",
    ])

    # ---------------- 7 Network results
    story.append(PageBreak())
    story += H1("Network, critical path and schedule", "CPM results")
    story.append(P(f"Expected project duration T<sub>E</sub> = <b>{R['T']:.1f} months</b> from T0 to first coal. "
                   f"Critical path: <b>{cp_names}</b>. Variance along the path to MS-5 = {R['cp_var']:.1f} "
                   f"(σ = {math.sqrt(R['cp_var']):.1f} months). Columns: a/m/b three-point estimates, t<sub>e</sub>, σ, "
                   "earliest/latest start and finish, total float (TF) and Monte Carlo criticality index (CI). Red "
                   "rows have zero total float; CI ≥ 50% means the activity drives the finish in at least half the "
                   "simulated futures."))
    rows = [["ID", "Activity", "a", "m", "b", "te", "σ", "ES", "EF", "LS", "LF", "TF", "CI"]]
    crit_rows = []
    for i, a in enumerate(acts, 1):
        nm = a.name if len(a.name) <= 62 else a.name[:60].rstrip(" ,;") + "…"
        rows.append([a.id, nm, f"{a.a:g}", f"{a.m:g}", f"{a.b:g}", f"{a.te:.1f}", f"{math.sqrt(a.var):.1f}",
                     f"{a.es:.1f}", f"{a.ef:.1f}", f"{a.ls:.1f}", f"{a.lf:.1f}", f"{max(a.tf, 0):.1f}",
                     f"{a.ci * 100:.0f}%"])
        if a.crit:
            crit_rows.append(i)
    w_num = 24.5
    tbl = table(rows, [22, FW - 22 - w_num * 11] + [w_num] * 11, font=6.5, align_right_cols=range(2, 13),
                crit_rows=crit_rows, pad=1.1)
    story.append(tbl)

    story.append(NextPageTemplate("landscape"))
    story.append(PageBreak())
    story.append(H2("Time-scaled activity-on-node network", toc=False))
    story.append(ch.NetworkDiagram(acts, LFW, 420, md.PHASES, months=66, title_w=74))
    story.append(P("Each node is placed at its earliest start (months from T0) in its phase lane; the label gives t<sub>e</sub>. "
                   "Red nodes and links form the critical path; navy diamonds mark CMDPA milestones.", "cap"))
    story.append(NextPageTemplate("portrait"))
    story.append(PageBreak())
    story.append(H2("Gantt chart with float", toc=False))
    story.append(ch.Gantt(acts, FW, md.PHASES, row_h=9.35, label_w=196, months=66))
    story.append(P("Bars: ES to EF (t<sub>e</sub>); dotted tail: total float up to LF; red: critical; diamonds: milestones.", "cap"))
    story.append(PageBreak())

    # ---------------- 8 Probability & scenarios
    story += H1("Probability, criticality and acceleration", "Risk-adjusted schedule")
    s = R["ms5_samples"]
    xs = np.linspace(34, 70, 145)
    mc_cdf = [(s <= x).mean() for x in xs]
    te = R["ms5_te"]
    sig = math.sqrt(R["cp_var"])
    pert_cdf = [0.5 * (1 + math.erf((x - te) / (sig * math.sqrt(2)))) for x in xs]
    counts, edges = np.histogram(s, bins=np.arange(34, 71, 1))
    story.append(ch.SCurve([("Monte Carlo (all paths)", xs, mc_cdf, ch.PHASE_COL["AUC"], False),
                            ("Classical PERT (critical path only)", xs, pert_cdf, ch.PHASE_COL["MOB"], True)],
                           FW, 210, (34, 70), targets=[(51, "51-month CMDPA window")],
                           xlabel="Months from vesting order to mine opening (MS-5)", hist=(edges, counts)))
    story.append(P("Cumulative probability of reaching MS-5 by a given month after vesting. The PERT curve ignores "
                   "the near-critical forest path and is therefore slightly optimistic (merge bias).", "cap"))
    prob_rows = [["Target (months after vesting)", "42", "45", "48", "51", "54", "57", "60"]]
    r1 = ["Monte Carlo probability"] + [f"{(s <= t_).mean() * 100:.0f}%" for t_ in [42, 45, 48, 51, 54, 57, 60]]
    r2 = ["PERT normal approximation"] + [f"{50 * (1 + math.erf((t_ - te) / (sig * math.sqrt(2)))):.0f}%"
                                          for t_ in [42, 45, 48, 51, 54, 57, 60]]
    story.append(table([prob_rows[0], r1, r2], [150] + [(FW - 150) / 7] * 7, align_right_cols=range(1, 8)))
    story.append(Spacer(1, 8))
    story.append(H2("Criticality index - which activities really drive the finish", toc=False))
    top = sorted(acts, key=lambda a: -a.ci)[:16]
    story.append(ch.HBars([(f"{a.id}  {a.name}", a.ci, ch.CRIT if a.crit else ch.PHASE_COL[a.phase]) for a in top],
                          FW, row_h=11.5, label_w=300))
    story.append(P("Share of 20,000 simulated schedules in which the activity lies on the longest path.", "cap"))
    story.append(CondPageBreak(200))
    story.append(H2("Acceleration scenarios (crashing and fast-tracking)"))
    srows = [["", "Scenario", "Expected", "P50", "P80", "P(≤51 m)"]]
    for code, label, r in R["scen"]:
        srows.append([code, label, f"{r['te']:.1f}", f"{r['p50']:.1f}", f"{r['p80']:.1f}", f"{r['p51'] * 100:.0f}%"])
    story.append(table(srows, [22, FW - 22 - 4 * 52, 52, 52, 52, 52], align_right_cols=range(2, 6)))
    story.append(P("Months from vesting to MS-5, 12,000 runs per scenario. Once land is accelerated (S3-S5), the "
                   "forest-clearance chain (CA land → State processing → Stage-I compliance → Stage-II) becomes "
                   "critical - so land and forest fast-tracking must be done together.", "cap"))

    # ---------------- 9 Critical activities register + heat map
    story.append(CondPageBreak(420))
    story += H1("Critical activities register", "What to watch")
    reg = [
        ["#", "Activity (ID)", "Why it is critical", "Early-warning sign", "Mitigation / owner"],
        ["1", "SES, genealogy, YADAST (L7)", "Defines PAF/PDF base; disputes stall RPDAC (BW: recorded-tenant basis)", "Families surveyed vs estimate; objections logged", "Start at s.4(1); drone + GIS; supplementary survey of actual families - LA agency / Collector"],
        ["2", "R&amp;R plan &amp; RPDAC (L9)", "RPDAC dates depend on the Collector; colony and gochar land must be fixed", "No RPDAC date 60 days after SES", "Pre-identify colony land at bid stage; RDC escalation; draft minutes ready - GMDC"],
        ["3", "R&amp;R colony &amp; shifting (L12)", "Longest single activity (8-20 months)", "Colony civil progress &lt; plan", "Phase colony; cash-in-lieu options; shift initial patch first - GMDC / MDO"],
        ["4", "CBA s.4(1) &amp; s.7(1) (L2, L3)", "Gazette queue at MoC; schedule errors restart the clock", "Draft notification returned", "Tehsildar-certified schedule; CBA-cell liaison; parcel-wise s.9 - GMDC"],
        ["5", "Compensation disbursement (L10)", "Title disputes, mutation backlog, monthly rate revisions", "Case files validated vs target", "Village-wise camps; deposit disputed sums with Tribunal (s.17) - Collector"],
        ["6", "DGPS &amp; land schedule (B4, B5)", "Every clearance consumes the certified boundary and schedule", "Certificate not in hand at vesting + 3 m", "Order DGPS on day 1 after CMDPA; ORSAC - PMC"],
        ["7", "CA land (F2)", "Suitability, mutation, PF notification; often in another district", "No suitability certificate by month 6", "Search at bid stage; accredited CA land bank - GMDC / DFO"],
        ["8", "State FC processing (F5)", "Five desks; EDS loops; ~100 working days at best", "File idle &gt;15 working days at a desk", "Desk-wise liaison; PARIVESH tracking; complete checklist - FC consultant"],
        ["9", "Stage-I compliance (F8)", "12 schemes, SSWLCP, FRA certificate, extra CA cost", "Schemes approved vs total", "Prepare schemes in parallel with Stage-I; pre-fund demands - GMDC"],
        ["10", "FRA certificate (F3)", "Prerequisite for State diversion order", "Gram Sabha quorum failures", "Early Gram Sabhas, video minutes, SDLC/DLC calendar - Collector"],
        ["11", "EC appraisal (D8)", "EAC may return/defer (BW: 03-Apr-25)", "EDS count &gt;1; adverse PH issues", "Mock EAC; elephant-corridor, cumulative-impact and R&amp;R chapters upfront - EIA consultant"],
        ["12", "CTO (K10)", "Waits for FC Stage-II; gates mine opening", "CTO queries open after FC-II", "Apply early; close all queries except FC-II - GMDC"],
        ["13", "Mine-opening gate (K12)", "Ten inputs converge; any one blocks MS-5", "Checklist items open at M-3", "Readiness board from M-6; Board paper template - PMC"],
        ["14", "Nala diversion / water (K2)", "WRD field verification and NOC", "No joint visit 60 days after DPR", "Early DPR; Chief Engineer escalation - GMDC"],
        ["15", "Rail siding (R1-R3)", "Needed before 6 MTPA; 24-36 months", "DPR not approved 30 months before 6 MTPA year", "Parallel land for siding; ECoR follow-up - GMDC / IPRCL"],
    ]
    story.append(table(reg, [18, 92, 128, 96, FW - 334], font=7.1))
    story.append(Spacer(1, 6))
    story.append(H2("Risk heat map (impact on mine-opening date)", toc=False))
    risks = [(1, 4, 4), (2, 4, 5), (3, 4, 5), (4, 3, 4), (5, 4, 3), (6, 2, 4), (7, 4, 4), (8, 4, 4), (9, 3, 4),
             (10, 3, 3), (11, 3, 3), (12, 2, 3), (13, 3, 5), (14, 3, 2), (15, 3, 2)]
    hm = ch.HeatMap(risks, FW * 0.52, 200)
    legend = [P("<b>Numbers refer to the register above.</b>", "small")] + [
        P("Top-right cells (likely and severe) are the R&amp;R chain (2, 3), the land base (1), CA land and State FC "
          "processing (7, 8) and the mine-opening gate (13). These deserve weekly PMC review, named owners at "
          "GM level and escalation triggers.", "small"),
        P("Lower-left items still need tracking but can be managed monthly.", "small")]
    t = Table([[hm, legend]], colWidths=[FW * 0.55, FW * 0.45])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(t)

    # ---------------- 10 Baitarani West status and forecast
    story.append(PageBreak())
    story += H1("Baitarani West - status and forecast", "Applying the model")
    story.append(P("Status reconstructed from the MIS of 30-Sep-2026 and later updates (FC Stage-I compliance file "
                   "forwarded by PCCF to MoEFCC on 08-Oct-26; RPDAC held 07-Oct-26). Months are offsets from the "
                   "vesting order (08-Jun-2023)."))
    vest = md.VESTING_DATE

    def mo(d):
        return (d - vest).days / 30.4375
    rows_d = [
        ("Mining plan (MS-2)", mo(dt.date(2023, 12, 8)), mo(dt.date(2023, 10, 13)), "actual"),
        ("EC (MS-3)", mo(dt.date(2024, 12, 8)), mo(dt.date(2025, 12, 3)), "actual"),
        ("FC Stage-I", mo(dt.date(2024, 12, 8)), mo(dt.date(2025, 12, 2)), "actual"),
        ("FC Stage-II", mo(dt.date(2024, 12, 8)), mo(md.add_months(md.STATUS_DATE, byw["W1"].ef + byw["W4"].te * 0)), "forecast"),
        ("CTE", mo(dt.date(2024, 12, 8)), mo(dt.date(2026, 4, 29)), "actual"),
        ("MDO contract", mo(dt.date(2024, 9, 8)), mo(dt.date(2026, 9, 17)), "actual"),
        ("Land & R&R (MS-4)", mo(dt.date(2026, 9, 8)), mo(R["bw_ms4"]["p50"]), "forecast"),
        ("Mine opening (MS-5) - phased", mo(dt.date(2027, 3, 8)), mo(R["bw_phased"]["p50"]), "forecast"),
        ("Mine opening (MS-5) - strict", mo(dt.date(2027, 3, 8)), mo(R["bw_strict"]["p50"]), "forecast"),
    ]
    ticks = [(mo(dt.date(y, m_, 1)), f"{['Jan', 'Jul'][m_ // 7]}-{str(y)[2:]}") for y in range(2023, 2028)
             for m_ in (1, 7) if dt.date(y, m_, 1) >= dt.date(2023, 7, 1)]
    story.append(ch.Dumbbell(rows_d, FW, 17, 0, mo(dt.date(2027, 11, 1)), ticks, today=mo(md.STATUS_DATE), label_w=140))
    story.append(P("Blue dot = due date (CMDPA basis; MDO from the MD's internal plan); orange = actual (solid) or P50 "
                   "forecast (hollow); red bar = delay. FC Stage-II forecast uses the expected critical chain.", "cap"))
    story.append(H2("Remaining-work network (from 14-Oct-2026)"))
    rows = [["ID", "Remaining activity", "Owner", "a", "m", "b", "te", "EF date", "TF", "CI"]]
    crit_r = []
    for i, a in enumerate(bw, 1):
        rows.append([a.id, a.name, a.owner, f"{a.a:g}", f"{a.m:g}", f"{a.b:g}", f"{a.te:.1f}",
                     md.fmt_date(md.add_months(md.STATUS_DATE, a.ef)), f"{max(a.tf, 0):.1f}", f"{a.ci * 100:.0f}%"])
        if a.crit:
            crit_r.append(i)
    tb = table(rows, [24, FW - 24 - 80 - 22 * 4 - 48 - 22 - 26, 80, 22, 22, 22, 22, 48, 22, 26], font=7,
               align_right_cols=range(3, 10), crit_rows=crit_r)
    story.append(tb)
    story.append(P(f"Critical chain (phased possession): {' → '.join(R['bw_cp'])}. W9 (R&amp;R colony and shifting) is "
                   "off the path only if the box cut is placed on a patch with no habitation.", "cap"))
    ph, stc = R["bw_phased"], R["bw_strict"]
    story.append(table([
        ["Forecast (Monte Carlo, 20,000 runs)", "Phased possession (box cut on cleared patch)", "Strict sequence (R&amp;R shifting before MS-5)"],
        ["MS-5 mine opening - P50 / P80", f"{md.fmt_date(ph['p50'])} / {md.fmt_date(ph['p80'])}", f"{md.fmt_date(stc['p50'])} / {md.fmt_date(stc['p80'])}"],
        ["P(MS-5 by CMDPA date 08-Mar-27)", f"{ph['p_ms5'] * 100:.0f}%", f"{stc['p_ms5'] * 100:.0f}%"],
        ["P(MS-5 within 51-month window, 08-Sep-27)", f"{ph['p_win'] * 100:.0f}%", f"{stc['p_win'] * 100:.0f}%"],
        ["First coal - P50 / P80", f"{md.fmt_date(ph['fc50'])} / {md.fmt_date(ph['fc80'])}", f"{md.fmt_date(stc['fc50'])} / {md.fmt_date(stc['fc80'])}"],
    ], [170, (FW - 170) / 2, (FW - 170) / 2], bold_first=True))
    story.append(Spacer(1, 6))
    story.append(callout([
        P(f"<b>Rail check.</b> With IPA in hand (18-Jan-25) the remaining DPR/ESP approvals and construction take "
          f"t<sub>e</sub> ≈ {R['rail_te']:.0f} months → siding ready ≈ <b>{R['rail_done'].strftime('%b-%Y')}</b>. Production "
          f"reaches 6 MTPA about 24 months after first coal → needed by ≈ <b>{R['rail_need'].strftime('%b-%Y')}</b>. "
          f"Float is only ~{max((R['rail_need'] - R['rail_done']).days / 30.4, 0):.0f} months: rail is near-critical "
          "for ramp-up and for the early-production rebate.", "small"),
        P("<b>MIS forecast vs model.</b> The MIS high-level chart forecasts mine opening around 15-Nov-26; the model suggests this "
          "needs FC Stage-II, the State order, CTO and possession of the box-cut land to close within ~5 weeks - "
          "possible only if every item hits its optimistic time.", "small"),
    ], col=ch.PHASE_COL["OPN"], title="Two checks the MIS does not show"))

    # ---------------- 11 Strategic levers
    story.append(PageBreak())
    story += H1("Commercial levers you may not be using", "Beyond the brief")
    lev = [
        ["Lever", "What the CMDPA / rules allow", "So what for BW"],
        ["Refund of appropriated PS", "Schedule D note 6: if MS-5 is achieved within 51 months, PS appropriated for earlier delays may be refunded",
         "₹386.8 Cr (MS-3 10% + MS-4 25%) recoverable if MS-5 by 08-Sep-27 - the strongest reason to protect the mine-opening date"],
        ["Extension for bona fide delays", "Schedule D note 4: NA may extend timelines via the Scrutiny Committee for delays not attributable to the bidder",
         "Document State-side delays (2nd upfront after s.11(1), EAC return, CA norm change, FRA) and file a reasoned representation"],
        ["Early-production rebate", "Cl. 9.2: 50% rebate on Final Offer for coal produced before the Scheduled Date of Production (75 months from vesting)",
         "Window closes 08-Sep-2029. Each Mt saves ₹16.75 Cr for every ₹1,000/t of notional price; front-load years 3-5"],
        ["Gasification incentive", "Cl. 9.3: 50% rebate on coal used/sold for gasification if ≥10% of scheduled production",
         "Explore a gasification/derivatives tie-up for G12 coal (not combinable with cl. 9.2 on the same tonnes)"],
        ["Minor mining-plan changes", "MP Guidelines 2025 para 2.9b: Board can approve ≤50% capacity increase, HEMM or infrastructure relocation",
         "Re-site box cut/infrastructure away from habitation; raise early-year output without full revision"],
        ["Production flexibility", "Cl. 16.2: ≥65% of scheduled output in a year and ≥75% over 3-year blocks",
         "Plan ramp-up and rail to stay above 65% from the first scheduled year"],
        ["Upfront adjustment", "Cl. 9.4: upfront adjusted against monthly payments, capped at 50% per month",
         "₹500 Cr is recovered from revenue share - include in the cash-flow model"],
        ["PBG revision timing", "Cl. 6.1.4: first revision at mine opening on NCI; then every April",
         "Coordinate BG limits with banks before MS-5"],
        ["Colliery Control amendment", "Board approves mine opening; intimate CCO within 15 days",
         "Saves up to ~2 months vs the old CCO permission; prepare the Board note in advance"],
    ]
    story.append(table(lev, [104, 190, FW - 294], font=7.3))
    story.append(Spacer(1, 8))

    # ---------------- 12 Tracker reconciliation
    story += H1("Reconciliation of 'Final Tracker_cl.xlsx'", "Using the old tracker properly")
    story.append(P("The workbook (sheets BP, BW_, Partner Onboarding, Support Activities, HO Core Team) dates from "
                   "mid-2023. Its activity lists are useful; its dates are stale and several procedures have changed. "
                   "Item-by-item:"))
    rec = [
        ["Tracker block", "What it says", "Current position / correction"],
        ["A1 Contract formalisation", "'Agreement signing 08-Jun-23'", "CMDPA signed 29-Mar-23; 08-Jun-23 is the vesting order date"],
        ["P1-P6 Preliminary", "DGPS Aug-Oct-23; GR soft copy 13-Jul-23", "DGPS by CMPDIL completed 12-Jan-24; continue to use for CA land and siding surveys"],
        ["MP1-MP14 Mining plan", "Fresh plan, MoC approval Nov/Dec-23", "Not needed: OMC plan (10-Nov-21) deemed transferred; MS-2 met. Revise only for optimisation"],
        ["FC1-FC30 Forest clearance", "Old Part I-V file movement (FCR 2003)", "Superseded by VSSR 2023 / PARIVESH 2.0; Stage-I 02-Dec-25; Stage-II pending at MoEFCC"],
        ["FRA1-FRA9", "Collector-led FRA process", "Still valid; certificate pending - now on the critical path for the State order"],
        ["CA1-CA13 / TE1-TE10 / WLCP1-4", "CA land, tree enumeration, wildlife plan", "Done: TE (Jun-24), CA land Koraput mutated & PF-notified (11-Jun-26), SSWLCP and elephant-corridor NOC (25-Aug-25)"],
        ["EC1-EC19", "Form-1 Oct-Nov-23 onwards", "ToR transferred 06-Nov-23; EC granted 03-Dec-25"],
        ["ML1-ML12 Mining lease", "State ML via Collector, DGM, MRD, MoC prior approval", "Not required for CBA land: s.11(1) order (13-Oct-23) substitutes for ML; confirm whether State wants a lease for Govt/forest parcels"],
        ["LA1-LA50 Land &amp; R&amp;R", "RFCTLARR 2013 s.4 SIA, s.11, s.19, s.21, s.23, s.38", "Wrong statute for this route - replace with CBA s.4(1)/7(1)/8/9(1)/10/11(1)/12/13-14/17 plus RFCTLARR Sch. I-III (S.O. 2368(E)) and ORRP 2006 RPDAC"],
        ["CTE1-CTE6 / CTO1-CTO5", "~60 days each", "CTE took ~4 months (02-Jan to 29-Apr-26); CTO applied 08-Jul-26, pending FC-II"],
        ["MO1-MO9 Mine opening", "'Grant of mine opening permission by Coal Controller'", "Replaced by Board approval + CCO intimation (Colliery Control (Amendment) Rules 2025/2026); escrow done"],
        ["Partner Onboarding", "Tenders for MP, EC+FC, LA, DPR, MDO (2023)", "All agencies onboard; MDO LoI 13-Nov-25, contract 17-Sep-26"],
        ["HO Core Team deadlines", "EC/FC 07-Dec-24; LA 07-Sep-26; opening 07-Mar-27", "EC met 12 months late; MS-4 overdue; MS-5 at risk - see Section 10"],
        ["Missing altogether", "-", "CGWA NOC, WRD water &amp; nala NOC, power, PESO licences, DGMS notices &amp; manager, CMPF/CLRA, royalty/DMF/NMET/i3MS, grade declaration, GCT rail approvals, approach road, RPDAC, SES/genealogy/YADAST, R&amp;R colony &amp; gochar land, upfront 3rd/4th, PBG transfer, extension request"],
    ]
    story.append(table(rec, [104, 130, FW - 234], font=7.2))

    # ---------------- 13 Recommendations
    story.append(PageBreak())
    story += H1("Recommendations and 90-day action plan", "What to do next")
    act_rows = [
        ["#", "Action", "Owner", "By"],
        ["1", "Daily follow-up of FC Stage-I compliance at MoEFCC (FC division) and IRO; pre-empt queries", "GMDC FC cell / DCS", "Nov-26"],
        ["2", "Obtain FRA certificate (DLC Angul) - prerequisite for the State diversion order", "GMDC / Collector", "Oct-26"],
        ["3", "Secure nala-diversion NOC from WRD (joint report submitted 29-Apr-26)", "GMDC", "Oct-26"],
        ["4", "Close all CTO observations except FC-II so CTO issues within days of Stage-II", "GMDC Env cell", "Nov-26"],
        ["5", "Finalise and validate 199-ha case files; village-wise disbursement camps; execute Govt-land possession", "BNB / Collector", "Dec-26"],
        ["6", "Notify R&amp;R scheme after RPDAC; lock R&amp;R colony and gochar land; start colony civil works", "Collector / GMDC", "Jan-27"],
        ["7", "Supplementary SES for extended/actual families to de-risk R&amp;R entitlements", "BNB", "Dec-26"],
        ["8", "Fix the box-cut patch on Govt/acquired land with no habitation; complete tree cutting there", "GMDC / MDO", "Nov-26"],
        ["9", "DGMS Form I-A notice, manager appointment, SMP; PESO magazine & HSD licences", "MDO / GMDC", "Dec-26"],
        ["10", "Mine-opening readiness board (all approvals) and Board note; fund 3rd upfront ₹125 Cr and PBG transfer", "PMC / Finance", "Jan-27"],
        ["11", "File extension representation to NA for delays not attributable to GMDC", "GMDC / PMC", "Dec-26"],
        ["12", "Push ECoR DPR/ESP approval; acquire siding and coal-stock land at Jharpada", "GMDC / IPRCL", "Mar-27"],
        ["13", "Customer contracts and grade declaration; royalty/DMF/NMET and i3MS registrations", "Marketing / Finance", "Feb-27"],
        ["14", "Enforce contractual LDs on agencies that missed milestones, without stalling deliverables", "GMDC Contracts", "Ongoing"],
        ["15", "Replace the 2023 tracker with the activity list in Section 5 and this report's network", "PMC", "Nov-26"],
    ]
    story.append(table(act_rows, [16, FW - 16 - 112 - 46, 112, 46], font=7.5))
    story.append(Spacer(1, 8))
    story.append(H2("Governance rhythm the PMC should run", toc=False))
    story += bullets([
        "<b>Weekly</b>: critical-chain stand-up (land, R&amp;R, FC-II, CTO, possession) with named owners and a two-week look-ahead.",
        "<b>Fortnightly</b>: desk-level tracking of every file in Government (date received, days idle, next action) - VSSR and "
        "the Mining Plan Guidelines publish desk timelines that can be cited in escalations.",
        "<b>Monthly</b>: re-run this PERT/CPM model with actuals; publish P50/P80 dates for MS-4, MS-5 and first coal; "
        "report the efficiency-parameter status to the Nominated Authority.",
        "<b>Quarterly</b>: Board-level review of performance-security exposure, the 51-month window and the early-production rebate.",
    ])
    story.append(Spacer(1, 6))
    story.append(callout(
        "For a <b>new</b> Odisha block, the biggest gains come before and immediately after the bid: price and plan R&amp;R "
        "and CA land into the bid, order DGPS and the land schedule on day 1, run land and forest tracks in parallel from "
        "s.4(1), and design the first-year box cut away from habitation.", col=ch.PHASE_COL["LAR"],
        title="Lessons for the next block"))

    # ---------------- Annex
    story.append(PageBreak())
    story.append(P("ANNEX", "kicker"))
    a = Paragraph("A&nbsp;&nbsp;Glossary", S["h1"])
    a._toc = (0, "Annex A  Glossary")
    story += [a, Rule(FW, NAVY, 1.2), Spacer(1, 4)]
    g = ct.GLOSSARY
    half = math.ceil(len(g) / 2)
    grows = [["Term", "Meaning", "Term", "Meaning"]]
    for i in range(half):
        l_ = g[i]
        r_ = g[i + half] if i + half < len(g) else ("", "")
        grows.append([l_[0], l_[1], r_[0], r_[1]])
    story.append(table(grows, [62, FW / 2 - 62, 62, FW / 2 - 62], font=7.3,
                       extra=[("FONTNAME", (0, 1), (0, -1), "Carlito-Bold")]))
    story.append(Spacer(1, 4))
    b = Paragraph("B&nbsp;&nbsp;Sources", S["h1"])
    b._toc = (0, "Annex B  Sources")
    story += [b, Rule(FW, NAVY, 1.2), Spacer(1, 4)]
    story.append(H2("Web sources (retrieved October 2026 via Firecrawl)", toc=False))
    srows = [["#", "Source", "Location"]] + [[str(i), s_, u] for i, (s_, u) in enumerate(ct.SOURCES_WEB, 1)]
    story.append(table(srows, [16, FW * 0.55, FW * 0.45 - 16], font=7))
    story.append(H2("Project documents in the repository", toc=False))
    story += bullets(ct.SOURCES_REPO, "bullet")
    story.append(P("<i>Statutory limits are as published at retrieval; three-point durations are professional estimates "
                   "to be refreshed monthly with actuals. Not legal advice.</i>", "small"))

    doc = Doc(OUT, title="Coal Mining PMC", author="PMC - GMDC Odisha Coal",
              subject="Auction to operationalisation of a coal block in Odisha: process map, PERT/CPM")
    doc.multiBuild(story)
    return R


class LaneMap9(ch.LaneMap):
    """LaneMap with lane colour codes distinct from lane keys."""

    def __init__(self, width, height, lanes3, boxes, links):
        self.lane_col = {k: c for k, _, c in lanes3}
        super().__init__(width, height, [(k, l) for k, l, _ in lanes3], boxes, links, title_w=96)

    def draw(self):
        orig = dict(ch.PHASE_COL)
        for k, c in self.lane_col.items():
            ch.PHASE_COL[k] = orig[c]
        try:
            super().draw()
        finally:
            ch.PHASE_COL.clear()
            ch.PHASE_COL.update(orig)


if __name__ == "__main__":
    R = build()
    print("Wrote", OUT)
    print("p51", R["p51"], "ms5_te", R["ms5_te"])
    print("BW phased", {k: v for k, v in R["bw_phased"].items() if k != "samples"})
    print("BW strict", {k: v for k, v in R["bw_strict"].items() if k != "samples"})
    print("BW MS4", R["bw_ms4"], "rail", R["rail_done"], R["rail_need"])
    for code, label, r in R["scen"]:
        print(code, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k != "cp"})
