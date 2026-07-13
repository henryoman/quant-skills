# Experiment Catalog

This catalog is a research menu, not a mandate to optimize every cell. The IDs
make failures and follow-ups traceable. Start with `E00-E07`, then test each
major family with a small, predeclared grid. Promote only families showing a
broad, stable conditional effect.

For every experiment:

```text
inputs at t -> future outcome after t
```

Run long and short orientations separately before combining them. Report gross
prediction evidence before strategy logic, then net trading evidence after a
fixed decision rule. Use [EXPERIMENT_TEMPLATE.md](EXPERIMENT_TEMPLATE.md) for
the complete variable/control declaration.

## Standard parameter axes

Translate bars to clock time in every report. A reasonable first grid is:

```text
feature lookbacks: [1, 2, 3, 5, 10, 20, 40, 80] bars
forecast horizons: [1, 2, 5, 10, 20] bars
rolling contexts: [20, 60, 240] bars
quantile bins: [5, 10] equal-count bins fitted on train
deadbands: [0, 0.10, 0.25, 0.50] * past_sigma * sqrt(h)
confidence thresholds: small validation-only grid
cost stress: [0.5x, 1x, 1.5x, 2x] base all-in cost
entry delay: [0, 1, 2] bars or venue-specific time delays
```

These are examples, not magic defaults. Reduce the grid when the dataset is
small. Each combination counts toward the multiple-testing budget.

## A. Data, nulls, and unconditional structure

### E00 — Data-contract audit

- Question: are the candles internally valid and semantically known?
- Setup: apply every invariant and metadata requirement in
  [DATA_AND_LABELS.md](DATA_AND_LABELS.md).
- Varied: none.
- Fixed: source files and cleaning policy.
- Plot: missing/gap timeline; invalid-bar counts; interval histogram.
- Pass: no unexplained timestamp/price violations; every removal is counted.
- Reject/repair: conflicting duplicates, mixed bar clocks, unknown quote/volume
  units, or unexplained source changes.

### E01 — Gap, stale-feed, and outlier audit

- Question: can gaps or bad ticks create the apparent edge?
- Setup: flag return/range/volume extremes with robust train-only medians/MAD,
  but inspect raw bars before filtering.
- Varied: robust flag threshold, for diagnostics only.
- Fixed: no signal modeling.
- Plot: returns with flags; gap-length histogram; before/after distributions.
- Pass: candidate result survives both raw-with-flags and defensibly repaired
  datasets.
- Reject: PnL or lift concentrates in data-error windows.

### E02 — Bar-construction sensitivity

- Question: does the finding depend on arbitrary candle boundaries?
- Setup: rebuild or compare equal-duration bars with several clock offsets; if
  raw trades exist, also compare time, volume, or dollar bars.
- Varied: bar duration, phase offset, bar type.
- Fixed: UTC range, underlying source, target clock time, costs.
- Plot: metric by duration × offset; signal overlap; normalized price paths.
- Pass: a plateau across neighboring durations/offsets.
- Reject: one exact clock alignment owns the result without a venue reason.

### E03 — Unconditional target baseline

- Question: what happens without any feature?
- Setup: measure distribution, class balance, base hit rate, mean/median,
  quantiles, tail loss, and naive expected payoff for every label/horizon.
- Varied: target and horizon.
- Fixed: data and decision clock.
- Plot: return histogram/ECDF; horizon fan; base-rate table.
- Pass: baseline is recorded; there is nothing to “beat” until this exists.

### E04 — Shuffled-label negative control

- Question: can the pipeline manufacture edge from noise?
- Setup: shuffle labels in blocks large enough to preserve local dependence, or
  circularly shift labels beyond the maximum horizon; rerun selection.
- Varied: random seeds and block sizes.
- Fixed: complete feature/model/search pipeline.
- Plot: real score against null score distribution.
- Pass: real result is exceptional relative to the full search null.
- Reject: shuffled data routinely produces similar winners.

### E05 — Naive predictor baselines

- Question: does the candidate beat trivial forecasts?
- Setup: unconditional mean/median/class; zero return; last return sign;
  volatility persistence; always long/short/flat; random rule with equal
  exposure/turnover.
- Varied: baseline family.
- Fixed: same rows, horizon, costs, and exposure constraints.
- Plot: metric and equity comparison.
- Pass: candidate adds meaningful net value over the relevant naive baseline.

## B. Model-free conditional discovery

### E06 — Univariate equal-count bins

- Question: does one present feature shift a future outcome monotonically or at
  the tails?
- Setup: fit train quantile edges; apply unchanged to valid/test; report count,
  mean, median, quantiles, hit rate, t-stat/interval, and net payoff by bin.
- Varied: feature, lookback, target, horizon, 5 versus 10 bins.
- Fixed: split, label, cost, and bin edges within each comparison.
- Plot: outcome with uncertainty by bin, plus support.
- Pass: ordered or economically interpretable pattern seen across splits—not
  one lucky bucket.

### E07 — Two-dimensional conditional heatmap

- Question: does the effect live in an interaction or regime intersection?
- Setup: train-fit 5×5 or 10×10 quantile grid for two features; compute outcome
  level, excess versus unconditional baseline, support, and uncertainty.
- Varied: a limited pair list and horizon.
- Fixed: axes/bins across splits; never independently recolor each panel.
- Plot: train, validation, test outcome heatmaps followed by support heatmaps.
- Pass: contiguous cluster with enough support, same sign, and neighboring-cell
  stability across time.
- Reject: isolated hot pixel, edge-only sparse cells, or color driven by a few
  overlapping events. See [VISUAL_GUIDE.md](VISUAL_GUIDE.md).

### E08 — Event study

- Question: what path follows a defined event?
- Setup: define event using present/past data, de-overlap events, index path to
  event time zero, and compare to matched control periods.
- Varied: event threshold and forward path length on train/validation.
- Fixed: event definition for test; matching variables; no overlapping event
  stacking.
- Plot: average/median cumulative path with block-bootstrap band; MFE/MAE.
- Pass: timing and payoff shape persist versus matched controls.

### E09 — Conditional distribution shift

- Question: does a state change the whole future distribution rather than only
  its mean?
- Setup: compare ECDFs/quantiles/tails for state versus unconditional/matched
  rows; use KS/energy/Wasserstein as diagnostics, not standalone proof.
- Varied: state and target.
- Fixed: sample windows and multiple-test correction.
- Plot: overlaid ECDF, quantile-difference curve, tail exceedance curve.
- Pass: economically relevant quantile shift with stable sign and magnitude.

### E10 — Threshold and parameter plateau

- Question: is the rule robust near the selected cutoff?
- Setup: evaluate a dense local neighborhood around a validation-selected
  threshold/lookback; carry the neighborhood unchanged into test.
- Varied: one or two parameters only.
- Fixed: everything else.
- Plot: full parameter surface with trade/support contours and selected point.
- Pass: broad plateau, not a needle peak.

## C. Candle morphology and classical patterns

### E11 — Continuous candle-geometry scan

- Question: do body, wick, range, or close location predict future direction,
  range, volatility, or path quality?
- Setup: use continuous fractions before named patterns.
- Varied: `body_frac`, `upper_frac`, `lower_frac`, `close_pos`, signed body,
  range percentile; targets/horizons.
- Fixed: current candle is fully closed; scale is past-only.
- Plot: univariate profiles and geometry × regime heatmaps.
- Pass: stable, supported region rather than a folklore name.

### E12 — Named single-candle taxonomy

- Question: do doji/hammer/body-style tokens add information beyond continuous
  geometry?
- Setup: train/freeze thresholds; include an `unclassified`/flat state.
- Varied: a small threshold grid for body and zone fractions.
- Fixed: token vocabulary and future labels after validation.
- Plot: class probability and net payoff by token; confusion/support tables.
- Pass: tokens add incremental out-of-sample information after controlling for
  range, volatility, and prior direction.

### E13 — Two/three-candle patterns

- Question: do engulfing, inside/outside, rejection, or consecutive-body
  geometries forecast follow-through/reversal?
- Setup: express every named pattern numerically: coverage, extension, body
  ratio, close strength, prior direction, range/volume context.
- Varied: pattern thresholds and context gates.
- Fixed: pattern formula, target, non-overlap rule.
- Plot: state table, geometry heatmap, event path.
- Pass: effect grows logically with pattern strength and survives simpler
  continuous controls.

### E14 — Wick rejection versus continuation

- Question: does a long wick mean rejection, or is it simply high volatility?
- Setup: condition on wick fraction, close position, direction into the candle,
  range percentile, and relative volume.
- Varied: wick/close thresholds.
- Fixed: volatility and trend matching.
- Plot: wick × prior trend heatmap; future MFE/MAE and return paths.
- Pass: incremental effect beyond large-range control.

### E15 — Pattern incremental-value test

- Question: does the pattern contribute beyond standard numeric features?
- Setup: compare identical baseline models with and without pattern features or
  compare matched samples.
- Varied: pattern family only.
- Fixed: rows, splits, model class, hyperparameters, costs.
- Plot: fold-by-fold metric delta and permutation/drop-column delta.
- Pass: consistent incremental value; reject if folklore relabels geometry
  already captured elsewhere.

## D. Trend, momentum, and continuation

### E16 — Return continuation surface

- Question: do past returns predict same-direction future returns?
- Setup: past return quantile × horizon; normalize by past volatility.
- Varied: lookback and forecast horizon.
- Fixed: same direction rule and cost.
- Plot: lookback × horizon heatmap; decile profile; event paths.
- Pass: contiguous positive region after costs and delay.

### E17 — Multi-scale trend alignment

- Question: does agreement across short/medium/long trends improve continuation?
- Setup: signs/slopes of returns or MAs at several clock scales.
- Varied: scale triplets and strength threshold.
- Fixed: base timeframe and execution rule.
- Plot: discrete state table; alignment count × strength heatmap.
- Pass: ordered lift as alignment/strength rises with adequate support.

### E18 — Momentum acceleration/deceleration

- Question: is the short return stronger or weaker than the long-run pace?
- Setup: `ret_short - ret_long * short/long`, optionally volatility-normalized.
- Varied: short/long pairs.
- Fixed: formula and horizon.
- Plot: acceleration bins versus future direction, range, and drawdown.
- Pass: stable effect not reducible to the raw short return.

### E19 — Trend cleanliness/path efficiency

- Question: does a clean recent path continue better than a choppy path with
  the same net return?
- Setup: match on past return, split by path efficiency/body-to-range quality.
- Varied: lookback and cleanliness threshold.
- Fixed: past-return bucket and future target.
- Plot: return × efficiency heatmap; matched event paths.
- Pass: incremental continuation or lower adverse excursion.

## E. Mean reversion and exhaustion

### E20 — Distance-from-mean reversion

- Question: do standardized deviations from rolling mean/EMA/VWAP proxy revert?
- Setup: distance divided by past volatility; future return oriented toward the
  mean.
- Varied: mean type, lookback, z threshold, horizon.
- Fixed: no future-centered smoothing.
- Plot: z-score profile; lookback × horizon heatmap; time-to-mean curve.
- Pass: symmetric or explainably asymmetric reversion after costs.

### E21 — Oscillator incremental test

- Question: do RSI/Bollinger/percent-rank style oscillators add beyond their
  underlying return and volatility inputs?
- Setup: matched or nested-model comparison.
- Varied: oscillator lookback and extreme cutoff.
- Fixed: base numeric controls and model class.
- Plot: oscillator bins; incremental fold delta.
- Pass: added information, not merely a rescaled return.

### E22 — Exhaustion interaction

- Question: do extreme move + volume/range/wick conditions mark reversal or
  continuation?
- Setup: past return extreme × volume shock × close/wick quality.
- Varied: limited threshold grid.
- Fixed: matched volatility and time period.
- Plot: 2D/3D sliced heatmaps, MFE/MAE event paths.
- Pass: contiguous regime, enough events, consistent across folds.

## F. Breakout, range, and support/resistance without chart mysticism

### E23 — Breakout and failed-breakout study

- Question: after crossing a prior rolling high/low, does price continue or
  fail?
- Setup: prior boundary excludes current bar; measure break distance, close
  retention, volume/range context, and return inside boundary.
- Varied: boundary lookback, break threshold, confirmation delay.
- Fixed: causal boundary and exit rule.
- Plot: event paths; break strength × volume heatmap; failure-time histogram.
- Pass: delayed entries still retain net edge.

### E24 — Compression-to-expansion

- Question: does low current range/volatility relative to longer context predict
  future range expansion?
- Setup: short/long volatility, range, Bollinger-width, or ATR ratios.
- Varied: short/long windows and low-percentile threshold.
- Fixed: target is magnitude/range before direction.
- Plot: compression percentile versus future range; horizon surface.
- Pass: strong out-of-sample magnitude signal; directional use needs separate
  evidence.

### E25 — Range position and boundary proximity

- Question: does position inside a rolling high-low range predict breakout,
  bounce, or risk?
- Setup: `(close - rolling_low)/(rolling_high-rolling_low)` with boundary built
  from prior bars.
- Varied: range lookback and horizon.
- Fixed: volatility normalization.
- Plot: position deciles versus return/upside/downside/barrier labels.
- Pass: stable conditional distribution shift.

### E26 — False-break/return-inside state

- Question: is a close back inside a recently crossed range predictive?
- Setup: define break, excursion, re-entry, and confirmation causally.
- Varied: break/re-entry thresholds.
- Fixed: event de-overlap and target.
- Plot: event study and excursion × close-retention surface.
- Pass: re-entry event adds beyond wick and volatility controls.

## G. Volatility, range, and volume

### E27 — Volatility persistence and term structure

- Question: does past volatility forecast future volatility/range?
- Setup: realized vol, absolute returns, ATR, and range estimators at multiple
  windows; compare naive persistence, HAR-style linear model, and quantiles.
- Varied: estimator, lookback, horizon.
- Fixed: scale and split.
- Plot: past-vol bins; lookback × horizon score heatmap; calibration by quantile.
- Pass: stable magnitude forecast that beats unconditional and last-value
  baselines.

### E28 — Volatility-of-volatility and shock decay

- Question: after a volatility shock, how fast does magnitude normalize?
- Setup: vol z-score/event plus forward vol/range path.
- Varied: shock threshold and context window.
- Fixed: de-overlapped events.
- Plot: decay curve, half-life distribution, regime slices.
- Pass: repeatable decay/persistence useful for holding time or no-trade rules.

### E29 — Volume × volatility opportunity map

- Question: does volume identify when movement is large enough to overcome
  costs, without assuming direction?
- Setup: relative volume × volatility/range expansion; target future absolute
  move/range and separately signed continuation/reversal.
- Varied: volume normalization, vol window, horizon.
- Fixed: venue/unit and cost hurdle.
- Plot: full-width heatmap plus support; magnitude and direction panels.
- Pass: magnitude edge may qualify as a gate even if direction is null.

### E30 — Volume-price confirmation/exhaustion

- Question: does relative volume change continuation or reversal after a signed
  move?
- Setup: past return/body direction × volume percentile/trend.
- Varied: lookback and volume threshold.
- Fixed: matched volatility/range.
- Plot: signed-move × volume heatmap; event paths.
- Pass: consistent interaction. Reject “high volume means follow-through” if
  direction panel fails despite magnitude lift.

## H. Calendar and recurring time structure

### E31 — Intraday/day-of-week seasonality

- Question: do return, volatility, range, volume, cost, or signal efficacy vary
  by UTC clock?
- Setup: hour/minute cyclic features and discrete bins; continuous markets still
  have venue/session rhythms.
- Varied: clock granularity and horizon.
- Fixed: UTC plus local/session labels when relevant.
- Plot: hour × weekday heatmap for mean, variance, support, and net strategy.
- Pass: repeated across months and not explained only by one episode.

### E32 — Period-boundary effects

- Question: do funding, settlement, auction, maintenance, data-release, or bar
  boundary times change behavior?
- Setup: event-distance feature around venue-relevant scheduled times.
- Varied: before/after windows.
- Fixed: event calendar known in advance.
- Plot: event-time path and distribution shift.
- Pass: persists across many events after costs. General framework stays neutral;
  details belong in asset/venue extensions.

## I. Time-series dependence and statistical structure

### E33 — Autocorrelation and variance ratio

- Question: do returns show short-horizon continuation or reversal?
- Setup: ACF/PACF with robust intervals; variance-ratio across horizons; repeat
  by volatility/time regime.
- Varied: lag and regime.
- Fixed: sampling and return definition.
- Plot: ACF/PACF; lag × regime heatmap.
- Pass: stable enough magnitude to translate into a costed rule; statistical
  significance alone is insufficient.

### E34 — Conditional heteroskedasticity

- Question: is variance predictable even when mean is not?
- Setup: squared/absolute-return ACF, ARCH-style diagnostics, simple EWMA/HAR and
  optional GARCH benchmark.
- Varied: volatility model/window.
- Fixed: same future-vol label and evaluation loss.
- Plot: predicted versus realized vol; calibration; residual ACF.
- Pass: out-of-sample loss improvement useful for sizing/gating.

### E35 — Hurst/fractal/long-memory diagnostics

- Question: is apparent persistence consistent across scales?
- Setup: rolling rescaled-range/DFA/Hurst estimates with synthetic/null
  calibration and regime comparison.
- Varied: estimation scale/window.
- Fixed: estimator and sampling.
- Plot: estimate over time and by regime; null distribution.
- Pass: use only as a descriptive/regime feature if stable. Never infer a
  strategy directly from `H > 0.5`.

### E36 — Spectral and cycle diagnostics

- Question: is there repeatable periodic structure beyond clock seasonality?
- Setup: detrended returns/vol/volume; periodogram/wavelet or spectral density;
  compare rolling windows and surrogate data.
- Varied: window and series.
- Fixed: detrending and sampling.
- Plot: frequency power across time; surrogate bands.
- Pass: stable phase/frequency with a causal implementation. Most isolated
  peaks should be treated skeptically.

## J. States, sequences, and information

### E37 — State table / Markov transition

- Question: does a compact discrete current state change the next-state or
  future-outcome probabilities?
- Setup: train-fit tokens from signs, quantiles, candle geometry, trend, or
  regime; count transitions; apply smoothing and minimum support.
- Varied: token vocabulary, order `k`, smoothing, horizon.
- Fixed: state thresholds and vocabulary on valid/test.
- Plot: transition matrix; state support; probability lift; test survival.
- Pass: supported states retain direction/magnitude lift out of sample.
- Reject: state space grows faster than evidence (`classes^features` or
  `tokens^k`) and most states are sparse.

### E38 — Sequence n-gram incremental value

- Question: does order matter beyond the latest token and aggregate returns?
- Setup: compare Markov orders `k=1,2,3...` and a matched continuous-feature
  baseline.
- Varied: order and vocabulary only.
- Fixed: target and smoothing.
- Plot: out-of-sample log loss/accuracy/net payoff versus order; coverage.
- Pass: higher order adds value without state-collapse.

### E39 — Entropy and mutual information

- Question: where does uncertainty fall, and does a feature contain nonlinear
  information about the target?
- Setup: estimate entropy/conditional entropy/MI with bias-aware estimators or
  permutation baseline; calculate on train, confirm on test.
- Varied: feature, binning/estimator, horizon.
- Fixed: target and sample.
- Plot: MI versus null; conditional entropy by state/support.
- Pass: repeatable information that also produces economic lift. MI does not
  specify trade direction by itself.

## K. Regimes and unsupervised learning

### E40 — Simple rule-based regimes

- Question: when does a signal work or fail?
- Setup: predeclare low/medium/high vol, trend/chop, liquid/thin, compressed/
  expanding states with train quantiles.
- Varied: small threshold grid.
- Fixed: base signal unchanged.
- Plot: signal net payoff and support by regime/fold.
- Pass: regime gate improves worst folds/drawdown without deleting nearly all
  trades.

### E41 — Clustering

- Question: do recurring OHLCV states emerge without outcome labels?
- Setup: robustly scale training features; fit k-means/GMM/hierarchical or
  density clustering; assign future rows without refitting.
- Varied: feature set and small cluster-count grid.
- Fixed: target never used to form clusters.
- Plot: cluster profiles, transition matrix, occupancy over time, future-outcome
  distributions.
- Pass: clusters recur, remain populated, and route signal performance. Reject
  pretty 2D embeddings that have no stable outcome or time persistence.

### E42 — Hidden-state/HMM regime

- Question: do persistent latent volatility/trend states improve forecasting or
  strategy gating?
- Setup: fit on training observations; infer filtered (not future-smoothed)
  state probabilities for live realism.
- Varied: state count and observation family.
- Fixed: causal filtered inference.
- Plot: state probability timeline, transition matrix, dwell time, performance
  by state.
- Pass: stable dwell/transition behavior and out-of-sample incremental value.

### E43 — Change-point detection

- Question: did the data-generating regime shift enough to retire or retrain a
  rule?
- Setup: causal CUSUM/Bayesian/rolling-distribution detectors on returns,
  volatility, volume, residuals, or strategy PnL.
- Varied: detector threshold on historical training episodes.
- Fixed: response policy.
- Plot: change scores over price/vol/PnL; pre/post distributions.
- Pass: useful kill switch or retraining trigger with tolerable false alarms.

## L. Supervised prediction

### E44 — Linear/logistic baseline

- Question: can a transparent linear combination of features beat simple
  baselines?
- Setup: train-only scaling/imputation; ridge/elastic net or logistic; class
  balance handled inside train.
- Varied: regularization, feature family, target/horizon.
- Fixed: chronological splits and selection metric.
- Plot: coefficient stability by fold; calibration; prediction deciles.
- Pass: signs and probability/payoff ordering survive folds.

### E45 — Tree/boosting tabular model

- Question: do nonlinear interactions add incremental value?
- Setup: random forest, extra trees, histogram/gradient boosting; shallow/simple
  baselines first; tune only on validation.
- Varied: small depth/leaf/regularization grid.
- Fixed: feature set, rows, target, costs.
- Plot: prediction deciles, calibration, permutation/drop-column importance,
  partial/ALE shapes, fold scores.
- Pass: incremental test value over linear and model-free baselines, not just
  feature importance theater.

### E46 — Quantile/distribution model

- Question: can the model predict downside/upside/range quantiles rather than a
  point estimate?
- Setup: quantile regression or distributional model for returns/MFE/MAE/range.
- Varied: quantiles and model family.
- Fixed: pinball/coverage scoring.
- Plot: predicted interval coverage, width, calibration, conditional tails.
- Pass: calibrated intervals and economically useful tail separation.

### E47 — Sequence model benchmark

- Question: do raw/derived sequences add value beyond tabular summaries?
- Setup: only after E38/tabular baselines; try 1D CNN, recurrent model, or small
  transformer with strict capacity control.
- Varied: sequence length and one compact architecture grid.
- Fixed: identical folds/targets/costs and parameter-count report.
- Plot: learning curves, fold results, calibration, comparison to n-gram and
  boosted-tree baselines.
- Pass: clear incremental value after compute/complexity penalty. Otherwise keep
  the simpler model.

### E48 — Ensemble and signal combination

- Question: do independent families combine better than the strongest member?
- Setup: combine out-of-fold predictions only; test agreement, veto, ranking,
  or regularized stacking.
- Varied: combination rule on validation.
- Fixed: component models frozen and final test untouched.
- Plot: overlap/Venn or correlation matrix, payoff by agreement count, fold
  delta.
- Pass: better robustness/net payoff with explainable diversification, not
  duplicate signals counted twice.

## M. Cross-asset and cross-venue structure

### E49 — Lead-lag predictive power

- Question: does asset/venue A at `t` predict asset/venue B after `t`?
- Setup: align clocks; lag A features; predict B return/range/vol; compare B-only
  model versus A+B model.
- Varied: lags, horizons, limited leader set.
- Fixed: venues, quote normalization, missing-bar policy.
- Plot: lag × horizon heatmap; incremental fold score; event paths.
- Pass: causal lag survives latency/delay and B-only controls.

### E50 — Relative move/catch-up

- Question: after A moves more than B on a normalized basis, does B catch up or
  diverge?
- Setup: `relative_return = normalized_A_return - beta * normalized_B_return`;
  estimate beta on training only.
- Varied: lookback, horizon, beta model.
- Fixed: entry asset B and cost model.
- Plot: relative-move bins, event study, beta stability.
- Pass: stable conditional B response after both venue costs.

### E51 — Rolling dependence and correlation breakdown

- Question: when is the A/B relationship reliable enough to use?
- Setup: rolling correlation/beta/residual volatility and shock differences;
  condition the base lead-lag signal.
- Varied: dependence window/regime.
- Fixed: base signal.
- Plot: dependence timeline; signal payoff by dependence regime.
- Pass: improves risk or turns off failing regimes without over-selection.

### E52 — Feed/venue disagreement

- Question: are different prices informative or merely different quote assets,
  indexes, latency, and construction?
- Setup: preserve raw prices; normalize each feed from its own start with log
  returns; record quote, age, venue, and target/settlement source.
- Varied: feed pair and normalization horizon.
- Fixed: clock alignment and official reference.
- Plot: raw basis and normalized-return basis separately; age × disagreement.
- Pass: disagreement survives normalization, costs, and the actual tradable
  instrument/settlement mapping. Otherwise it is diagnostic only.

## N. Strategy translation and execution reality

### E53 — Exact rule backtest

- Question: does one frozen prediction-to-position rule make net money?
- Setup: signal threshold, side, entry, exit, size, concurrency, netting, skip
  reasons, and cost formula fixed before test.
- Varied: none on final test.
- Fixed: everything declared in the experiment spec.
- Plot: net equity, drawdown, trade PnL distribution, exposure, turnover.
- Pass: positive net payoff with acceptable downside and concentration.

### E54 — Purged walk-forward replay

- Question: does the complete research/selection process work repeatedly through
  time?
- Setup: train → validation selection → purge/embargo → unseen test, roll
  forward; stitch only unseen decisions.
- Varied: optionally a predeclared window scheme robustness set.
- Fixed: candidate family and selection procedure.
- Plot: split map, fold table, fold equity/drawdown one chart per row.
- Pass: majority of meaningful folds positive, aggregate not owned by one fold,
  and live-plausible retraining cadence.

### E55 — Cost, spread, slippage, and delay surface

- Question: how much friction can the edge tolerate?
- Setup: recompute full strategy over cost × entry-delay × size assumptions.
- Varied: all-in cost, spread, slippage, latency/delay, optional funding.
- Fixed: raw signal and side rule.
- Plot: net outcome heatmap with trade count; break-even contour.
- Pass: positive region includes conservative reality, not only zero cost and
  instant fill.

### E56 — Stop/target/holding-period path test

- Question: does exit engineering improve a valid entry signal or merely
  overfit intrabar ambiguity?
- Setup: use lower-frequency execution data when barriers can co-occur inside a
  bar; compare time exit, stop/target, trailing, and signal exit.
- Varied: small exit grid on validation.
- Fixed: entry signal and ambiguity policy.
- Plot: exit parameter surface, MFE/MAE, holding-time distribution.
- Pass: broad improvement robust to conservative same-bar ordering.

### E57 — Sizing and concurrency

- Question: does the edge survive realistic capital allocation and overlapping
  signals?
- Setup: fixed notional, volatility targeting, confidence sizing, and capped
  Kelly as comparisons; enforce max concurrent exposure.
- Varied: sizing family and cap on validation.
- Fixed: underlying entries/exits.
- Plot: return/drawdown/exposure/capacity comparison.
- Pass: sizing improves risk without making alpha depend on leverage.

### E58 — Concentration and leave-one-bucket-out

- Question: is PnL dependent on one day, month, hour, side, regime, asset, or
  extreme trade?
- Setup: contribution shares, top-N removal, leave-one-bucket-out replay.
- Varied: bucket family.
- Fixed: strategy.
- Plot: contribution bars, Lorenz curve, leave-one-out net outcome.
- Pass: conclusion survives removal of plausible dominant buckets.

### E59 — Forward paper and fillability audit

- Question: do real-time decisions, quotes, depth, and outcomes match the
  candle backtest?
- Setup: log raw payloads, feature snapshot, decision, rejection reason, quote,
  full-depth VWAP, fees, latency, fill status, and official outcome.
- Varied: none during a frozen paper cohort.
- Fixed: versioned strategy/config.
- Plot: predicted versus actual; backtest proxy versus executable price; slippage
  and rejection distributions; settled PnL.
- Pass: sufficient forward sample remains net positive and replayable.

## Recommended order by question

| If the question is… | Start with | Then |
|---|---|---|
| “Does anything predict direction?” | E03-E07, E16, E20, E33 | E37, E44-E45, E53-E55 |
| “Will it move a lot?” | E24, E27-E30, E34 | E46, E53-E55 |
| “Do candle patterns work?” | E11, E13-E15 | E37, E53-E55 |
| “When does a signal fail?” | E31, E40-E43, E51, E58 | E54-E55, E59 |
| “Does another asset/venue lead?” | E49-E52 | E54-E55, E59 |
| “Is this heatmap cluster real?” | E07, E10, E04 | E54, E58 |
| “Can ML find more?” | E06-E10 first | E44-E48 only afterward |

## What to kill quickly

Stop or demote a family when:

- it cannot beat the unconditional/naive baseline;
- the sign changes across train, validation, and test without a declared regime;
- only one sparse heatmap cell works;
- only one exact threshold/lookback works;
- performance disappears with one-bar delay or realistic cost;
- shuffled labels produce comparable winners;
- a complex model cannot beat a transparent baseline;
- one day/month/trade owns the result;
- the apparent cross-feed edge disappears after start-normalized log returns;
- candle-only assumptions are being described as actual fills.

Recording a clean failure is progress: it shrinks the search space and protects
capital.
