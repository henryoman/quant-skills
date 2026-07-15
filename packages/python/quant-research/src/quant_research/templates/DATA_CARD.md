# Data Card

## Identity

- Asset: TODO
- Venue: TODO
- Instrument type: TODO
- Bar interval: TODO
- Timestamp timezone: TODO
- Timestamp semantics: TODO (`open_time`, `close_time`, or documented alternative)
- Date range: TODO
- Observation count: TODO
- Raw data path: TODO (relative to the cycle directory)
- Raw data hash: TODO

## Available fields

- TODO

## Audit results

| Check | Result | Affected rows | Research impact | Action |
|---|---|---:|---|---|
| Ordering | TODO | TODO | TODO | TODO |
| Duplicate timestamps | TODO | TODO | TODO | TODO |
| Missing/irregular intervals | TODO | TODO | TODO | TODO |
| OHLC invariants | TODO | TODO | TODO | TODO |
| Nonpositive prices | TODO | TODO | TODO | TODO |
| Zero/negative volume | TODO | TODO | TODO | TODO |
| Stale prices | TODO | TODO | TODO | TODO |
| Outlier bars | TODO | TODO | TODO | TODO |
| Final incomplete bar | TODO | TODO | TODO | TODO |

## Structural breaks and caveats

TODO

## Repair ledger

Do not repair silently.

| Issue | Proposed repair | Rows affected | Could influence results? | Approved? |
|---|---|---:|---|---|
| TODO | TODO | TODO | TODO | TODO |

## Execution limitations

TODO

## Approval

- Data accepted for structural profiling: TODO
- Data accepted for alpha testing: TODO
- Reviewer/date: TODO
