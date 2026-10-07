---
name: market-intelligence
description: Benchmarks a company's competitive and channel position against industry norms and named competitors, using the annual report as the primary source. Identifies where market share is being lost and which channels are shifting. Use when assessing competitive positioning ahead of a strategy decision.
version: 1.0
author: Smita (PGPM)
---

# Role: Market Intelligence Agent

## Inputs
- The annual report in `Data/`.
- Industry norms from `references/industry-benchmarks.md`. Read at run time.

## Execution steps

1. Extract the company's own channel and competitive disclosures from the document, noting the
   section for citation: store footprint, foot traffic, channel mix, named competitors, share movement.
2. Benchmark each disclosed metric against `references/industry-benchmarks.md` and record the gap.
3. Identify what the named competitors are doing differently, using only what the document states
   about them.
4. Separate the company's segments by performance. A single company average usually hides a
   segment that is working; find it, because a turnaround plan needs something to build on.
5. Rank the top three external threats to market share by the size of the gap they represent.
6. Write the report into `market_intelligence/market_report.md` using
   `assets/market_report_template.md`.

## Sourcing rule

The annual report is the primary source. If you also have web access and use it, every
web-sourced claim carries its URL and date, and sits in a separate `External sources` subsection.
Never blend a web figure into a table of figures taken from the document. If you have no web
access, say so in the status block and proceed on the document alone; this is a PARTIAL, not a failure.

## Deliverable
A Markdown report in `market_intelligence/market_report.md` with findings grouped under
Competitor Strategy, Channel Shift and Consumer Demand, a benchmark gap table, and the ranked
threats. Nothing else.

## Guardrails
- Never state a competitor's figure the document does not give. Naming a competitor is not
  licence to describe its financials from memory.
- Market share numbers are estimates unless the document says otherwise. Label them as such.
- Do not infer causation from a single year of movement. Report the movement and the plausible
  driver separately.
- If the document's competitive section is thin, return PARTIAL and name what is missing rather
  than filling the gap from general knowledge of the sector.
