# Foundational Quant Research Sources for 1-Minute BTC OHLCV

Verified online: 2026-07-13

This is a curated source list, not a trading framework. It prioritizes primary papers, university material, official scientific-library documentation, and executable Jupyter notebooks. It excludes influencer trading content, indicator-list articles, and unsupported “AI predicts Bitcoin” demos.

## Legend

| Label | Meaning |
|---|---|
| **Direct** | Can be applied to a single 1-minute BTC OHLCV series after replacing the example data. |
| **Adapt** | The method transfers, but the source uses another asset or sampling horizon. |
| **More data** | Requires another series, futures basis/funding, tick trades, or order-book data. |
| **Notebook/code** | Executable implementation or code-first documentation. |
| **Paper** | Primary academic paper or institutional working paper. |

## The strongest starting sources

These are the cleanest resources to open first because they contain executable work and cover different approaches rather than variations of one model.

| Resource | Fit | What it gives you |
|---|---|---|
| [Forecasting: Principles and Practice, the Pythonic Way](https://otexts.com/fpppy/) | **Direct · code-first textbook** | A rigorous open Python text covering transformations, residual diagnostics, statistical benchmarks, forecast evaluation, prediction intervals, and rolling-origin validation. It is not finance-specific, which is useful: it teaches forecasting mechanics without trading mythology. |
| [Scikit-learn: lagged features for time-series forecasting](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html) | **Direct · notebook** | A compact, downloadable notebook for turning a time series into lagged features, fitting gradient-boosted trees, using `TimeSeriesSplit`, and producing quantile forecasts. It explicitly demonstrates how a shuffled split gives falsely optimistic results. Replace the demand target with a forward BTC return, realized variance, range, or event label. |
| [Quantopian quantitative research lecture notebooks](https://github.com/quantopian/research_public/tree/master/notebooks/lectures) | **Adapt · 55+ notebooks** | One of the best free archives of basic quantitative-research notebooks: hypothesis tests, regression diagnostics, stationarity, AR models, GARCH, Kalman filters, futures, slippage, market impact, overfitting, and multiple comparisons. Some data-loading calls are obsolete, but the mathematics and experiment structure remain useful. |
| [Machine Learning for Trading, 3rd edition repository](https://github.com/stefan-jansen/machine-learning-for-trading) | **Direct/Adapt · notebooks and libraries** | A broad research-to-production codebase: data quality, feature/label engineering, leakage-safe preparation, model diagnostics, deflated Sharpe, cost-aware backtesting, and live-trading structure. This is the most comprehensive single Python repository in the list; use the individual notebooks rather than treating it as a black-box strategy generator. |
| [Microsoft Qlib](https://github.com/microsoft/qlib) | **Adapt · notebook/platform** | A reproducible ML research workflow with LightGBM, MLP, LSTM, GRU, ALSTM, transformers, signal analysis, information coefficients, cost-aware backtests, and graphical reports. It is most natural for multiple assets; it becomes more useful if BTC is joined by ETH, SOL, funding, basis, open interest, or exchange-level series. |
| [ARCH: univariate volatility modeling](https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_modeling.html) | **Direct · notebook** | The cleanest Python implementation of ARCH, GARCH, GJR-GARCH, TARCH/ZARCH, Student-t errors, parameter estimation, diagnostic summaries, and conditional-volatility plots. Use BTC log returns instead of the example S&P data. |
| [ARCH: volatility forecasting](https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_forecasting.html) | **Direct · notebook** | Shows analytical, simulation, and bootstrap forecasts from fitted volatility models, including genuine out-of-sample forecasting. It is the immediate executable companion to Engle and Bollerslev. |
| [StatsForecast: GARCH and ARCH tutorial](https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/garch_tutorial.html) | **Direct · notebook** | A second, simple Python implementation of conditional-volatility forecasting. Useful for checking whether an `arch` result is implementation-specific and for comparing volatility models in a unified forecasting interface. |
| [VectorBT open-source documentation](https://vectorbt.dev/) and [usage examples](https://vectorbt.dev/getting-started/usage/) | **Direct · code-first backtesting** | Fast parameter sweeps, signal-to-position conversion, fees, trade records, drawdowns, and portfolio statistics. Good for screening many simple hypotheses. It will not automatically prevent same-bar lookahead, optimistic close fills, missing funding, or invalid intrabar stop assumptions. |
| [Mlfin.py labeling documentation](https://mlfinpy.readthedocs.io/en/latest/Labelling.html) | **Direct · code-first** | Implementations and equations for raw forward returns, fixed-horizon direction labels, dynamic thresholds, triple-barrier labels, and meta-labeling. This answers the concrete ML question “what exactly should the target be?” without forcing every experiment into next-bar direction classification. |
| [ARCH multiple-comparison tests](https://arch.readthedocs.io/en/stable/multiple-comparison/multiple-comparison_examples.html) | **Direct · notebook** | Executable Superior Predictive Ability/Reality Check, StepM, and Model Confidence Set tests. Give it the loss series from all candidate forecasts or rules; it tests whether apparent winners remain superior after searching many alternatives. |
| [PyTorch official time-sequence prediction example](https://github.com/pytorch/examples/tree/main/time_sequence_prediction) | **Direct · minimal code** | A deliberately small LSTM example using two `LSTMCell` layers. It is a clean way to learn the tensor shapes, recurrent state, training loop, and multi-step prediction mechanics before touching a large forecasting framework. The toy sine-wave predictability is not evidence that an LSTM will predict BTC. |
| [NeuralForecast end-to-end walkthrough](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/getting_started_complete.html) | **Direct · Colab notebook** | A runnable workflow for LSTM/GRU/TCN/N-BEATS/N-HiTS/transformer-family models with temporal cross-validation. It gives a consistent interface for comparing neural models rather than hand-writing a different training loop for each architecture. |
| [NeuralForecast probabilistic forecasting](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/uncertainty_quantification.html) | **Direct · Colab notebook** | Trains LSTM and N-HiTS models to emit prediction intervals. This is more appropriate than point-price prediction when the target is future range, realized variance, or tail risk. |
| [Statsmodels Markov-switching autoregression notebook](https://www.statsmodels.org/devel/examples/notebooks/generated/markov_autoregression.html) | **Direct · notebook** | A tested implementation of Hamilton-style latent regimes. It can be adapted to returns, absolute returns, realized volatility, volume shocks, or a multifeature state definition. |
| [Ruptures basic change-point detection](https://centre-borelli.github.io/ruptures-docs/getting-started/basic-usage/) and [GitHub repository](https://github.com/deepcharles/ruptures) | **Direct · code-first** | Offline segmentation of nonstationary signals with dynamic programming, PELT, binary segmentation, window methods, and several cost functions. This supports a different school of thought: identify structural changes first instead of assuming one model is stable through the whole sample. |

## Focused executable notebooks and scientific tools

### Statistical properties, stationarity, and simple predictive structure

| Resource | Fit | Concrete use |
|---|---|---|
| [Quantopian: hypothesis testing](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Hypothesis_Testing/notebook.ipynb) | **Direct · notebook** | Builds the basic test-statistic/p-value machinery needed to test a proposed return, volume, volatility, or conditional-return effect. |
| [Quantopian: integration, cointegration, and stationarity](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Integration_Cointegration_and_Stationarity/notebook.ipynb) | **Direct/More data · notebook** | ADF-style stationarity work for price versus returns; cointegration becomes relevant when BTC is paired with spot, another exchange, a dated future, ETH, or a sector proxy. |
| [Quantopian: autocorrelation and AR models](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Autocorrelation_and_AR_Models/notebook.ipynb) | **Direct · notebook** | ACF/PACF, autoregressive fitting, and the relationship between serial correlation and forecastability. Apply separately to signed returns, squared returns, absolute returns, ranges, and volume changes. |
| [Quantopian: model misspecification](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Model_Misspecification/notebook.ipynb) | **Direct · notebook** | Shows what it means for a regression to be wrong even when coefficients look significant. Useful for detecting omitted nonlinearities, changing variance, and invalid residual assumptions. |
| [Quantopian: residual analysis](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Residuals_Analysis/notebook.ipynb) | **Direct · notebook** | Turns model residuals into a diagnostic object. A model that leaves predictable autocorrelation or volatility structure has not extracted all available structure. |
| [Statsmodels time-series analysis reference](https://www.statsmodels.org/stable/tsa.html) | **Direct · official reference** | ACF/PACF, ADF/KPSS, Ljung-Box, BDS nonlinearity testing, ARIMA, VAR/VECM, filters, state-space models, and regime switching in one maintained library. |
| [Scikit-learn: visualizing cross-validation behavior](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html) | **Direct · downloadable notebook** | Makes the indices in `TimeSeriesSplit`, K-fold, and grouped splits visible. Use it to inspect that training timestamps always precede test timestamps and that a gap exists when labels overlap. |
| [Forecasting: rolling-origin time-series cross-validation](https://otexts.com/fpp3/tscv.html) | **Direct · academic text/code** | A precise explanation of expanding and fixed rolling windows for one-step and multi-step evaluation. The examples are R, but the evaluation logic maps directly to Python. |

### Volatility, range, and uncertainty

| Resource | Fit | Concrete use |
|---|---|---|
| [Quantopian: ARCH, GARCH, and GMM](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/ARCH_GARCH_and_GMM/notebook.ipynb) | **Direct · notebook** | A gentler notebook introduction to conditional heteroskedasticity before using the more complete `arch` package. |
| [HAR-RV Python notebook](https://github.com/deep-hedger-Peng/HAR-RV) | **Adapt · notebook** | A compact implementation of Corsi’s heterogeneous autoregressive realized-volatility model. The example forecasts SPY daily RV; replace its RV construction with sums of squared BTC intraday log returns and define the desired forecast horizon. |
| [MAPIE EnbPI time-series example](https://contrib.scikit-learn.org/MAPIE/1.4.0/generated/regression/2-advanced-analysis/plot_timeseries_enbpi/) | **Direct · notebook** | Wraps a fitted regression model with sequential conformal prediction intervals and updates calibration scores through time. Useful when interval coverage matters more than a single point estimate. |
| [Conformal Prediction Interval for Dynamic Time Series — official code](https://github.com/hamrel-cxu/EnbPI) | **Direct · paper code** | Reproduces the EnbPI experiments and supplies the original implementation behind distribution-free sequential prediction intervals. |
| [Scikit-learn quantile regression example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html) | **Direct · downloadable notebook** | Predicts conditional quantiles instead of only a mean. Adapt it to future maximum adverse move, high-low range, absolute return, or realized variance. |
| [NeuralForecast robust forecasting notebook](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/robust_forecasting.html) | **Direct · Colab notebook** | Huber and multi-quantile losses plus dropout for noisy and outlier-heavy time series. This is a concrete alternative to deleting crypto spikes as “bad data.” |

### Regimes, state space, and time-frequency structure

| Resource | Fit | Concrete use |
|---|---|---|
| [Quantopian: Kalman filters](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Kalman_Filters/notebook.ipynb) | **Direct/More data · notebook** | Recursive latent-state estimation for changing means, hedge ratios, trends, and spreads. It provides a continuous-state alternative to discrete Markov regimes. |
| [Statsmodels state-space models](https://www.statsmodels.org/stable/statespace.html) | **Direct · official reference** | Kalman filtering, local-level/local-trend models, dynamic regression, structural components, and maximum-likelihood estimation. |
| [Statsmodels seasonal/state-space notebook](https://www.statsmodels.org/stable/examples/notebooks/generated/statespace_seasonal.html) | **Direct · notebook** | Shows how to represent more than one periodic component. For BTC, this is directly relevant to minute-of-hour, hour-of-day, UTC-day, weekday/weekend, and funding-cycle effects. |
| [SciPy periodogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html) | **Direct · scientific example** | Power-spectral-density estimation for checking stable periodic structure. Apply to volatility, volume, spread proxies, or signed returns; price levels will usually produce misleading low-frequency power. |
| [PyWavelets continuous wavelet transform](https://pywavelets.readthedocs.io/en/latest/ref/cwt.html) | **Direct · scientific examples** | A time-localized frequency representation. Unlike one global FFT, it can reveal whether a cycle exists only in particular regimes. Use this as a feature-extraction experiment, not proof of a tradable cycle. |
| [PyWavelets usage examples](https://pywavelets.readthedocs.io/en/latest/regression/) | **Direct · code-first** | DWT, stationary wavelet transform, multilevel decompositions, boundary modes, and reconstruction examples. Boundary handling is especially important when computing rolling, no-lookahead features. |

### ML, deep learning, and symbolic search

| Resource | Fit | Concrete use |
|---|---|---|
| [Qlib workflow notebook](https://github.com/microsoft/qlib/blob/main/examples/workflow_by_code.ipynb) | **Adapt · Jupyter notebook** | End-to-end data/model/record/backtest/report wiring. Best viewed as an example of reproducible experiment structure; its default Alpha158 equity setup must be replaced for BTC. |
| [Qlib model zoo](https://github.com/microsoft/qlib/tree/main/examples/benchmarks) | **Adapt · runnable configs** | Comparable configs for LightGBM, XGBoost, CatBoost, PyTorch MLP/LSTM/GRU/ALSTM, transformers, and other models. This makes model-class comparison cleaner than unrelated one-off notebooks. |
| [PyTorch Forecasting tutorials](https://pytorch-forecasting.readthedocs.io/en/v1.4.0/tutorials.html) | **Direct · notebooks** | N-BEATS, DeepAR/DeepVAR, N-HiTS, Temporal Fusion Transformer, quantiles, custom models, and metrics. The library is higher-level than raw PyTorch and useful after a linear/tree baseline exists. |
| [NeuralForecast model repository](https://github.com/Nixtla/neuralforecast) | **Direct · maintained code/notebooks** | One interface for MLP, RNN, LSTM, GRU, TCN, N-BEATS, N-HiTS, DeepAR, TFT, PatchTST, iTransformer, and other architectures. Useful for model comparison, not for declaring the newest architecture the winner from one split. |
| [Scikit-learn permutation feature importance](https://scikit-learn.org/stable/modules/permutation_importance.html) | **Direct · official example** | Measures out-of-sample loss degradation after a feature is shuffled. For time series, compute it only inside an untouched future block and consider block permutations so serial structure is not destroyed unrealistically. |
| [gplearn symbolic-transformer example](https://gplearn.readthedocs.io/en/stable/examples.html#symbolic-transformer) | **Direct · code example** | Evolves explicit nonlinear formulas as new features. It is a transparent alternative to a neural black box, but it creates a severe multiple-testing problem and therefore belongs next to SPA/DSR/PBO tests. |
| [DEAP symbolic-regression example](https://deap.readthedocs.io/en/master/examples/gp_symbreg.html) | **Direct · code example** | A lower-level genetic-programming implementation where primitives, fitness, mutation, crossover, tree depth, and complexity penalties are explicit. Useful for experimenting with evolved trading rules without hiding the search process. |
| [DeepLOB paper repository and Jupyter notebooks](https://github.com/zcakhaa/DeepLOB-Deep-Convolutional-Neural-Networks-for-Limit-Order-Books) | **More data · PyTorch/TensorFlow notebooks** | The canonical CNN+LSTM order-book model implementation. It is deliberately listed as a boundary: it cannot be reproduced honestly from 1-minute OHLCV; it becomes relevant only after acquiring synchronized depth-of-book data. |

### Sampling, labeling, costs, and backtesting

| Resource | Fit | Concrete use |
|---|---|---|
| [Mlfin.py financial data structures](https://mlfinpy.readthedocs.io/en/latest/FinancialDataStructure.html) | **More data · code-first** | Time, tick, volume, dollar, imbalance, and run bars. True alternative bars require underlying trades; a 1-minute OHLCV file cannot reconstruct their within-minute ordering. |
| [Mlfin.py CUSUM filtering](https://mlfinpy.readthedocs.io/en/latest/Filtering.html) | **Direct · code-first** | Event sampling based on accumulated deviations instead of labeling every minute. This creates a different dataset rather than another indicator on the same fixed clock. |
| [Purged and combinatorial cross-validation notebook](https://github.com/hudson-and-thames/example-notebooks/blob/main/Cross_validation/Chapter7_Cross_Validation.ipynb) | **Direct · notebook** | Purging and embargo for overlapping financial labels, plus finance-specific CV concepts. Particularly relevant when a sample at time `t` uses a future window extending several bars. |
| [purgedcv: scikit-learn-compatible implementation](https://github.com/eslazarev/purged-cross-validation) | **Direct · code/tests** | Maintained implementation of purged K-fold, grouped purging, walk-forward splits, combinatorial purged CV, reconstructed paths, probabilistic Sharpe, and deflated Sharpe. |
| [VectorBT portfolio API](https://vectorbt.dev/api/portfolio/base/) | **Direct · official examples** | Explicit order/trade/position records, fees, equity curves, and drawdowns. Inspect the assumed execution price for every signal; bar-close knowledge cannot receive the same bar’s close fill. |
| [Quantopian: volume, slippage, and liquidity](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Introduction_to_Volume_Slippage_and_Liquidity/notebook.ipynb) | **Adapt · notebook** | Introduces volume participation, slippage, and capacity. The equity examples must be replaced with exchange-specific BTC fees, bid-ask spreads, funding, and observed fill behavior. |
| [Quantopian: market-impact model](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Market_Impact_Model/notebook.ipynb) | **Adapt · notebook** | Makes the relationship between trade size, volume, volatility, and execution loss quantitative. Useful even if the first BTC research account is small because it prevents assuming unlimited scalability. |
| [Quantopian: futures trading considerations](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Futures_Trading_Considerations/notebook.ipynb) | **Adapt · notebook** | Contract mechanics, continuous-series issues, leverage, margin, and roll considerations. For crypto perpetuals, add funding, mark/index prices, liquidation rules, and exchange-specific fees. |

## Foundational papers by school of thought

### 1. Test whether price history contains directional structure

1. [Lo and MacKinlay — *Stock Market Prices Do Not Follow Random Walks*](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/8705.pdf) — **Paper · Adapt.** Introduces the variance-ratio test: compare variance across sampling horizons under the random-walk null. The original horizon is weekly equities; the test logic can be applied across 1, 5, 15, 30, and 60-minute BTC returns with heteroskedasticity-robust inference.

2. [Brock, Lakonishok, and LeBaron — *Simple Technical Trading Rules and the Stochastic Properties of Stock Returns*](https://finance.martinsewell.com/stylized-facts/dependence/BrockLakonishokLeBaron1992.pdf) — **Paper · Adapt.** A foundational scientific treatment of moving-average and trading-range-break rules using bootstrap null models. Read it for the experimental method, not because its century of DJIA data proves a BTC rule.

3. [Moskowitz, Ooi, and Pedersen — *Time Series Momentum*](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf) — **Paper · Adapt.** Defines a clean futures trend strategy using an instrument’s own past excess return and volatility-scaled positions across 58 contracts. Its evidence is medium-horizon, not 1-minute, but the signal definition and risk normalization are foundational.

4. [Hurst, Ooi, and Pedersen — *A Century of Evidence on Trend-Following Investing*](https://fairmodel.econ.yale.edu/ec439/hurst.pdf) — **Paper · Adapt.** A long out-of-sample extension of time-series momentum across futures markets. It is valuable as robustness evidence across eras, not an intraday parameter recommendation.

5. [Liu and Tsyvinski — *Risks and Returns of Cryptocurrency*](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf) — **Paper · Direct concept/horizon mismatch.** Finds crypto-specific time-series momentum and investor-attention predictors at daily and weekly frequencies. It is one of the highest-quality empirical starting points specific to crypto returns.

6. [Allen and Karjalainen — *Using Genetic Algorithms to Find Technical Trading Rules*](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9320.pdf) — **Paper · Adapt.** Early genetic-programming search over trading rules with honest out-of-sample tests and transaction costs. Its largely negative excess-return result is exactly why it is useful: evolutionary search can discover regime/volatility timing while still failing to produce net alpha.

7. [Neely and Weller — *Intraday Technical Trading in the Foreign Exchange Market*](https://wrap.warwick.ac.uk/id/eprint/1846/1/WRAP_Neely_fwp99-02.pdf) — **Paper · Adapt.** Compares genetic-program and optimized linear trading rules on intraday FX. It is closer to 1-minute BTC than daily genetic studies and provides a disciplined historical example of automated rule search.

### 2. Forecast volatility rather than direction

1. [Engle — *Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of U.K. Inflation*](https://www.econ.uiuc.edu/~econ536/Papers/engle82.pdf) — **Paper · Direct.** The original ARCH paper: conditional variance depends on lagged squared innovations. This is the conceptual base for volatility clustering models.

2. [Bollerslev — *Generalized Autoregressive Conditional Heteroskedasticity*](https://public.econ.duke.edu/~boller/Published_Papers/joe_86.pdf) — **Paper · Direct.** Extends ARCH so conditional variance depends on both past squared shocks and past conditional variance. GARCH(1,1) is the mandatory statistical baseline before neural volatility models.

3. [Andersen, Bollerslev, Diebold, and Labys — *Modeling and Forecasting Realized Volatility*](https://www.nber.org/system/files/working_papers/w8160/w8160.pdf) — **Paper · Direct.** Shows how intraday returns construct ex-post realized volatility and how that measure can be modeled and forecast. One-minute data is especially suitable for building higher-horizon realized-variance targets, subject to microstructure noise.

4. [Corsi — *A Simple Approximate Long-Memory Model of Realized Volatility*](https://statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/Corsi2009JFinEtrics_LMmodelRealizedVola.pdf) — **Paper · Direct.** Introduces HAR-RV: daily, weekly, and monthly realized-volatility components in a simple linear model. It is interpretable, easy to estimate, and a strong benchmark for any ML volatility predictor.

5. [Parkinson — *The Extreme Value Method for Estimating the Variance of the Rate of Return*](https://www-2.rotman.utoronto.ca/~kan/3032/pdf/FinancialAssetReturns/Parkinson_JB_1980.pdf) — **Paper · Direct.** A high-low range volatility estimator that extracts more information than close-to-close squared returns under its assumptions. Directly usable with OHLC.

6. [Garman and Klass — *On the Estimation of Security Price Volatilities from Historical Data*](https://www-2.rotman.utoronto.ca/~kan/3032/pdf/FinancialAssetReturns/Garman_Klass_JB_1980.pdf) — **Paper · Direct.** Combines open, high, low, and close into a more efficient range-based variance estimator. Compare it against close-to-close, Parkinson, Rogers-Satchell, and realized variance rather than choosing it by reputation.

7. [Corwin and Schultz — *A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices*](https://users.nber.org/~confer/2009/mms09/Corwin_Schultz.pdf) — **Paper · Adapt.** Infers a spread component from high-low behavior over adjacent intervals. It was designed for daily equity data; on BTC it is best treated as a candidate liquidity/spread proxy and validated against actual quote spreads when available.

8. [Xu and Xie — *Conformal Prediction Interval for Dynamic Time Series*](https://proceedings.mlr.press/v139/xu21h/xu21h.pdf) — **Paper · Direct.** Distribution-free sequential prediction intervals around any bootstrap ensemble estimator. Useful for calibrated future-volatility or range bands without assuming Gaussian forecast errors.

### 3. Model changing regimes instead of one stationary process

1. [Hamilton — *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*](https://www.ssc.wisc.edu/~bhansen/718/Hamilton1989.pdf) — **Paper · Direct concept.** The foundational Markov-switching autoregression: model parameters depend on an unobserved discrete state inferred probabilistically from the data.

2. [Truong, Oudre, and Vayatis — *Ruptures: Change Point Detection in Python*](https://arxiv.org/abs/1801.00826) — **Paper/code · Direct.** Algorithms and software for segmenting a nonstationary series where means, variances, trends, or distributions change. This is useful when the goal is to discover when a predictor stops working rather than average its performance across incompatible regimes.

3. [Quantopian: instability of estimates](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Instability_of_Estimates/notebook.ipynb) — **Notebook · Direct.** Demonstrates that estimated means, variances, correlations, and betas move through time. It provides a concrete reason to inspect rolling coefficients instead of reporting only full-sample estimates.

### 4. Relative value, hedged signals, and multivariate structure

1. [Engle and Granger — *Co-Integration and Error Correction: Representation, Estimation, and Testing*](https://users.ssc.wisc.edu/~behansen/718/EngleGranger1987.pdf) — **Paper · More data.** The foundation for testing whether nonstationary price series share a stable long-run combination and for modeling deviations with an error-correction term.

2. [Gatev, Goetzmann, and Rouwenhorst — *Pairs Trading: Performance of a Relative-Value Arbitrage Rule*](https://stat.wharton.upenn.edu/~steele/Courses/434/434Context/PairsTrading/PairsTradingGGR.pdf) — **Paper · More data.** A simple distance-based formation and trading rule with bootstrap analysis and transaction costs. Adaptable to BTC spot versus futures, exchange pairs, BTC/ETH structures, or coin-versus-SOL residuals.

3. [Avellaneda and Lee — *Statistical Arbitrage in the U.S. Equities Market*](https://traders.berkeley.edu/papers/Statistical%20arbitrage%20in%20the%20US%20equities%20market.pdf) — **Paper · More data.** Uses PCA or sector-factor regression to remove common movement, then models residuals as mean-reverting processes. This is the core reference for discovering hedged residual alpha across a crypto universe rather than predicting every coin outright.

4. [Statsmodels VAR/VECM documentation](https://www.statsmodels.org/devel/vector_ar.html) — **Code-first reference · More data.** Vector autoregression, Granger causality, impulse responses, cointegration rank tests, and vector error-correction models for BTC plus spot/futures/funding/other assets.

### 5. Crypto futures, carry, funding, and derivative-specific signals

1. [Ackerer, Hugonnier, and Jermann — *Perpetual Futures Pricing*](https://finance.wharton.upenn.edu/~jermann/AHJ-main-10.pdf) — **Paper · More data.** Derives no-arbitrage pricing for linear, inverse, and quanto perpetual futures and formalizes the funding mechanism that anchors perp to spot. This is foundational before treating funding as a predictor or carry return.

2. [He, Manela, Ross, and von Wachter — *Fundamentals of Perpetual Futures*](https://arxiv.org/abs/2212.06888) — **Paper · More data.** Studies the contract mechanics and funding design of crypto perpetuals. Useful for defining P&L correctly and separating directional return from funding and basis convergence.

3. [Schmeling, Schrimpf, and Todorov — *Crypto Carry*](https://www.bis.org/publ/work1087.pdf) — **Institutional paper · More data.** Empirical study of BTC/ETH spot, futures basis, volume, open interest, and options characteristics across exchanges. It opens a carry/basis school of research that OHLCV alone cannot represent.

4. [Liu, Tsyvinski, and Wu — *Common Risk Factors in Cryptocurrency*](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf) — **Paper · More assets.** Builds crypto market, size, momentum, volume, and volatility factors across a large coin universe. Relevant once research expands beyond one BTC series into cross-sectional ranking and hedged factor portfolios.

### 6. Machine learning that is specific enough to reproduce

1. [Dixon, Klabjan, and Bang — *Classification-Based Financial Markets Prediction Using Deep Neural Networks*](https://arxiv.org/pdf/1603.08604) — **Paper · Adapt.** Predicts direction classes for 43 commodity and FX futures at five-minute intervals and specifies network/training/backtest choices. It is an early, concrete finance DNN baseline rather than a generic “use an LSTM” claim.

2. [Oreshkin et al. — *N-BEATS: Neural Basis Expansion Analysis for Interpretable Time Series Forecasting*](https://arxiv.org/abs/1905.10437) and [official repository](https://github.com/servicenow/n-beats) — **Paper/code · Direct.** A univariate deep forecasting model built from fully connected residual blocks, with an interpretable trend/seasonality version. Suitable for testing nonlinear forecasts of volatility or range against HAR/GARCH.

3. [Lim et al. — *Temporal Fusion Transformers for Interpretable Multi-Horizon Time-Series Forecasting*](https://arxiv.org/abs/1912.09363) — **Paper · Direct/More features.** A multi-horizon model with gating, variable selection, recurrent local processing, and attention. It becomes most justified when the dataset includes many known and observed covariates, not only one close-price sequence.

4. [Zhang, Zohren, and Roberts — *DeepLOB*](https://arxiv.org/pdf/1808.03668) — **Paper · More data.** A CNN+LSTM model for limit-order-book prediction. Read it to understand the next data tier after OHLCV and why genuine high-frequency prediction normally uses order flow and book state.

### 7. Prove that a result survived the search process

1. [White — *A Reality Check for Data Snooping*](https://www.ssc.wisc.edu/~bhansen/718/White2000.pdf) — **Paper · Direct.** The foundational bootstrap test for whether the best rule among many searched rules actually outperforms a benchmark after data snooping.

2. [Hansen — *A Test for Superior Predictive Ability*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=264569) — **Paper · Direct.** A more powerful and less irrelevant-model-sensitive successor to White’s Reality Check. The executable implementation is in the `arch` multiple-comparisons notebook above.

3. [Bailey et al. — *The Probability of Backtest Overfitting*](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf) — **Paper · Direct.** Defines combinatorially symmetric cross-validation and a probability that selecting the best backtest has overfit the historical path.

4. [Bailey and López de Prado — *The Deflated Sharpe Ratio*](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf) — **Paper · Direct.** Adjusts a reported Sharpe for multiple trials, non-normal returns, skewness, kurtosis, and sample uncertainty. Keep the number of attempted variants; without the trial count, deflation cannot be honest.

5. [Quantopian: the dangers of overfitting](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/The_Dangers_of_Overfitting/notebook.ipynb) — **Notebook · Direct.** Visual and executable examples of why increasing strategy flexibility improves in-sample fit while damaging future performance.

6. [Quantopian: p-hacking and multiple-comparisons bias](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/p-Hacking_and_Multiple_Comparisons_Bias/notebook.ipynb) — **Notebook · Direct.** Shows why testing many lags, thresholds, features, horizons, assets, and model seeds creates apparently significant discoveries by chance.

### 8. Execution and the difference between forecast edge and tradable edge

1. [Almgren and Chriss — *Optimal Execution of Portfolio Transactions*](https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf) — **Paper · Adapt.** Separates temporary impact, permanent impact, price risk, and schedule choice. The institutional order-size assumptions may not fit a small BTC strategy, but the cost/risk decomposition is foundational.

2. [Amihud — *Illiquidity and Stock Returns*](https://www.cis.upenn.edu/~mkearns/finread/amihud.pdf) — **Paper · Adapt.** Defines a simple price-impact/illiquidity proxy from absolute return divided by dollar volume. It is directly constructible from OHLCV as a feature, but exchange-specific validation is required.

## Useful source combinations

These combinations are links to existing material, not a new research framework.

| Question | Sources that directly address it |
|---|---|
| “Are BTC returns serially predictable at any horizon?” | [Lo–MacKinlay](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/8705.pdf), [Quantopian AR notebook](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Autocorrelation_and_AR_Models/notebook.ipynb), [statsmodels TSA](https://www.statsmodels.org/stable/tsa.html) |
| “Can I build a simple volatility predictor from 1-minute bars?” | [Andersen et al.](https://www.nber.org/system/files/working_papers/w8160/w8160.pdf), [Corsi HAR-RV](https://statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/Corsi2009JFinEtrics_LMmodelRealizedVola.pdf), [HAR-RV notebook](https://github.com/deep-hedger-Peng/HAR-RV), [ARCH forecasting](https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_forecasting.html) |
| “Can OHLC ranges predict future volatility better than close returns?” | [Parkinson](https://www-2.rotman.utoronto.ca/~kan/3032/pdf/FinancialAssetReturns/Parkinson_JB_1980.pdf), [Garman–Klass](https://www-2.rotman.utoronto.ca/~kan/3032/pdf/FinancialAssetReturns/Garman_Klass_JB_1980.pdf), [scikit lagged-feature notebook](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html) |
| “Does a rule work only in certain states?” | [Hamilton](https://www.ssc.wisc.edu/~bhansen/718/Hamilton1989.pdf), [statsmodels Markov notebook](https://www.statsmodels.org/devel/examples/notebooks/generated/markov_autoregression.html), [Ruptures](https://github.com/deepcharles/ruptures), [estimate-instability notebook](https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Instability_of_Estimates/notebook.ipynb) |
| “Can a tree model beat linear/GARCH baselines?” | [scikit lagged-feature notebook](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html), [permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html), [time-series CV](https://otexts.com/fpp3/tscv.html), [ARCH SPA test](https://arch.readthedocs.io/en/stable/multiple-comparison/multiple-comparison_examples.html) |
| “Can a small PyTorch model add nonlinear predictive power?” | [official PyTorch LSTM example](https://github.com/pytorch/examples/tree/main/time_sequence_prediction), [NeuralForecast walkthrough](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/getting_started_complete.html), [Dixon et al.](https://arxiv.org/pdf/1603.08604), [N-BEATS](https://arxiv.org/abs/1905.10437) |
| “Can automated search discover formulas instead of fixed indicators?” | [gplearn](https://gplearn.readthedocs.io/en/stable/examples.html#symbolic-transformer), [DEAP](https://deap.readthedocs.io/en/master/examples/gp_symbreg.html), [Allen–Karjalainen](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9320.pdf), [Deflated Sharpe](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf) |
| “What becomes possible after adding futures and funding data?” | [Perpetual Futures Pricing](https://finance.wharton.upenn.edu/~jermann/AHJ-main-10.pdf), [Fundamentals of Perpetual Futures](https://arxiv.org/abs/2212.06888), [Crypto Carry](https://www.bis.org/publ/work1087.pdf), [Engle–Granger](https://users.ssc.wisc.edu/~behansen/718/EngleGranger1987.pdf) |
| “How do I know the best backtest was not just the luckiest?” | [White Reality Check](https://www.ssc.wisc.edu/~bhansen/718/White2000.pdf), [Hansen SPA](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=264569), [PBO](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf), [DSR](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf), [executable SPA notebook](https://arch.readthedocs.io/en/stable/multiple-comparison/multiple-comparison_examples.html) |

## Important scope boundaries in the sources

- One-minute OHLCV supports return, range, volatility, volume, seasonality, change-point, and bar-level liquidity-proxy research.
- It does **not** reveal trade direction, bid/ask quotes, queue position, order-book imbalance, liquidations, open interest, funding, spot/perp basis, or exact intrabar path.
- A bar-level backtest cannot know whether the high or low occurred first. Any strategy using both intrabar stop and target levels needs tick data or an explicit adverse ordering assumption.
- Papers using daily or monthly horizons are included for their definitions and testing methods. Their reported parameter values are not direct recommendations for one-minute BTC.
- The strongest negative papers are intentionally included. A method that failed honest out-of-sample testing is often more educational than a notebook that reports one unexplained profitable curve.
