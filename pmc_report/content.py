"""Narrative content and granular activity lists for each process chapter."""

# Each process: flowchart steps (summary) + granular table rows
# row = (activity, responsible, legal / reference, typical time)

PROCESSES = [
    {
        "code": "AUC",
        "title": "Pre-bid, e-auction, CMDPA and vesting",
        "intro": (
            "Commercial coal blocks are auctioned by the Nominated Authority (NA), Ministry of Coal, under the "
            "Coal Mines (Special Provisions) Act, 2015 and the MMDR Act, 1957, on the MSTC e-platform. The bid "
            "parameter is the <b>percentage share of revenue</b> payable to the State (floor 4%; increments of 0.5% up "
            "to 10% and 0.25% thereafter). There is no end-use restriction, no technical or financial eligibility "
            "threshold and 100% FDI is allowed under the automatic route. A two-stage process applies: technical bid "
            "plus initial offer, then an ascending forward e-auction among qualified bidders. Baitarani West was won by "
            "GMDC at a <b>Final Offer of 33.50%</b> (16th tranche under CM(SP) Act; CMDPA signed 29-Mar-2023; vesting "
            "order NA-104/4/2023-NA dated 08-Jun-2023)."
        ),
        "flow": [
            dict(t="Tranche launch; buy tender document; MSTC registration", who="NA / Bidder", d="Day 0-30"),
            dict(t="Data room: GR, mine dossier, DGPS boundary, valuation", who="CMPDI / Bidder", d="2-4 wks"),
            dict(t="Pre-bid queries, site visit and due diligence", who="Bidder", d="4-6 wks"),
            dict(t="Financial model, Board/State approval, bid security", who="Bidder", d="3-6 wks"),
            dict(t="Technical bid + Initial Offer on MSTC; offline originals", who="Bidder", d="Bid due date"),
            dict(t="Evaluation, ranking and elimination of TQBs", who="NA", d="2-4 wks"),
            dict(t="Ascending forward e-auction; Preferred Bidder", who="NA / MSTC", d="1 day/mine"),
            dict(t="Central Govt approval: Successful Bidder", who="MoC", d="2-4 wks"),
            dict(t="Execute CMDPA", who="NA + SB", d="1-2 wks", crit=True),
            dict(t="1st upfront (25%), performance security, fixed amount", who="SB", d="≤40 business days", crit=True),
            dict(t="Completion notice; vesting / allotment order", who="NA", d="2-6 wks", ms="Zero date"),
            dict(t="Transfer of prior allottee approvals (MP, ToR, CBA, FC files)", who="NA / MoEFCC / CCO", d="1-5 months"),
        ],
        "table": [
            ("Track tranche notices; shortlist blocks on reserves, grade, strip ratio, land/forest share, logistics", "Bidder (strategy)", "MoC tranche notice", "Continuous"),
            ("Register on MSTC with DSC; purchase tender document", "Bidder", "Tender Document", "Before cut-off"),
            ("Data-room review: Geological Report, mine dossier, drone survey, valuation, prior-allottee data", "Bidder / CMPDI", "Tender Document", "2-4 weeks"),
            ("Submit written queries; attend pre-bid meeting; track corrigenda", "Bidder / NA", "Tender schedule", "Per schedule"),
            ("Request and carry out site visit (villages, forest patches, nalas, roads, rail heads, power, water)", "Bidder", "Tender schedule", "1-2 weeks"),
            ("Legal & social due diligence: land schedule split, Fifth Schedule/PESA status, ESZ & elephant corridors within 10 km, R&R magnitude", "Bidder / advisors", "PESA 1996, WPA 1972", "2-4 weeks"),
            ("Market & logistics study: NCI-linked price, customers, evacuation route & cost", "Bidder (marketing)", "National Coal Index", "2-4 weeks"),
            ("Financial model: capex, MDO rates, revenue share, royalty 14% ad valorem, DMF 10% of royalty, NMET 2%", "Bidder (finance)", "MMDR s.9, 9B, 9C", "2-3 weeks"),
            ("Board approval (and State Govt approval for a State PSU) of bid ceiling and funding", "Board / State Govt", "Companies Act 2013", "1-3 weeks"),
            ("Bid security: 20% of upfront amount (fully explored) as BG/RTGS; 210-day validity + 60-day claim", "Bidder", "Tender Document", "1 week"),
            ("Prepare technical bid: eligibility affidavits, undertakings, POA, affiliate declarations", "Bidder", "Tender Document", "2 weeks"),
            ("Online submission on MSTC (technical + Initial Offer); offline originals to NA", "Bidder", "Annexure III cl. 3A", "Bid due date"),
            ("Technical evaluation; responsiveness; Technically Qualified Bidders declared", "NA", "Tender Document", "2-3 weeks"),
            ("Open Initial Offers; rank; eliminate (4-6 TQBs: lowest out; ≥7: lowest 1/3, max 3)", "NA", "Tender Document", "1 week"),
            ("Ascending forward e-auction; highest Final Offer = Preferred Bidder", "MSTC / NA", "Tender Document", "1 day"),
            ("NA recommends; Central Govt declares Successful Bidder; bid securities of others returned", "MoC / NA", "CM(SP) Rules", "2-4 weeks"),
            ("Execute CMDPA (Coal Mine Development and Production Agreement)", "NA + SB", "CM(SP) Act s.8", "1-2 weeks"),
            ("Pay 1st upfront instalment (25%) within 40 business days of CMDPA", "SB", "CMDPA cl. 5.2.1", "≤40 business days"),
            ("Furnish performance security: 65% of (1-yr royalty + 1-yr revenue share) at PRC", "SB", "CMDPA cl. 6.1.2", "With completion notice"),
            ("Pay Fixed Amount (mine dossier, prior-allottee land, GR and clearance costs)", "SB", "CMDPA cl. 3.1(d)", "With completion notice"),
            ("Submit Schedule B intimation and Schedule C completion notice with evidence", "SB", "CMDPA cl. 3.2.1", "1 week"),
            ("Vesting / allotment order issued: efficiency-parameter clock (51 months) starts", "NA", "CM(SP) s.8", "2-6 weeks"),
            ("Apply for transfer of prior allottee's mining plan, ToR/EC, FC proposal, CBA notifications", "SB", "EIA Notif. para 11; VSSR 2023", "1-5 months"),
        ],
        "tips": [
            "Budget the full cash call before bidding: 1st upfront + PBG + fixed amount fall due within ~2 months of CMDPA.",
            "Price the R&R burden and CA-land search into the bid: they, not geology, usually decide the 51-month timeline.",
        ],
    },
    {
        "code": "MOB",
        "title": "Mobilisation, surveys and project set-up",
        "intro": (
            "The first 3-6 months after vesting decide whether every downstream clearance can start on time. The "
            "certified DGPS boundary and a plot-wise land schedule (khata, plot, kisam, area, owner) certified by the "
            "Revenue Inspector and Tehsildar are inputs to the mining plan, the FC proposal (KML on PARIVESH), the CBA "
            "notifications and the SES. Consultants are best tendered in parallel immediately after CMDPA signing."
        ),
        "flow": [
            dict(t="Steering committee, PMC, Odisha regional office", who="GMDC", d="2-4 wks"),
            dict(t="SWCS, PARIVESH, OCMMS, NOCAP, MSTC user registrations", who="GMDC", d="2-4 wks"),
            dict(t="Tender & onboard MPPA, EIA/FC, LA-R&R, DGPS, rail-DPR agencies", who="GMDC", d="2-5 months", crit=True),
            dict(t="Collect GR (soft & hard copy) and borehole data", who="CMPDI", d="2-6 wks"),
            dict(t="DGPS boundary survey; CMPDI/ORSAC certificate; KML", who="CMPDI / ORSAC", d="1-4 months", crit=True),
            dict(t="Cadastral maps, RoR, digitisation & superimposition", who="Tehsil / ORSAC", d="1-3 months", crit=True),
            dict(t="Plot-wise land schedule certified by RI & Tehsildar", who="Revenue Dept", d="1-3 months", crit=True),
            dict(t="Stakeholder map, village engagement & CSR baseline", who="GMDC / PMC", d="1-2 months"),
        ],
        "table": [
            ("Constitute project steering committee; nominate project head and authorised signatories", "GMDC", "Board resolution", "1-2 weeks"),
            ("Appoint PMC; set up MIS, master tracker, risk register, monthly NA review pack", "GMDC / PMC", "-", "2-4 weeks"),
            ("Nominate authorised personnel; register on SWCS; obtain login credentials", "GMDC / MoC", "SWCS", "2-4 weeks"),
            ("Register as user agency on PARIVESH 2.0; OSPCB OCMMS; CGWA NOCAP; Odisha GO-SWIFT", "GMDC", "Portals", "1-2 weeks"),
            ("Approve organogram; hire GM (Project), DGM (Coal), land/R&R, environment & forest officers", "GMDC HR", "-", "3-6 months"),
            ("Office space and guest house at Bhubaneswar and site; vehicles; IT connectivity", "GMDC Admin", "-", "1-3 months"),
            ("Tender: Mining Plan agency (accredited MPPA / Qualified Person)", "GMDC", "MCR 2016 r.22B", "6-10 weeks"),
            ("Tender: EC + FC consultant (NABET/QCI accredited for coal mining, Category A)", "GMDC", "EIA Notif. 2006", "6-10 weeks"),
            ("Tender: LA & R&R agency (SES, genealogy, YADAST, case files, valuation)", "GMDC", "-", "6-10 weeks"),
            ("Tender: rail siding / road feasibility and DPR (e.g., IPRCL); transaction advisor for MDO", "GMDC", "GCT Policy", "6-10 weeks"),
            ("Obtain approved GR soft copy and hard copy, borehole logs, seam data from CMPDI", "CMPDI", "Tender Document", "2-6 weeks"),
            ("DGPS survey of block boundary; boundary pillars; certification by CMPDI; KML file", "CMPDI / ORSAC", "MP Guidelines 2025", "1-4 months"),
            ("Collect cadastral (village) maps, Record of Rights, settlement records", "Tehsil office", "OLR Act", "1-2 months"),
            ("Digitise maps; superimpose ML boundary on cadastral, forest (FMIS) and satellite layers", "ORSAC / consultant", "-", "1-2 months"),
            ("Prepare plot-wise land schedule: tenancy / Govt non-forest / forest; certify by RI & Tehsildar", "Revenue Dept", "-", "1-3 months"),
            ("Identify grazing (gochar), homestead, religious and community land needing replacement", "Tehsildar / GMDC", "OGLS Act", "1 month"),
            ("Stakeholder mapping; village meetings; CSR needs assessment and baseline", "GMDC / PMC", "Companies Act s.135", "1-2 months"),
            ("Logistics pre-feasibility (rail/road/port) and customer discovery", "GMDC Marketing", "-", "2-3 months"),
        ],
        "tips": [
            "Get the land schedule right first time - GMDC's Burapahar block had to revise its certified schedule after an ML-boundary change, holding up s.9(1).",
            "Insist that every consultant contract has milestone-linked payments and liquidated damages tied to CMDPA dates.",
        ],
    },
    {
        "code": "MPL",
        "title": "Mining Plan and Mine Closure Plan (MS-2)",
        "intro": (
            "Under the Mining Plan Guidelines for Coal and Lignite Blocks 2025 (MoC, Jan-2025) the plan is "
            "prepared by a Qualified Person / accredited MPPA, approved by the company Board, peer reviewed and filed on "
            "SWCS with the fee. The Technical Committee must raise observations within 15 days (only twice); the "
            "proponent replies within 15 days (max 30); the approving authority disposes within 30 days of "
            "(re)submission; CCO conveys in-principle approval within 5 working days and final approval within 3 days of "
            "payments being confirmed by the NA. MS-2 is due 6 months from vesting. For Baitarani West the OMC plan "
            "approved on 10-Nov-2021 was deemed transferred with the vesting order."
        ),
        "flow": [
            dict(t="Freeze design basis: geology, method, PRC, dumps, CHP, infra", who="GMDC + MPPA", d="2-4 wks"),
            dict(t="Draft Mining Plan + progressive & final Mine Closure Plan", who="MPPA / QP", d="6-10 wks", crit=False),
            dict(t="Expert peer review; incorporate comments; Board approval", who="GMDC", d="2-4 wks"),
            dict(t="Upload on SWCS (temporary QP login) with fee", who="QP / GMDC", d="1 wk"),
            dict(t="Technical Committee observations", who="CCO / MoC", d="≤15 days"),
            dict(t="Compliance & re-submission (max 2 rounds)", who="MPPA", d="15-30 days"),
            dict(t="Presentation; recommendation; approval", who="MoC", d="≤30 days"),
            dict(t="In-principle approval; payments; final approval", who="CCO / NA", d="5 + 3 days", ms="MS-2"),
        ],
        "table": [
            ("Finalise project assumptions (geology, mine design, method, PRC, mine life) - management sign-off", "GMDC + MPPA", "-", "2-4 weeks"),
            ("Mine design: pit limits, stripping ratio, calendar plan, dump design, CHP, drainage, infrastructure", "MPPA", "MP Guidelines 2025", "4-8 weeks"),
            ("Mine Closure Plan (progressive + final) with cost, ecological restoration and post-mining land use", "MPPA", "MCP Guidelines", "2-4 weeks"),
            ("Attach CMPDI DGPS certificate, KML and approved GR; QP certifies plan within block boundary", "QP", "MP Guidelines 2025", "-"),
            ("Submit draft to GMDC; expert reviewer comments; pre-check; re-share; go-ahead", "MPPA / Expert", "Tracker MP4-MP9", "3-6 weeks"),
            ("Company Board approval of the Mining Plan", "GMDC Board", "MP Guidelines 2025", "1-2 weeks"),
            ("Upload through temporary login on SWCS; pay non-refundable fee; submit", "QP / GMDC", "SWCS", "1 week"),
            ("Technical Committee scrutiny; observations uploaded (twice only)", "CCO / Tech. Committee", "MP Guidelines 2025", "≤15 days"),
            ("Address observations; re-submit modified plan", "MPPA / GMDC", "MP Guidelines 2025", "15 days (max 30)"),
            ("Presentation before committee; recommendation for approval", "GMDC / MoC", "-", "1-2 weeks"),
            ("Approving authority disposes the application", "MoC", "MP Guidelines 2025", "≤30 days"),
            ("CCO conveys in-principle approval to proponent and NA", "CCO", "MP Guidelines 2025", "≤5 working days"),
            ("Revise performance security if PRC changed; pay dues; NA confirmation", "GMDC / NA", "CMDPA cl. 6.1.4(c)", "≤30 days"),
            ("CCO conveys final approval (MS-2 achieved)", "CCO", "CMDPA Sch. D", "≤3 days"),
            ("Later revisions: minor changes (e.g., ≤50% capacity increase, HEMM change) by Board; others to Coal Controller", "GMDC", "MP Guidelines 2025 para 2.9", "As needed"),
        ],
        "tips": [
            "A plan that front-loads production pays: coal produced before the Scheduled Date of Production gets a 50% rebate on the revenue share.",
            "Keep the box-cut in a no-habitation patch (Govt/acquired land) so mine opening is not hostage to R&R shifting.",
        ],
    },
    {
        "code": "ENV",
        "title": "Environment Clearance (MS-3)",
        "intro": (
            "A coal mine is Category A (item 1(a)) under the EIA Notification 2006 and is appraised by the Expert "
            "Appraisal Committee (Coal Mining) of MoEFCC on PARIVESH. ToR is due within 60 days of Form-1/CAF (standard "
            "ToR may issue faster); baseline covers one season; the public hearing must be completed within 45 days of "
            "the request; EC is to be decided within 105 days of the final EIA. MS-3 (EC) is due 18 months after MS-2. "
            "Baitarani West: ToR transferred 06-Nov-23, PH 24-Sep-24, EAC returned the proposal on 03-Apr-25, "
            "elephant-corridor NOC 25-Aug-25, fresh EC application 30-Sep-25, EC granted 03-Dec-25."
        ),
        "flow": [
            dict(t="Form-1/CAF + PFR; ToR application", who="EIA consultant", d="3-6 wks"),
            dict(t="EAC appraisal; ToR granted", who="MoEFCC", d="≤60 days"),
            dict(t="Baseline monitoring (one season)", who="NABL lab", d="3-4 months"),
            dict(t="Specialised studies: GW model, HEC, traffic, R&R", who="Consultants", d="2-5 months"),
            dict(t="Draft EIA/EMP + Odia summary to OSPCB", who="Consultant", d="4-6 wks"),
            dict(t="PH notice (30 days) and public hearing", who="Collector / OSPCB", d="≤45 days"),
            dict(t="Final EIA/EMP; EC application on PARIVESH", who="Consultant", d="4-6 wks"),
            dict(t="EDS/ADS replies; EAC presentation", who="GMDC", d="1-3 months"),
            dict(t="EAC recommendation; EC letter", who="MoEFCC", d="≤105 days", ms="MS-3"),
        ],
        "table": [
            ("Prepare Pre-Feasibility Report and Form-1 / Common Application Form; KML; approved mine plan", "EIA consultant", "EIA Notif. App. I", "3-6 weeks"),
            ("Online ToR application on PARIVESH (or ToR transfer in Form-8 for a prior allottee's ToR)", "GMDC", "EIA Notif. para 11", "1 week"),
            ("ToR presentation before EAC (Coal Mining); standard/specific ToR granted", "MoEFCC / EAC", "EIA Notif. para 7(ii)", "≤60 days"),
            ("Accept ToR or seek amendment (e.g., after mining plan revision)", "GMDC", "-", "2-4 weeks"),
            ("Baseline data: AAQ, water, noise, soil, ecology & biodiversity, traffic, socio-economics (one season)", "NABL lab / consultant", "Std. ToR", "3-4 months"),
            ("Hydrogeological investigation and groundwater modelling; mine dewatering estimate", "Consultant", "ToR / CGWA", "2-4 months"),
            ("Human-elephant conflict & wildlife study; site-specific wildlife conservation plan input", "Consultant / WII-type agency", "ToR", "2-4 months"),
            ("Traffic study, subsidence/slope stability, cumulative impact (Talcher coalfield), R&R plan", "Consultants", "ToR", "2-3 months"),
            ("Prepare draft EIA/EMP and executive summary in English and Odia", "Consultant", "EIA Notif. App. III", "4-6 weeks"),
            ("Submit to Member Secretary, OSPCB requesting public hearing; fee", "GMDC", "EIA App. IV", "1 week"),
            ("Publish PH notice in two newspapers (one Odia) - at least 30 days before hearing", "OSPCB", "EIA App. IV para 3", "30 days"),
            ("Conduct public hearing (DM/ADM presides; video-recorded); proceedings in 8 days", "Collector / OSPCB", "EIA App. IV", "≤45 days"),
            ("OSPCB forwards PH proceedings to MoEFCC and Regional Office", "OSPCB", "EIA App. IV", "1-2 weeks"),
            ("Incorporate PH issues & action plan with budget into final EIA/EMP", "Consultant", "-", "3-6 weeks"),
            ("Submit final EIA/EMP and EC application; respond to EDS/ADS", "GMDC", "EIA Notif. para 7(iv)", "2-8 weeks"),
            ("Final technical presentation before EAC; EAC recommendation (or return / deferral)", "EAC", "EIA Notif. para 7(iv)", "≤60 days"),
            ("MoEFCC decision and EC letter with specific conditions", "MoEFCC", "EIA Notif. para 8", "≤45 days after EAC"),
            ("Upload six-monthly compliance reports; display EC; publish in newspapers", "GMDC", "EC conditions", "Ongoing"),
        ],
        "tips": [
            "BW lesson: EAC returned the first proposal (Apr-25); build the elephant-corridor study, R&R plan and FC status into the EIA from day one.",
            "Run baseline in the first non-monsoon season after vesting; a missed season costs ~6 months.",
        ],
    },
    {
        "code": "FOR",
        "title": "Forest clearance, FRA, CA land, tree enumeration and wildlife plan",
        "intro": (
            "Diversion of forest land (BW: 64.37 ha = 4.47 ha reserved + 59.90 ha revenue forest) needs prior approval "
            "under the Van (Sanrakshan Evam Samvardhan) Adhiniyam, 1980 and Rules 2023 (VSSR), processed on PARIVESH 2.0. "
            "VSSR prescribes working-day limits at every desk (DCF/Collector 20, site inspections 20, Nodal/PCCF 15, PSC "
            "30, State 15, MoEFCC scrutiny/IRO/Advisory Committee 4+5+20+20, approval 10). Stage-I (in-principle) is "
            "followed by payment of compensatory levies (NPV, CA, SMC, wildlife plan), compliance of conditions and "
            "settlement of rights under FRA 2006 before Stage-II and the State's diversion order. Four sub-processes "
            "run in parallel: FRA, CA land, tree enumeration and the site-specific wildlife conservation plan."
        ),
        "flow": [
            dict(t="Tree enumeration with FMIS grid/stock maps", who="DFO / committees", d="2-6 months"),
            dict(t="CA land: identify, NOC, DGPS, suitability, CA scheme", who="Collector / DFO", d="3-10 months", crit=False),
            dict(t="FRA: Gram Sabha resolutions; SDLC, DLC; certificate", who="Collector / Gram Sabha", d="3-12 months"),
            dict(t="Form-A on PARIVESH 2.0 with KML, NOCs, SSWLCP", who="User agency", d="1-3 months"),
            dict(t="DFO/DC, CF, Nodal/PCCF, PSC, State Govt", who="State Forest Dept", d="~100 working days"),
            dict(t="IRO site inspection; Advisory Committee (FAC)", who="MoEFCC", d="2-4 months"),
            dict(t="Stage-I (in-principle) approval", who="MoEFCC", d="10 working days", ms="FC-I"),
            dict(t="Demand notes; pay NPV, CA, SMC, WLMP; CA mutation & PF notification", who="DFO / Revenue", d="2-8 months"),
            dict(t="Compliance file DFO > RCCF > PCCF > MoEFCC", who="Forest Dept", d="3-12 months"),
            dict(t="Stage-II approval; State diversion order", who="MoEFCC / State", d="1-5 months", ms="FC-II"),
            dict(t="Tree felling (OFDC); possession of forest land", who="DFO / OFDC", d="1-4 months"),
        ],
        "table": [
            ("Letter from DFO to FMIS for grid and stock maps; demand note; pay fees; maps issued", "DFO / FMIS", "Tracker TE1-TE4", "3-6 weeks"),
            ("Form tree-enumeration committees (RO); enumerate; report to DFO; DFO approval", "Range Officer / DFO", "Tracker TE5-TE10", "1-4 months"),
            ("Identify CA land: equivalent non-forest Govt land (or 2x degraded forest where permitted)", "Collector / GMDC", "VSSR 2023 r.11", "1-4 months"),
            ("Collector NOC for CA land; Gram Sabha in CA villages; DGPS of CA land; DSS check", "Collector / DFO", "Tracker CA1-CA6", "1-3 months"),
            ("Suitability certificate from DFO/CCF; prepare and get CA scheme technically vetted", "DFO / CF", "Tracker CA7-CA9", "1-2 months"),
            ("Transfer & mutation of CA land to Forest Dept; notify as PF/RF", "Tehsildar / Collector", "Tracker CA10-CA13", "3-6 months"),
            ("FRA: application to Collector; SDM starts process; Gram Sabha resolutions (quorum, minutes, video)", "Collector / Gram Sabha", "FRA 2006 s.6; Rules r.4", "1-3 months"),
            ("FRC claims verification; SDLC and DLC recommendations; FRA certificate by Collector", "SDLC / DLC", "FRA Rules r.12", "2-6 months"),
            ("Prepare site-specific wildlife conservation plan (elephant corridor measures); CWLW approval", "Consultant / CWLW", "WPA 1972", "3-6 months"),
            ("Obtain NOCs: Gram Panchayat, Archaeology, Collector; details of land and R&R", "GMDC", "VSSR checklist", "1-3 months"),
            ("File Form-A (Part I) on PARIVESH 2.0 with KML, maps, mine plan, CA details", "User agency", "VSSR 2023 r.9", "2-4 weeks"),
            ("Nodal Officer completeness check; EDS loop", "State Nodal Officer", "VSSR timelines", "≤10 working days"),
            ("DFO/DC processing; site inspection by DCF/CF; CF recommendation", "DFO / CF", "VSSR Schedule", "40 working days"),
            ("Nodal Officer/PCCF processing; Project Screening Committee; State Govt recommendation", "PCCF / PSC / State", "VSSR Schedule", "60 working days"),
            ("MoEFCC scrutiny; IRO site inspection & report; Advisory Committee (FAC)", "MoEFCC / IRO / FAC", "VSSR Schedule", "~50 working days"),
            ("Stage-I (in-principle) approval with conditions", "MoEFCC", "Adhiniyam s.2", "10 working days"),
            ("DFO raises demand: NPV, CA cost, SMC plan, wildlife plan, additional CA norms; pay on e-portal", "DFO / GMDC", "VSSR 2023", "1-3 months"),
            ("Prepare & get approved SMC plan, avifauna & other schemes (BW: 11 of 12 approved 10-Apr-26)", "DFO / RCCF", "FC-I conditions", "2-6 months"),
            ("Compliance report: DFO > RCCF > PCCF (Nodal) > Secretary (Forest) > MoEFCC", "Forest Dept", "VSSR 2023", "2-6 months"),
            ("Stage-II (final) approval; State Govt order for diversion / lease", "MoEFCC / State", "VSSR 2023 r.9-10", "1-3 months"),
            ("Tree-felling application; marking; APCCF approval; demand for felling cost; payment", "DFO / APCCF", "Tracker TFPP1-TFPP12", "1-3 months"),
            ("Felling, debarking, logging, transport by OFDC; possession of felled area with coordinates", "OFDC / DFO", "Tracker TFPP13-TFPP19", "1-4 months"),
        ],
        "tips": [
            "CA land is the classic long pole: BW's CA land is in Koraput district (Baipariguda), 300+ km from the mine; start the search at the bid stage.",
            "FRA certificate is a hard prerequisite for the State diversion order - BW's is still pending (Oct-26).",
        ],
    },
    {
        "code": "LAR",
        "title": "Land acquisition under the CBA Act, 1957 and R&R (MS-4)",
        "intro": (
            "For a Government company, land is acquired by the Central Government under the Coal Bearing Areas "
            "(Acquisition & Development) Act, 1957 and vested in the company by a s.11(1) order; that order substitutes "
            "for a mining lease for CMDPA purposes (2nd upfront instalment is due within 15 business days). Under "
            "the RFCTLARR (Removal of Difficulties) Order 2015 (S.O. 2368(E), 28-Aug-2015) the <b>First, Second and Third "
            "Schedules of RFCTLARR 2013</b> (compensation, R&R, infrastructure amenities) apply to CBA acquisitions; "
            "Odisha's R&R Policy 2006 (RPDAC) and ORFCTLARR Rules 2016 govern implementation. Statutory clocks: s.7(1) "
            "within 2 years of s.4(1) (+1 year); objections within 30 days of s.7; s.9(1) declaration within 3 years "
            "of s.7(1). MS-4 (possession and R&R for rated capacity) is due 21 months after MS-3."
        ),
        "flow": [
            dict(t="Land schedule & proposal to MoC (CBA cell)", who="GMDC / Collector", d="1-4 months"),
            dict(t="s.4(1): intention to prospect (Gazette)", who="MoC", d="1-6 months", crit=True),
            dict(t="s.7(1): notice of intention to acquire", who="MoC", d="2-8 months", crit=True),
            dict(t="s.8: objections (30 days); hearing & report", who="Competent Authority", d="1-4 months"),
            dict(t="s.9(1) declaration; s.10 vesting in Centre", who="MoC", d="2-8 months"),
            dict(t="s.11(1) order: vesting in GMDC; 2nd upfront", who="MoC", d="0.5-3 months"),
            dict(t="SES, genealogy, YADAST; PAF/PDF lists", who="R&R agency / Collector", d="6-16 months", crit=True),
            dict(t="Valuation & compensation award (First Schedule)", who="Competent Authority", d="2-8 months"),
            dict(t="R&R plan, colony & gochar land; RPDAC approval", who="Collector / RPDAC", d="4-15 months", crit=True),
            dict(t="Case files; deposit & disbursement", who="Collector / GMDC", d="4-14 months"),
            dict(t="R&R colony & shifting of displaced families", who="GMDC / Collector", d="8-20 months", crit=True),
            dict(t="Physical possession (s.12) for rated capacity", who="Competent Authority", d="1-4 months", ms="MS-4", crit=True),
        ],
        "table": [
            ("Prepare land documents for CBA: schedule, maps, khatian, RoR, area statement", "GMDC / LA agency", "CBA s.4(2)", "1-2 months"),
            ("Proposal for s.4(1) to MoC through Coal Controller / CBA cell; vetting; Gazette notification", "MoC", "CBA s.4(1)", "1-6 months"),
            ("Survey, bore, mark boundaries under s.4(3); pay/tender damages under s.6", "Competent Authority", "CBA s.4(3), s.6", "During validity"),
            ("Notice of intention to acquire land/rights - within 2 years of s.4(1) (+1 year max)", "MoC", "CBA s.7(1)-(2)", "2-8 months"),
            ("Receive objections within 30 days; hearing in person/by counsel; report to Central Govt", "Competent Authority (Collector/ADM)", "CBA s.8", "1-4 months"),
            ("Declaration of acquisition (parcel-wise allowed) - within 3 years of s.7(1); copy to State", "MoC", "CBA s.9(1)-(2)", "2-8 months"),
            ("Urgency route if justified: s.8 dispensed, declaration any time after s.7", "MoC", "CBA s.9A", "Optional"),
            ("Vesting in Central Govt free of encumbrances on publication", "MoC", "CBA s.10", "Automatic"),
            ("Order directing vesting in GMDC (Govt company) on terms; pay 2nd upfront within 15 business days", "MoC / GMDC", "CBA s.11(1); CMDPA 5.2.1", "0.5-3 months"),
            ("Socio-economic survey (SES) of all affected families; cut-off date; PAF/PDF lists", "R&R agency / Collector", "RFCTLARR Sch. II; ORRP 2006", "4-10 months"),
            ("Genealogy (family tree) and YADAST (enumeration of houses, structures, trees, wells)", "R&R agency / RI", "ORFCTLARR Rules 2016", "4-10 months"),
            ("Valuation: market value x multiplier (rural factor), 100% solatium, assets; 12% additional amount", "Competent Authority", "RFCTLARR Sch. I", "2-6 months"),
            ("Compensation determined; disputes to Tribunal; appeal to High Court in 30 days", "CA / Tribunal", "CBA s.13, 14, 20", "2-8 months"),
            ("Draft R&R plan: homestead, house, subsistence, employment/annuity, shifting, cattle shed, artisans", "GMDC / Collector", "RFCTLARR Sch. II; ORRP 2006", "2-4 months"),
            ("Identify R&R colony land and replacement gochar land; Third-Schedule amenities", "Collector / GMDC", "RFCTLARR Sch. III", "2-6 months"),
            ("RPDAC meeting (Collector chairs; MLA, MP, PRI, PAF reps); R&R plan approval; Govt notification", "Collector / RDC", "ORRP 2006 para 6", "2-8 months"),
            ("Prepare & validate case files (title, mutation, bank details); deposit with Competent Authority", "LA agency / Collector", "CBA s.17", "2-6 months"),
            ("Disbursement camps; tender/deposit compensation; deposit with Tribunal if disputed", "Collector", "CBA s.17", "3-9 months"),
            ("Government land: alienation/premium or transfer for land in ML area; possession letter", "Revenue & DM Dept", "OGLS Act / CBA s.9 proviso", "3-12 months"),
            ("R&R colony development: plots, roads, water, power, school, health post, community hall", "GMDC / contractor", "RFCTLARR Sch. III", "8-18 months"),
            ("Shifting of displaced families (phase-wise, initial mining area first); shifting allowance", "GMDC / Collector", "ORRP 2006", "2-6 months"),
            ("Notice to surrender possession; take possession; demarcate and fence", "Competent Authority", "CBA s.12", "1-3 months"),
            ("Constitute project-level R&R monitoring; grievance redressal; periphery development", "Collector / GMDC", "ORRP 2006", "Ongoing"),
        ],
        "tips": [
            "SES must capture actual families, not only recorded tenants - BW's SES (3,402 original families, Jan-25) created an issue at RPDAC.",
            "Monthly rate revisions force re-work of case files; batch disbursement by village and lock rates via the award date.",
        ],
    },
    {
        "code": "OPN",
        "title": "Other statutory consents, permissions and registrations",
        "intro": (
            "CMDPA Schedule D lists many 'non-monitored' activities that are nevertheless pre-conditions for opening: "
            "nala/river diversion, diversion of power lines/roads, permission to draw water and power, CTE/CTO, DGMS "
            "intimation, explosives and petroleum licences, Factories Act permission, radio-frequency licence, labour "
            "permissions and the escrow account. Each has its own portal and clock; most can and should run in parallel "
            "with EC/FC so that only FC Stage-II remains when the CTO is due."
        ),
        "flow": [
            dict(t="CGWA NOC (NOCAP) for dewatering / abstraction", who="CGWA", d="2-6 months"),
            dict(t="Water allocation & nala diversion NOC", who="WRD Odisha", d="3-12 months"),
            dict(t="Consent to Establish (OCMMS)", who="OSPCB", d="2-5 months"),
            dict(t="Power: load sanction, line & substation", who="TPCODL / OPTCL", d="4-10 months"),
            dict(t="Explosives (LE-3) & petroleum storage licences", who="PESO / DM", d="2-5 months"),
            dict(t="Labour: CLRA registration/licences, CMPF, BOCW", who="RLC (C) / CMPFO", d="1-2 months"),
            dict(t="Escrow account for mine closure (CCO beneficiary)", who="GMDC / CCO", d="2-6 wks"),
            dict(t="Consent to Operate (after FC-II)", who="OSPCB", d="1.5-4 months", crit=True),
        ],
        "table": [
            ("CGWA NOC for mine dewatering & GW abstraction on NOCAP (impact assessment, piezometers, recharge plan)", "CGWA", "CGWA Guidelines 2020", "2-6 months"),
            ("Surface-water allocation for dust suppression/CHP/colony; agreement with WRD", "WRD Odisha", "Odisha Irrigation Act", "3-9 months"),
            ("Nala/stream diversion: DPR, joint field survey (WRD, Minor Irrigation), NOC (BW: due 30-Oct-26)", "WRD / Chief Engineer", "CMDPA Sch. D", "4-12 months"),
            ("Diversion of power line / road / canal within lease, if any", "OPTCL / R&B / WRD", "CMDPA Sch. D", "3-9 months"),
            ("CTE: online application; hard copy to Member Secretary; RO inspection; technical committee; grant", "OSPCB", "Water Act s.25; Air Act s.21", "2-5 months"),
            ("Hazardous waste authorisation (used oil, batteries); e-waste registration", "OSPCB", "HOWM Rules 2016", "1-2 months"),
            ("Power: application, feasibility, estimate, deposit; 33 kV line / substation construction", "TPCODL / OPTCL", "Electricity Act 2003", "4-10 months"),
            ("Explosives: magazine site approval, DM NOC, licence in Form LE-3; shot-firer/blaster competency", "PESO / DM", "Explosives Rules 2008", "2-5 months"),
            ("Petroleum (HSD) storage licence for mine fuel station", "PESO", "Petroleum Rules 2002", "2-4 months"),
            ("Factories Act licence for CHP / workshop where applicable", "Director of Factories", "Factories Act 1948", "1-2 months"),
            ("WPC licence for radio-frequency communication (VHF/UHF sets)", "DoT / WPC", "Indian Telegraph Act", "1-3 months"),
            ("Principal employer registration (CLRA) and contractor licences - Central sphere", "RLC (Central)", "CLRA 1970", "1 month"),
            ("CMPF registration of mine & employees; BOCW registration for construction", "CMPFO / Labour Dept", "CMPF Act 1948", "1 month"),
            ("Fire NOC, building plan approvals (site office, colony), legal-metrology stamping of weighbridges", "Local bodies / LM Dept", "Various", "1-3 months"),
            ("Escrow account (FD with CCO as exclusive beneficiary) at Rs 14 lakh/ha OC base rate (May-24, WPI-escalated)", "GMDC / CCO", "MP Guidelines 2025", "2-6 weeks"),
            ("CTO: application with EC, FC-II, CTE compliance; queries; inspection; grant (BW applied 08-Jul-26)", "OSPCB", "Water & Air Acts", "1.5-4 months"),
        ],
        "tips": [
            "Apply for CTO as soon as CTE conditions are met; keep only FC-II outstanding (BW followed this approach).",
            "Nala diversion often needs Gram Sabha and WRD field verification - BW's DPR (Mar-26) is still awaiting NOC.",
        ],
    },
    {
        "code": "OPN",
        "title": "Mine developer (MDO), infrastructure and evacuation",
        "intro": (
            "GMDC operates through a turnkey contractor/MDO for coal and OB. Rail is the binding long-term constraint: "
            "the EC requires 12 of 15 MTPA to move by in-pit conveyor, silo and a private siding connected through the "
            "common rail corridor to ECoR at Jarpara, and the siding must be ready before output reaches 6 MTPA. Under "
            "the Gati Shakti Cargo Terminal (GCT) Master Circular 2026: joint survey within 15 days, in-principle "
            "approval within 20 days, ESP approval in 4+2+2 weeks, signalling plan in 4 weeks, construction to start "
            "within 6 months and finish within 24 months. Early coal moves by covered trucks on the strengthened "
            "Chhendipada-Jharpada road (~25 km)."
        ),
        "flow": [
            dict(t="Transaction advisor; RFP & contract model", who="GMDC", d="1-3 months"),
            dict(t="NIT, pre-bid, corrigenda, bid submission", who="GMDC", d="2-4 months"),
            dict(t="Technical & financial evaluation; award; LoA", who="GMDC", d="2-4 months"),
            dict(t="PBG, contract signing, site handover", who="GMDC / MDO", d="1-3 months"),
            dict(t="Mobilisation: HEMM, workshop, magazine, camp", who="MDO", d="2-5 months"),
            dict(t="Approach road; weighbridge; coal yard", who="GMDC / MDO", d="4-10 months"),
            dict(t="GCT application; IPA; DPR / ESP / SIP approvals", who="ECoR", d="5-15 months"),
            dict(t="Siding, conveyor, silo construction; CRS; commissioning", who="GMDC / EPC", d="14-30 months"),
        ],
        "table": [
            ("Appoint transaction advisor; choose model (MDO vs turnkey coal + OB contract); approvals", "GMDC", "Tracker 'Tender-MDO'", "1-3 months"),
            ("Prepare RFP: scope, HEMM, rates, minimum guarantee, LDs, safety, PBG", "GMDC / TA", "GFR / GMDC manual", "1-2 months"),
            ("Upload NIT; pre-bid meeting (BW: 17-Feb-25, 14 bidders); corrigenda", "GMDC", "-", "1-2 months"),
            ("Bid submission; technical evaluation; financial opening / reverse auction", "GMDC", "-", "1-3 months"),
            ("Competent-authority approval; LoA; PBG (BW: LoI 13-Nov-25, PBG 30-Nov-25)", "GMDC / MDO", "-", "1-2 months"),
            ("Sign contract; hand over site (BW: handover 10-Aug-26; contract 17-Sep-26)", "GMDC / MDO", "-", "1-3 months"),
            ("Mobilise HEMM (surface miners, shovels, dumpers), workshop, fuel station, camp, magazine", "MDO", "CMR 2017", "2-5 months"),
            ("Strengthen Chhendipada-Jharpada road (24.985 km incl. 3 bypasses); approach to ML boundary", "GMDC / R&B", "EC condition", "6-15 months"),
            ("Interim dispatch: weighbridges, CCTV, RFID, coal yard, covered trucks", "GMDC / MDO", "EC; Legal Metrology", "3-6 months"),
            ("GCT application with fee (Rs 20,000 + GST); joint location survey; feasibility; IPA (BW IPA: 18-Jan-25)", "Division (DRM)", "GCT Circular 2026", "~35 days"),
            ("DPR/ESP submission within 4 weeks of IPA; Division 2 weeks; HQ (CE/P&D) 2 weeks (BW: DPR 17-Jun-25)", "ECoR", "GCT Circular 2026", "2-12 months"),
            ("Signalling interlocking plan; land for siding & coal stock at Jharpada", "ECoR / GMDC", "GCT Circular 2026", "1-6 months"),
            ("Construct siding, in-pit conveyor, silo; CRS inspection; agreement (35 yrs); commercial notification", "GMDC / EPC / ECoR", "GCT Circular 2026", "14-30 months"),
        ],
        "tips": [
            "Rail is not on the path to first coal but becomes critical for ramp-up: plan its latest start from the 6 MTPA year.",
            "Lock the MDO's mobilisation to the forecast FC-II date to avoid idle-HEMM claims.",
        ],
    },
    {
        "code": "OPN",
        "title": "Mine opening, first coal and production compliance (MS-5)",
        "intro": (
            "The Colliery Control (Amendment) Rules, 2025 (notified 23-Dec-2025) removed the Coal Controller's prior "
            "mine-opening permission: the Board of a company now approves opening of a mine/seam once all Central, "
            "State and statutory approvals are in hand, and intimates CCO (a further 2026 amendment specifies "
            "intimation within 15 days of opening). The 3rd upfront instalment is due within 15 business days of the "
            "opening permission and the performance security moves to the State Government. The notice of opening "
            "(Form I-A) must reach DGMS, the Coal Controller and the District Magistrate at least one month before "
            "operations begin (Mines Act s.16; CMR 2017 reg. 3)."
        ),
        "flow": [
            dict(t="Approvals readiness checklist (EC, FC-II, CTO, possession, NOCs)", who="PMC", d="Month -6 to 0"),
            dict(t="DGMS: Form I-A notice (≥30 days); owner/agent/manager", who="GMDC / DGMS", d="30 days"),
            dict(t="Safety Management Plan; VT centre; rescue; first aid", who="GMDC / MDO", d="1-2 months"),
            dict(t="Board approval of mine opening; intimation to CCO", who="GMDC Board", d="1-2 wks", ms="MS-5", crit=True),
            dict(t="3rd upfront instalment; PBG to State Govt", who="GMDC", d="≤15 business days"),
            dict(t="Intimate start date to DGMS & Collector; box cut", who="GMDC / MDO", d="Day 0", crit=True),
            dict(t="Royalty, DMF, NMET, i3MS e-permit, GST, grade declaration", who="GMDC / DoM / CCO", d="1-3 months"),
            dict(t="First coal & dispatch; 4th upfront instalment", who="GMDC", d="≤15 business days", ms="Coal", crit=True),
        ],
        "table": [
            ("Approvals readiness review: EC, FC-II & State order, CTO, possession, CGWA, water, nala, power, licences", "PMC / GMDC", "CCR 2004 r.9 (amended)", "Monthly from M-6"),
            ("Appoint owner/agent/manager (First-Class Manager's certificate) and statutory officials; notices to DGMS", "GMDC / MDO", "Mines Act s.17; CMR 2017", "1 month"),
            ("Notice of opening in Form I-A to DGMS (Chief Inspector), Coal Controller & DM - ≥ 30 days ahead", "GMDC", "Mines Act s.16; CMR 2017 reg. 3", "≥30 days"),
            ("Safety Management Plan, risk assessment, traffic rules for HEMM, blasting SOP, dump-slope study", "GMDC / MDO", "CMR 2017", "1-2 months"),
            ("Vocational training centre, first-aid, rescue-station tie-up, crèche, canteen, rest shelters", "GMDC / MDO", "MVT Rules 1966; Mines Rescue Rules 1985", "1-3 months"),
            ("Board resolution approving opening of mine/seam (Companies Act company)", "GMDC Board", "CCR (Amendment) Rules 2025/2026", "1-2 weeks"),
            ("Intimation of opening to Coal Controller's Organisation (within 15 days)", "GMDC", "CCR (Amendment) Rules 2026", "≤15 days"),
            ("Pay 3rd upfront instalment (25%) to State Govt; submit performance security to State; NA returns its PBG", "GMDC", "CMDPA 5.2.1, 6.2", "≤15 business days"),
            ("Revise PBG (first revision on NCI at opening permission)", "GMDC", "CMDPA 6.1.4(a)", "≤30 days"),
            ("Intimate actual date of start to DGMS and Collector; box cut; OB removal", "GMDC / MDO", "Tracker MO7-MO9", "Day 0"),
            ("Register for royalty/DMF/NMET with Deputy Director of Mines (Talcher); i3MS e-transit permits", "GMDC / DoM Odisha", "MMDR s.9, 9B, 9C", "1-2 months"),
            ("Coal grade declaration (third-party sampling) and quality systems", "CCO / GMDC", "Colliery Control Rules", "1-3 months"),
            ("Sales: customer contracts / e-auction, pricing linked to NCI, invoicing, GST", "GMDC Marketing", "-", "1-3 months"),
            ("First coal dispatch; pay 4th upfront instalment within 15 business days", "GMDC", "CMDPA 5.2.1", "≤15 business days"),
            ("Monthly revenue-share payments (Final Offer x quantity x max(notional, actual price)); upfront adjusted up to 50%", "GMDC", "CMDPA cl. 9", "Monthly"),
            ("Monthly efficiency-parameter report to NA; annual production ≥ 65% (3-yr block ≥ 75%) of plan", "GMDC", "CMDPA cl. 10, 16", "Monthly / annual"),
            ("Annual escrow deposit by 30 Sept; six-monthly EC compliance; Form-wise DGMS returns", "GMDC", "MP Guidelines 2025; EC", "Recurring"),
        ],
        "tips": [
            "Mine-opening date drives three cash events (3rd upfront, PBG transfer, PBG revision) - provision them in the treasury plan.",
            "Every tonne before the Scheduled Date of Production (BW: 08-Sep-2029) attracts only half the 33.5% revenue share.",
        ],
    },
]


LEGAL = [
    ("Coal Mines (Special Provisions) Act, 2015 & Rules", "Auction, vesting/allotment orders, Nominated Authority", "MoC (NA)", "Auction & vesting"),
    ("Mines & Minerals (Dev. & Regulation) Act, 1957; MCR 2016/2020", "Auction of coal mines, mining plan, royalty (14% ad valorem), DMF, NMET", "MoC / State", "Throughout"),
    ("Coal Bearing Areas (Acquisition & Development) Act, 1957", "Acquisition of land/rights (s.4, 7, 8, 9, 10, 11, 12, 13, 14)", "MoC / Competent Authority", "Land acquisition"),
    ("RFCTLARR Act 2013 + Removal of Difficulties Order 2015 (S.O. 2368(E))", "Compensation (Sch. I), R&R (Sch. II), amenities (Sch. III) for CBA acquisitions", "MoC / State", "Land & R&R"),
    ("Odisha R&R Policy 2006; ORFCTLARR Rules 2016", "RPDAC, entitlements, procedures in Odisha", "Revenue & DM Dept / Collector", "Land & R&R"),
    ("Environment (Protection) Act, 1986; EIA Notification 2006", "ToR, baseline, public hearing, EC (Category A, item 1(a))", "MoEFCC / EAC", "EC"),
    ("Van (Sanrakshan Evam Samvardhan) Adhiniyam 1980 & Rules 2023", "Forest diversion, CA, NPV, Stage-I/II", "MoEFCC / State Forest Dept", "FC"),
    ("Scheduled Tribes & OTFD (Recognition of Forest Rights) Act, 2006", "Settlement of forest rights; Gram Sabha consent; FRA certificate", "Collector / DLC", "FC"),
    ("PESA Act, 1996", "Gram Sabha consultation in Fifth Schedule areas (verify status of villages)", "Panchayati Raj Dept", "Land / FC"),
    ("Wildlife (Protection) Act, 1972", "Wildlife plan, elephant corridors; NBWL if within 10 km of PA/ESZ", "CWLW / NBWL", "FC / EC"),
    ("Water Act 1974; Air Act 1981; HOWM Rules 2016", "CTE, CTO, hazardous-waste authorisation", "OSPCB", "Consents"),
    ("CGWA Guidelines 2020 (EP Act s.3)", "Groundwater abstraction & dewatering NOC", "CGWA (NOCAP)", "Consents"),
    ("Mines Act 1952; Coal Mines Regulations 2017", "Notice of opening, manager appointment, safety", "DGMS", "Mine opening"),
    ("Colliery Control Rules 2004 (amended 2025 & 2026)", "Mine/seam opening by Board; intimation to CCO; grade declaration", "MoC / CCO", "Mine opening"),
    ("Explosives Act 1884 & Rules 2008; Petroleum Rules 2002", "Magazine and HSD storage licences", "PESO", "Mine opening"),
    ("CLRA 1970; CMPF Act 1948; BOCW Act 1996", "Contract labour, provident fund for coal-mine workers", "RLC (C) / CMPFO", "Mine opening"),
    ("Indian Railways GCT Master Circular 2026", "Private siding / cargo terminal approvals", "ECoR / Railway Board", "Evacuation"),
    ("Companies Act 2013 (s.135)", "Board approvals, CSR", "GMDC Board", "Throughout"),
]


GLOSSARY = [
    ("CBA", "Coal Bearing Areas (Acquisition & Development) Act, 1957"),
    ("CCO", "Coal Controller's Organisation (MoC)"),
    ("CMDPA", "Coal Mine Development & Production Agreement"),
    ("CA / NPV", "Compensatory afforestation / Net Present Value of forest"),
    ("CTE / CTO", "Consent to Establish / Operate (OSPCB)"),
    ("CPM / PERT", "Critical Path Method / Programme Evaluation & Review Technique"),
    ("DLC / SDLC", "District / Sub-Divisional Level Committee (FRA)"),
    ("EAC / FAC", "Expert Appraisal Committee / Forest Advisory Committee"),
    ("EDS / ADS", "Essential / Additional details sought"),
    ("ES, EF, LS, LF", "Earliest/latest start and finish of an activity"),
    ("GCT / ESP / IPA", "Gati Shakti Cargo Terminal / Engineering Scale Plan / In-principle approval"),
    ("IRO", "Integrated Regional Office of MoEFCC"),
    ("MDO / HEMM", "Mine Developer & Operator / Heavy Earth-Moving Machinery"),
    ("MPPA / QP", "Mining Plan Preparing Agency / Qualified Person"),
    ("MS-2 ... MS-5", "CMDPA efficiency-parameter milestones"),
    ("NA", "Nominated Authority, Ministry of Coal"),
    ("NCI", "National Coal Index"),
    ("PAF / PDF", "Project affected / displaced family"),
    ("PBG / PS", "Performance bank guarantee / performance security"),
    ("PRC", "Peak rated capacity"),
    ("RPDAC", "Rehabilitation & Periphery Development Advisory Committee"),
    ("SES", "Socio-economic survey"),
    ("SSWLCP", "Site-specific wildlife conservation plan"),
    ("SWCS", "Single Window Clearance System (MoC)"),
    ("TF / FF", "Total float / free float"),
    ("VSSR", "Van (Sanrakshan Evam Samvardhan) Rules, 2023"),
    ("YADAST", "Odisha enumeration of houses, structures & assets for valuation"),
]


SOURCES_WEB = [
    ("PIB (26-Dec-2025) - Colliery Control (Amendment) Rules, 2025: Board of company to approve mine opening", "pib.gov.in/PressReleasePage.aspx?PRID=2208844"),
    ("Corpseed note - Colliery Control (Amendment) Rules, 2026 (intimation to CCO within 15 days)", "corpseed.com/news/colliery-control-amendment-rules-2026-coal-mine-approval"),
    ("Coal Controller's Organisation - Opening & re-opening of coal mines (documents, SWCS process)", "coalcontroller.gov.in/opening-and-re-opening-coal-mines-and-coal-seams"),
    ("Ministry of Coal - Single Window Clearance System", "coal.nic.in/nominated-authority/single-window-system"),
    ("MoC - Mining Plan Guidelines for Coal & Lignite Mines 2025 (Jan-2025)", "coal.nic.in/sites/default/files/2025-01/31-01-2025a-wn.pdf"),
    ("Van (Sanrakshan Evam Samvardhan) Rules, 2023 - timelines schedule", "thc.nic.in/Central Governmental Rules/Van (Sanrakshan Evam Samvardhan) Rules, 2023.pdf"),
    ("MoC - Minutes of NA review of coal-block operationalisation (Baitarni West, Burapahar et al.)", "coal.gov.in/sites/default/files/2023-06/24-07-2025mom.pdf"),
    ("Madras HC, G. Kesavan v. UoI (2025) - S.O. 2368(E) applies RFCTLARR Schedules to CBA", "casemine.com/judgement/in/67c14327ed57983ce54e4142"),
    ("Railway Board - GCT Master Circular 2026", "indianrailways.gov.in/railwayboard/.../GCT Master Circular 2026.pdf"),
    ("PIB (17-Sep-2026) - 16th round of commercial coal mine auctions; 147 mines auctioned", "pib.gov.in/PressReleaseIframePage.aspx?PRID=2311453"),
    ("GMDC Annual Report 2025-26 (NSE filing) - Baitarni West status", "nsearchives.nseindia.com/annual_reports/AR_31488_GMDCLTD_2025_2026"),
    ("Construction World (12-Dec-2025) - GMDC secures EC and FC Stage-I; mining partner onboarded", "constructionworld.in/.../gmdc-advances-rs-15-mtpa-baitarni-west-mine"),
    ("CGWA - documents required for mining projects", "cgwa.mowr.gov.in/DocRecMining.html"),
    ("Odisha SPCB - consent to operate", "ospcboard.odisha.gov.in/en/divisions/consent-management-division"),
    ("Odisha R&R Policy 2006 (Revenue & DM Dept)", "revenue.odisha.gov.in/sites/default/files/2020-05/18040_14_05_06.pdf"),
]

SOURCES_REPO = [
    "CMDPA for Baitarni West (29-Mar-2023) - Final Offer, upfront, PBG, Schedule D efficiency parameters",
    "Final EIA/EMP, Baitarni West OCP 15 MTPA (GRC India) - project facts, land, reserves, production plan",
    "MIS Report of Burapahar & Baitarani West, 30-Sep-2026 (PMC) - actual and forecast status",
    "Final Tracker_cl.xlsx - 2023 activity lists (reconciled in Section 12)",
    "Bidding presentation (MoC, 10th tranche) - auction mechanics, payments and guarantees",
    "CBA Act 1957; CM(SP) Act 2015; MMDR Act 1957; EIA Notification 2006; EP Act 1986",
    "RFCTLARR Act 2013; ORFCTLARR Rules 2016; Odisha R&R Policy 2006; FRA 2006 and Rules; PESA 1996; Companies Acts",
]


# Statutory and contractual clocks: (step, limit, source)
CLOCKS = [
    ("Auction & CMDPA", "Bid security validity", "210 days from bid due date + 60-day claim period", "Tender Document"),
    ("Auction & CMDPA", "1st upfront instalment (25%)", "Within 40 business days of executing the CMDPA", "CMDPA cl. 5.2.1"),
    ("Auction & CMDPA", "2nd / 3rd / 4th instalments", "Within 15 business days of s.11(1) order (or ML) / mine opening / first coal", "CMDPA cl. 5.2.1"),
    ("Auction & CMDPA", "PBG substitution on revision", "Within 30 days of the trigger; annual revision by 30 April after opening", "CMDPA cl. 6.1.5"),
    ("Auction & CMDPA", "Efficiency parameters", "MS-2 6 m; MS-3 +18 m; MS-4 +21 m; MS-5 +6 m; total 51 m (66 m if partially explored)", "CMDPA Sch. D"),
    ("Auction & CMDPA", "Scheduled Date of Production", "75 months from vesting (end of 50% early-production rebate)", "CMDPA cl. 9.2.1"),
    ("Auction & CMDPA", "Minimum production", "≥65% of plan each FY; ≥75% over each 3-FY block; shortfall paid in 20 days", "CMDPA cl. 16.2"),
    ("Mining plan", "Technical Committee observations", "Within 15 days of receipt; observations raised only twice", "MP Guidelines 2025"),
    ("Mining plan", "Proponent compliance", "15 days, extendable to 30 days", "MP Guidelines 2025"),
    ("Mining plan", "Disposal / in-principle / final", "30 days / 5 working days / 3 days after payments confirmed", "MP Guidelines 2025"),
    ("Mining plan", "Escrow for mine closure", "Before mine opening; annual deposit by 30 September", "MP Guidelines 2025"),
    ("CBA Act", "s.4(3) entry into dwellings", "7 days' written notice to occupier", "CBA s.4 proviso"),
    ("CBA Act", "s.7(1) notice to acquire", "Within 2 years of s.4(1) (+1 year max); else s.4 lapses at 3 years", "CBA s.7"),
    ("CBA Act", "s.8 objections", "Within 30 days of s.7 notification", "CBA s.8(1)"),
    ("CBA Act", "s.9(1) declaration", "Within 3 years of s.7(1) notification", "CBA s.9 proviso"),
    ("CBA Act", "Appeal against Tribunal award", "Within 30 days to High Court", "CBA s.20"),
    ("EC", "ToR", "Within 60 days of Form-1, else applicant's ToR deemed approved", "EIA Notif. para 7(i)"),
    ("EC", "Public hearing", "Notice ≥30 days; hearing completed within 45 days of request", "EIA Notif. App. IV"),
    ("EC", "Appraisal and decision", "EAC within 60 days of final EIA; MoEFCC within 45 days (105 days)", "EIA Notif. para 8"),
    ("FC", "State desks", "DCF/Collector 20; inspections 20; Nodal/PCCF 15; PSC 30; State 15 working days", "VSSR 2023 Schedule"),
    ("FC", "MoEFCC desks", "Scrutiny 4; processing 5; IRO inspection 20; Advisory Committee 20; approval 10; letter 1 wd", "VSSR 2023 Schedule"),
    ("Rail (GCT)", "Survey, IPA, ESP", "Joint survey 15 days; IPA 20 days; ESP ≤4 weeks after IPA, Division 2 + HQ 2 weeks", "GCT Circular 2026"),
    ("Rail (GCT)", "Construction", "Start within 6 months; complete within 24 months of approval", "GCT Circular 2026"),
    ("Mine opening", "Notice to DGMS, CCO, DM", "To reach at least one month before commencement", "Mines Act s.16(2)"),
    ("Mine opening", "Intimation to CCO after Board approval", "Within 15 days of opening", "CCR (Amendment) Rules 2026"),
]

# RACI: A accountable, R responsible (does the work), S sanctions/approves, C consulted, I informed
RACI_COLS = ["GMDC", "PMC", "Consultants", "MDO", "MoC / NA / CCO", "MoEFCC", "Collector / Revenue", "Forest Dept", "OSPCB / WRD / others", "Gram Sabha / PAFs"]
RACI = [
    ("Auction & vesting", ["A R", "C", "C", "", "S", "", "", "", "", ""]),
    ("Mobilisation & surveys", ["A", "R", "R", "", "C", "", "S", "C", "C", "I"]),
    ("Mining plan (MS-2)", ["A", "C", "R", "I", "S", "", "", "", "", ""]),
    ("Environment clearance (MS-3)", ["A", "C", "R", "I", "I", "S", "C", "C", "R", "C"]),
    ("Forest clearance", ["A", "C", "R", "", "I", "S", "R", "S", "", "C"]),
    ("CBA land acquisition", ["A", "C", "R", "", "S", "", "R", "", "", "C"]),
    ("R&R (MS-4)", ["A", "C", "R", "I", "I", "", "S", "", "", "C"]),
    ("Consents & infrastructure", ["A", "C", "R", "R", "I", "", "C", "", "S", "I"]),
    ("Mine opening (MS-5) & coal", ["A S", "R", "C", "R", "I", "", "I", "", "S", "I"]),
]

# RFCTLARR 2013 entitlements applied to CBA acquisitions by S.O. 2368(E)
RR_ENT = [
    ("Compensation (First Schedule)", "Market value x multiplication factor notified by the State (1-2 in rural areas) + value of structures, trees and assets + 100% solatium; 12% p.a. additional amount from notification to award/possession"),
    ("Housing (Sch. II)", "Displaced family: house as per Indira Awas Yojana specification in rural areas (or its cost if declined)"),
    ("Employment / annuity", "Employment to one member per affected family, or one-time Rs 5 lakh, or annuity of not less than Rs 2,000/month for 20 years (indexed)"),
    ("Subsistence grant", "Rs 3,000 per month for one year to each displaced family; additional Rs 50,000 for SC/ST families displaced from Scheduled Areas"),
    ("Transport & resettlement", "One-time Rs 50,000 transportation and Rs 50,000 resettlement allowance"),
    ("Livelihood support", "Cattle shed / petty shop and artisan / small trader: one-time assistance of at least Rs 25,000 each"),
    ("Charges", "Stamp duty and registration fee for land and houses allotted are borne by the requiring body"),
    ("Third Schedule amenities", "Roads, drainage, drinking water, school, anganwadi, health centre, panchayat ghar, PDS outlet, places of worship, cremation ground, electricity, etc. in the R&R colony"),
    ("Odisha overlay", "ORRP 2006 / RPDAC-approved package; the higher of the State package and the Second Schedule should be applied - confirm with the Collector"),
]
