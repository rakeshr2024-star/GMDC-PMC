"""PERT / CPM model for an Odisha commercial coal block (CBA Act land route).

Two networks are defined:

* GENERIC  - a fresh fully-explored block, from tender launch to first coal.
* BW_REM   - Baitarani West remaining work, from the status date 14-Oct-2026.

Durations are three-point estimates (a = optimistic, m = most likely,
b = pessimistic) in MONTHS. They are calibrated on statutory time limits
(CBA Act, EIA Notification 2006, VSSR 2023, Mining Plan Guidelines 2025,
GCT policy) and on the actual durations observed on Baitarani West and
other Odisha blocks reviewed by the Nominated Authority.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import numpy as np

PHASES = [
    ("AUC", "Auction & vesting"),
    ("MOB", "Mobilisation & surveys"),
    ("MPL", "Mining plan"),
    ("ENV", "Environment clearance"),
    ("FOR", "Forest clearance"),
    ("LAR", "Land acquisition (CBA) & R&R"),
    ("OPN", "Consents, infrastructure & mine opening"),
]


@dataclass
class Act:
    id: str
    name: str
    phase: str
    owner: str
    a: float
    m: float
    b: float
    preds: list = field(default_factory=list)
    ref: str = ""
    milestone: str = ""
    # computed
    te: float = 0.0
    var: float = 0.0
    es: float = 0.0
    ef: float = 0.0
    ls: float = 0.0
    lf: float = 0.0
    tf: float = 0.0
    ff: float = 0.0
    crit: bool = False
    ci: float = 0.0  # criticality index (Monte Carlo)

    def __post_init__(self):
        self.te = (self.a + 4 * self.m + self.b) / 6.0
        self.var = ((self.b - self.a) / 6.0) ** 2


def A(*args, **kw):
    return Act(*args, **kw)


# ---------------------------------------------------------------------------
# GENERIC NETWORK  (T0 = launch of tender by Nominated Authority)
# ---------------------------------------------------------------------------
GENERIC = [
    # --- Auction & vesting ---
    A("A1", "Study tender document, data room, mine dossier & GR", "AUC", "Bidder", 0.5, 1, 1.5, [], "Tender Document"),
    A("A2", "Site visit; techno-commercial, land, forest, R&R & logistics due diligence", "AUC", "Bidder", 0.5, 1, 2, ["A1"]),
    A("A3", "Financial model, bid strategy, Board/State approvals, bid security (20% of upfront)", "AUC", "Bidder", 0.5, 1, 2, ["A2"]),
    A("A4", "Technical bid + Initial Offer on MSTC; evaluation; technically qualified bidders", "AUC", "NA / MSTC", 0.7, 1, 1.5, ["A3"]),
    A("A5", "Ascending forward e-auction; preferred bidder; Central Govt approval", "AUC", "NA / MoC", 0.5, 1, 2, ["A4"], "CM(SP) Rules"),
    A("A6", "Execute CMDPA with Nominated Authority", "AUC", "NA + Bidder", 0.3, 0.5, 1, ["A5"], "CMDPA"),
    A("A7", "1st upfront instalment, performance security, fixed amount; completion notice", "AUC", "Bidder", 0.7, 1.5, 2, ["A6"], "CMDPA cl. 3, 5, 6"),
    A("A8", "Vesting / allotment order issued (efficiency clock starts)", "AUC", "NA", 0.3, 0.7, 1.5, ["A7"], "CM(SP) s.8", "Zero date"),
    # --- Mobilisation & surveys ---
    A("B1", "Project organisation, PMC, Odisha office, SWCS registration", "MOB", "Bidder", 0.5, 1, 2, ["A6"]),
    A("B2", "Tender & onboard consultants (MPPA, NABET EIA, FC/LA/R&R, DGPS, rail DPR)", "MOB", "Bidder", 1.5, 3, 5, ["A6"]),
    A("B3", "Obtain GR, borehole data & mine dossier (CMPDI / NA)", "MOB", "CMPDI", 0.5, 1, 2, ["A8"]),
    A("B4", "DGPS boundary survey & CMPDI/ORSAC certification with KML", "MOB", "CMPDI / ORSAC", 1, 2, 4, ["B2", "A8"]),
    A("B5", "Cadastral maps, RoR, plot-wise land schedule certified by RI/Tehsildar", "MOB", "Revenue Dept", 2, 3, 6, ["B4"]),
    # --- Mining plan ---
    A("C1", "Mine design, draft Mining Plan + Mine Closure Plan, peer review, Board approval", "MPL", "MPPA / QP", 2, 3, 5, ["B3", "B4"], "MP Guidelines 2025"),
    A("C2", "SWCS submission; Technical Committee scrutiny & compliance (max 2 rounds)", "MPL", "CCO / MoC", 1, 1.5, 3, ["C1"], "MP Guidelines 2025"),
    A("C3", "Approval, in-principle approval & final approval of Mining Plan", "MPL", "CCO / NA", 0.5, 1, 2, ["C2"], "MCR 2020", "MS-2"),
    # --- Environment clearance ---
    A("D1", "Form-1/CAF + PFR; ToR application on PARIVESH", "ENV", "EIA consultant", 0.5, 1, 1.5, ["C1"], "EIA Notif. 2006"),
    A("D2", "EAC (Coal Mining) appraisal; grant of ToR (60 days)", "ENV", "MoEFCC", 1, 2, 4, ["D1"], "EIA Notif. para 7(ii)"),
    A("D3", "Baseline monitoring - one season (air, water, noise, soil, ecology, socio-economy)", "ENV", "EIA consultant", 3, 3.5, 5, ["D1"]),
    A("D4", "Specialised studies: hydrogeology/GW model, HEC & wildlife, traffic, slope, R&R", "ENV", "Consultants", 2, 3, 5, ["D2", "D3"]),
    A("D5", "Draft EIA/EMP + Odia summary to OSPCB; PH notice (30 days)", "ENV", "Consultant / OSPCB", 1, 1.5, 3, ["D4"]),
    A("D6", "Public hearing (within 45 days) and proceedings to MoEFCC", "ENV", "Collector / OSPCB", 1, 1.5, 4, ["D5"], "EIA App. IV"),
    A("D7", "Final EIA/EMP incorporating PH; EC application", "ENV", "Consultant", 1, 1.5, 3, ["D6"]),
    A("D8", "EDS/ADS, EAC appraisal & grant of EC (105 days)", "ENV", "MoEFCC / EAC", 2.5, 4, 10, ["D7", "F4"], "EIA Notif. para 8", "MS-3"),
    # --- Forest clearance ---
    A("F1", "Tree enumeration (FMIS maps, committee, DFO approval)", "FOR", "Forest Dept", 2, 3, 6, ["B5"]),
    A("F2", "CA land: identify, Collector NOC, DGPS/DSS, DFO suitability, CA scheme", "FOR", "Revenue / Forest", 3, 5, 10, ["B5"], "VSSR 2023 r.11"),
    A("F3", "FRA 2006: Gram Sabha resolutions, SDLC/DLC, Collector FRA certificate", "FOR", "Collector / Gram Sabha", 3, 6, 12, ["B5"], "FRA 2006"),
    A("F4", "FC proposal (Form-A) on PARIVESH 2.0 with KML, NOCs, draft SSWLCP", "FOR", "User agency", 1, 1.5, 3, ["C1", "F1"], "VSSR 2023"),
    A("F5", "State processing: DFO/DC, CF, Nodal/PCCF, PSC, State Govt (~100 working days)", "FOR", "State Forest Dept", 4, 7, 14, ["F4", "F2"], "VSSR 2023 Sch."),
    A("F6", "IRO inspection, Advisory Committee (FAC), Stage-I in-principle approval", "FOR", "MoEFCC", 2, 4, 9, ["F5"], "Adhiniyam s.2"),
    A("F7", "Demand notes & payment (NPV, CA, SMC, WLMP); CA land mutation & PF notification", "FOR", "DFO / Revenue", 2, 4, 8, ["F6"]),
    A("F8", "Stage-I compliance: schemes, SSWLCP (CWLW), FRA certificate, compliance file", "FOR", "Forest Dept", 3, 6, 12, ["F7", "F3"]),
    A("F9", "Stage-II (final) approval and State Govt diversion order", "FOR", "MoEFCC / State", 1, 2, 5, ["F8"], "VSSR 2023 r.9"),
    A("F10", "Tree felling (OFDC), working permission & possession of forest land", "FOR", "DFO / OFDC", 1, 2, 4, ["F9"]),
    # --- Land acquisition under CBA Act & R&R ---
    A("L1", "Land schedule & requisition to MoC for CBA notifications", "LAR", "GMDC / Collector", 1, 2, 4, ["B5"]),
    A("L2", "Sec 4(1) notification - intention to prospect", "LAR", "MoC", 1, 3, 6, ["L1"], "CBA s.4(1)"),
    A("L3", "Sec 7(1) notice of intention to acquire (within 2 yrs of 4(1))", "LAR", "MoC", 2, 4, 8, ["L2"], "CBA s.7(1)"),
    A("L4", "Sec 8 objections (30 days); hearing & report by Competent Authority", "LAR", "Competent Authority", 1, 2, 4, ["L3"], "CBA s.8"),
    A("L5", "Sec 9(1) declaration (within 3 yrs of 7(1)); Sec 10 vesting", "LAR", "MoC", 2, 4, 8, ["L4"], "CBA s.9, 10"),
    A("L6", "Sec 11(1) order vesting land in Govt company; 2nd upfront instalment", "LAR", "MoC", 0.5, 1.5, 3, ["L5"], "CBA s.11(1)"),
    A("L7", "SES, genealogy & YADAST asset enumeration; PAF/PDF lists", "LAR", "R&R agency / Collector", 6, 10, 16, ["L3"], "RFCTLARR Sch. II"),
    A("L8", "Compensation determination & award (First Schedule via S.O. 2368(E))", "LAR", "Competent Authority", 2, 4, 8, ["L6", "L7"], "CBA s.13-14"),
    A("L9", "R&R plan, colony & gochar land; RPDAC approval (ORRP 2006 / Sch. II)", "LAR", "Collector / RPDAC", 4, 8, 15, ["L7"], "ORRP 2006"),
    A("L10", "Case files, deposit & disbursement of compensation and R&R", "LAR", "Collector / GMDC", 4, 8, 14, ["L8", "L9"], "CBA s.17"),
    A("L11", "Government land: alienation/premium payment and handover", "LAR", "Revenue & DM Dept", 3, 6, 12, ["L6"]),
    A("L12", "R&R colony development and shifting of displaced families", "LAR", "GMDC / Collector", 8, 12, 20, ["L9"], "RFCTLARR Sch. III"),
    A("L13", "Physical possession of land for rated capacity (first 5 yrs)", "LAR", "Competent Authority", 1, 2, 4, ["L10", "L11", "L12"], "CBA s.12", "MS-4"),
    # --- Consents, infrastructure & mine opening ---
    A("K1", "CGWA NOC (NOCAP) for dewatering & GW abstraction", "OPN", "CGWA", 2, 3, 6, ["D4"], "CGWA Guidelines 2020"),
    A("K2", "Water allocation & nala diversion permission (WRD)", "OPN", "WRD Odisha", 3, 6, 12, ["C3", "D4"]),
    A("K3", "Consent to Establish (OSPCB / OCMMS)", "OPN", "OSPCB", 2, 3, 5, ["D8"], "Water & Air Acts"),
    A("K4", "Power: load sanction, line & substation", "OPN", "TPCODL / OPTCL", 4, 6, 10, ["C3"]),
    A("K5", "MDO / turnkey contractor: RFP, bidding, evaluation, LoA, contract", "OPN", "GMDC", 6, 9, 14, ["C3"]),
    A("K6", "Contractor mobilisation: PBG, site handover, HEMM, workshop", "OPN", "MDO", 2, 3, 5, ["K5", "K3"]),
    A("K7", "Approach road & interim road-dispatch set-up (weighbridge, coal yard)", "OPN", "GMDC / MDO", 4, 6, 10, ["K3"]),
    A("K8", "Explosives (PESO LE-3 magazine) & petroleum storage licences", "OPN", "PESO / DM", 2, 3, 5, ["K5"], "Explosives Rules 2008"),
    A("K9", "DGMS: Form I-A notice (≥30 days), manager appointment, SMP", "OPN", "DGMS", 1, 1.5, 3, ["K5"], "CMR 2017 reg. 3"),
    A("K10", "Consent to Operate (OSPCB)", "OPN", "OSPCB", 1.5, 2.5, 4, ["K3", "F9", "K1"]),
    A("K11", "Escrow account for progressive mine closure (CCO beneficiary)", "OPN", "GMDC / CCO", 0.5, 1, 2, ["C3"], "MP Guidelines 2025"),
    A("K12", "Board approval of mine opening; intimation to CCO; 3rd upfront; PBG to State", "OPN", "GMDC Board", 0.5, 1, 1.5,
      ["K10", "F10", "L13", "K6", "K8", "K9", "K11", "K2", "K4", "K7"], "CCR 2004 r.9 (amended)", "MS-5"),
    A("K13", "Box cut, OB removal and coal exposure", "OPN", "MDO", 2, 3, 5, ["K12"]),
    A("K14", "Commercial readiness: royalty/DMF/NMET, i3MS e-permit, grade declaration, sales", "OPN", "GMDC", 1, 2, 3, ["K12"]),
    A("K15", "First coal production & dispatch; 4th upfront instalment", "OPN", "GMDC / MDO", 0.3, 0.5, 1, ["K13", "K14"], "", "First coal"),
]

# Rail evacuation is not needed for first coal (initial road dispatch) but the EC
# condition requires the siding before production reaches 6 MTPA.
RAIL = [
    ("R1", "GCT application, joint survey & in-principle approval", 0.7, 1, 2),
    ("R2", "DPR / ESP / SIP approvals, land for siding & corridor", 4, 8, 14),
    ("R3", "Construction, OHE & signalling; CRS inspection & commissioning", 14, 20, 30),
]


# ---------------------------------------------------------------------------
# BAITARANI WEST - remaining work from status date 14-Oct-2026
# ---------------------------------------------------------------------------
STATUS_DATE = dt.date(2026, 10, 14)
VESTING_DATE = dt.date(2023, 6, 8)

BW_REM = [
    A("W1", "MoEFCC processing of Stage-I compliance; Stage-II approval", "FOR", "MoEFCC", 0.7, 2, 5, []),
    A("W2", "FRA certificate / NOC from DLC & Collector (overdue)", "FOR", "Collector Angul", 0.5, 1.5, 4, []),
    A("W3", "Nala diversion NOC from WRD", "OPN", "WRD Odisha", 0.3, 1, 3, []),
    A("W4", "State Govt diversion order (after Stage-II & FRA)", "FOR", "Forest Dept", 0.3, 0.7, 1.5, ["W1", "W2"]),
    A("W5", "Tree felling & possession of 64.37 ha forest land", "FOR", "DFO / OFDC", 0.7, 1.5, 3, ["W4"]),
    A("W6", "R&R scheme finalisation after RPDAC (07-Oct-26)", "LAR", "Collector / RDC", 0.5, 1.5, 3, []),
    A("W7", "Case files (199 ha) & compensation disbursement, 5-yr area", "LAR", "BNB / Collector", 1, 2.5, 6, []),
    A("W8", "Physical possession of 5-yr private & Govt land", "LAR", "Collector / GMDC", 0.5, 1, 3, ["W6", "W7"]),
    A("W9", "R&R colony land, development & shifting of PDFs", "LAR", "GMDC / Collector", 4, 8, 15, ["W6"]),
    A("W10", "Consent to Operate (pending FC Stage-II)", "OPN", "OSPCB", 0.5, 1, 2.5, ["W4"]),
    A("W11", "MDO mobilisation (HEMM, workshop, magazine)", "OPN", "MDO", 0.5, 1.5, 3, []),
    A("W12", "DGMS notices & appointments; explosives/HSD licences", "OPN", "DGMS / PESO", 0.5, 1.5, 3, []),
    A("W13", "Tree cutting on Govt & acquired private land", "OPN", "Forest / GMDC", 0.5, 1, 2.5, []),
    A("W14", "Board approval of mine opening; CCO intimation; 3rd upfront", "OPN", "GMDC Board", 0.2, 0.5, 1,
      ["W5", "W8", "W10", "W11", "W12", "W13", "W3"], "", "MS-5"),
    A("W15", "Box cut & start of OB removal", "OPN", "MDO", 0.5, 1, 2, ["W14"]),
    A("W16", "Coal exposure & first coal dispatch by road", "OPN", "GMDC / MDO", 2, 4, 7, ["W15"], "", "First coal"),
]


# ---------------------------------------------------------------------------
def cpm(acts: list[Act]):
    by = {x.id: x for x in acts}
    order = topo(acts)
    for aid in order:
        x = by[aid]
        x.es = max((by[p].ef for p in x.preds), default=0.0)
        x.ef = x.es + x.te
    T = max(x.ef for x in acts)
    succ = {x.id: [] for x in acts}
    for x in acts:
        for p in x.preds:
            succ[p].append(x.id)
    for aid in reversed(order):
        x = by[aid]
        x.lf = min((by[s].ls for s in succ[aid]), default=T)
        x.ls = x.lf - x.te
        x.tf = x.ls - x.es
        x.ff = min((by[s].es for s in succ[aid]), default=T) - x.ef
        x.crit = x.tf < 1e-6
    return T, succ


def topo(acts):
    by = {x.id: x for x in acts}
    seen, out = set(), []

    def visit(n):
        if n in seen:
            return
        for p in by[n].preds:
            visit(p)
        seen.add(n)
        out.append(n)

    for x in acts:
        visit(x.id)
    return out


def critical_path(acts, end_id):
    """Trace the zero-float chain back from end_id."""
    by = {x.id: x for x in acts}
    path = [end_id]
    cur = by[end_id]
    while cur.preds:
        best = max(cur.preds, key=lambda p: by[p].ef)
        path.append(best)
        cur = by[best]
    return list(reversed(path))


def beta_pert_samples(rng, a, m, b, n):
    if b - a < 1e-9:
        return np.full(n, m)
    al = 1 + 4 * (m - a) / (b - a)
    be = 1 + 4 * (b - m) / (b - a)
    return a + rng.beta(al, be, n) * (b - a)


def monte_carlo(acts, n=20000, seed=7, track=None, override_preds=None):
    """Return dict of finish-time arrays for `track` ids and criticality index."""
    rng = np.random.default_rng(seed)
    order = topo(acts)
    by = {x.id: x for x in acts}
    preds = {x.id: list(x.preds) for x in acts}
    if override_preds:
        preds.update(override_preds)
    dur = {x.id: beta_pert_samples(rng, x.a, x.m, x.b, n) for x in acts}
    ef = {}
    argp = {}
    for aid in order:
        ps = preds[aid]
        if ps:
            stack = np.vstack([ef[p] for p in ps])
            es = stack.max(axis=0)
            argp[aid] = np.array(ps)[stack.argmax(axis=0)]
        else:
            es = np.zeros(n)
            argp[aid] = None
        ef[aid] = es + dur[aid]
    end = max(by, key=lambda k: by[k].ef) if track is None else track[-1]
    # criticality index: walk back along driving predecessor per sample
    counts = {k: 0 for k in by}
    endarr = np.full(n, end, dtype=object)
    on = {k: np.zeros(n, dtype=bool) for k in by}
    cur = endarr
    for _ in range(len(order)):
        for k in by:
            mask = cur == k
            on[k] |= mask
        nxt = np.empty(n, dtype=object)
        nxt[:] = None
        for k in by:
            mask = cur == k
            if mask.any() and argp[k] is not None:
                nxt[mask] = argp[k][mask]
        if all(v is None for v in nxt):
            break
        cur = nxt
    for k in by:
        counts[k] = on[k].mean()
    return ef, counts


def add_months(d: dt.date, months: float) -> dt.date:
    return d + dt.timedelta(days=months * 30.4375)


def fmt_date(d: dt.date) -> str:
    return d.strftime("%d-%b-%y")


if __name__ == "__main__":
    T, _ = cpm(GENERIC)
    by = {x.id: x for x in GENERIC}
    print("Generic project duration (te):", round(T, 1))
    print("Vesting at", round(by["A8"].ef, 1), " MS-5 at", round(by["K12"].ef, 1),
          " -> months after vesting:", round(by["K12"].ef - by["A8"].ef, 1))
    cp = critical_path(GENERIC, "K15")
    print("CP:", " > ".join(cp))
    print("CP variance:", round(sum(by[k].var for k in cp), 2))
    for x in GENERIC:
        print(f"{x.id:4} te={x.te:5.2f} ES={x.es:5.1f} EF={x.ef:5.1f} TF={x.tf:5.1f} {'CRIT' if x.crit else ''}")
    ef, ci = monte_carlo(GENERIC)
    ms5 = ef["K12"] - ef["A8"]
    print("MC MS-5 after vesting: mean", ms5.mean().round(1), "P50", np.percentile(ms5, 50).round(1),
          "P80", np.percentile(ms5, 80).round(1), "P(<=51)", (ms5 <= 51).mean().round(3))
    print({k: round(v, 2) for k, v in ci.items() if v > 0.05})
    T2, _ = cpm(BW_REM)
    byw = {x.id: x for x in BW_REM}
    print("BW MS-5 te:", round(byw["W14"].ef, 2), fmt_date(add_months(STATUS_DATE, byw["W14"].ef)))
    print("BW CP:", critical_path(BW_REM, "W16"))
    efw, ciw = monte_carlo(BW_REM)
    for tgt, lab in [(dt.date(2027, 3, 8), "MS-5 CMDPA"), (dt.date(2027, 9, 8), "51-month window")]:
        mo = (tgt - STATUS_DATE).days / 30.4375
        print(lab, mo.__round__(2), "P=", (efw["W14"] <= mo).mean().round(3))
    strict = monte_carlo(BW_REM, override_preds={"W14": ["W5", "W8", "W9", "W10", "W11", "W12", "W13", "W3"]})[0]
    for tgt, lab in [(dt.date(2027, 3, 8), "MS-5 CMDPA"), (dt.date(2027, 9, 8), "51-month window")]:
        mo = (tgt - STATUS_DATE).days / 30.4375
        print("strict", lab, "P=", (strict["W14"] <= mo).mean().round(3), "P50", fmt_date(add_months(STATUS_DATE, np.percentile(strict["W14"], 50))))
