# Coal Mining PMC report generator

Builds `Coal Mining PMC.pdf` (repository root): auction-to-operationalisation process map for an
Odisha coal block (CBA Act land route), PERT/CPM and Monte Carlo analysis, and the Baitarani West
status forecast.

```
python3 pmc_report/build.py
```

- `model.py`   – activity networks (three-point durations, predecessors), CPM passes, Monte Carlo
- `content.py` – process narratives, granular step lists, legal tables, clocks, RACI, sources
- `charts.py`  – ReportLab flowables: flowcharts, lane map, AON network, Gantt, charts
- `build.py`   – assembles the PDF (ReportLab, Carlito font)

To refresh the forecast, update the `BW_REM` activities and `STATUS_DATE` in `model.py` and rebuild.
