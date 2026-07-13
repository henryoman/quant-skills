# Asset and Venue Extensions

This section is intentionally a framework placeholder. The core instructions
remain valid for any continuously traded OHLCV series. A later asset/venue
extension must add real market mechanics without rewriting general statistics
or quietly changing evidence standards.

No equity-specific material belongs here: no earnings, corporate actions,
fundamentals, stock universe selection, opening auction assumptions, or borrow
models derived from equities.

## What an extension must declare

```text
asset/instrument family
venues and access path
base and quote assets
24/7 or scheduled trading/maintenance windows
price type: trade, index, mark, midpoint, oracle, settlement reference
native bar semantics
volume and contract units
fee tiers and rebates
tick size and minimum order size
spread/depth/impact data availability
funding, carry, expiry, settlement, or pool mechanics
latency and region constraints
shorting/position mechanics if applicable
venue failure and stale-feed behavior
official outcome/settlement truth
capacity limits
```

## What stays fixed from the general framework

- causal decision clocks;
- raw values and source labels preserved before normalization;
- train-only transformations;
- model-free baselines before complex models;
- chronological purged/walk-forward validation;
- multiple-testing accounting;
- net payoff after actual instrument costs;
- concentration and parameter stability;
- evidence ladder from proxy to fills/settlement/live;
- complete decision and rejection logging.

## Extension template

### 1. Instrument truth

```text
instrument:
venue:
contract_or_pool_identifier:
base_asset:
quote_asset:
price_source_used_for_signal:
price_source_used_for_execution:
price_source_used_for_marking:
official_settlement_or_outcome_source:
```

Explain when those prices can disagree and why. Never assume a fast spot feed,
an execution venue, and a settlement oracle measure the same object.

### 2. Bar construction

```text
native_or_local:
timezone/bar_phase:
trade_price_or_mark/index:
zero_trade_bar_policy:
maintenance/gap_policy:
volume_unit:
cross_venue_alignment:
```

### 3. Executable payoff

Write the actual instrument PnL formula, including denomination and settlement.
Then map candle labels into that payoff. A directional candle hit rate is not a
substitute for contract or pool PnL.

### 4. Costs and constraints

| Item | Exact rule/source | Base assumption | Stress |
|---|---|---:|---:|
| Fee/rebate | | | |
| Spread | | | |
| Slippage/depth | | | |
| Funding/carry | | | |
| Minimum size/tick | | | |
| Latency/staleness | | | |
| Settlement/expiry | | | |

### 5. Extension-specific features

Only include fields truly known at decision time. Examples of possible later
families—not active specifications—include:

- spot/central-limit-order-book: bid/ask, depth, trade imbalance, venue basis;
- perpetual/futures: mark-index basis, funding, open interest, liquidation
  proxies, expiry where relevant;
- on-chain/AMM or concentrated liquidity: reserves, active liquidity, bin/tick
  position, swap flow, fee capture, gas/priority cost, adverse selection;
- binary/prediction contracts: bid/ask/depth, time to expiry, strike/target,
  implied probability/spot, fee and settlement oracle.

Each family requires its own source and execution validation. These bullets are
not permission to synthesize unavailable fields.

### 6. Extension-specific failure modes

```text
oracle/venue mismatch
quote-asset mismatch
stale or crossed books
mark versus executable trade price
funding or fee schedule changes
contract migration/expiry
chain congestion or failed transactions
pool liquidity migration
settlement ambiguity
regional/API/order-size constraints
```

### 7. Promotion threshold

Declare the minimum independent forward sample, size/depth evidence, maximum
acceptable rejection rate, settlement coverage, and live-small risk cap.

## Future sections

Add a section only when a user requests that asset/instrument family and the
relevant local data/code has been inspected. Until then, the framework remains
general. In this repository, any active SOL Up/Down extension must obey the
repo-wide rule that current workflows use 5-minute markets only; historical
15-minute artifacts remain legacy unless explicitly revived.
