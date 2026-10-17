# Equity Dashboard: Student Guide

Live site: https://dkann01.github.io/equity-dashboard/

The dashboard is built around one lesson: **mean returns are estimated very noisily; volatility is not.** Each tab answers one question and maps to one of the three Portfolio Analytics lectures.

## Defaults and conventions

Unless you change them: monthly data, **log** returns, **total** returns (not excess), annualized statistics, a 10-year rolling window, and the full date range. Every statistic is labeled annualized or monthly, log or simple, total or excess. Use **Load lecture example** (top of the page) to jump to a setup that matches a lecture.

- **Date range slider**: sets the sample for every tab.
- **Excess returns**: subtracts the 1-month T-bill rate from every series.
- **Monthly (not annualized) tiles**, **Simple returns**: switch the tile and moment statistics between annualized and monthly, and between log and simple returns. Geometric mean and max drawdown always use the compounded wealth path.
- **Predict first**: hides the Rolling and Return Pattern charts until you type a guess, then shows the answer next to it.
- EM (since 2003) and EAFE (since 2001) are short samples; their means are especially noisy.

## Tiles (top of the page)

Per series: arithmetic mean of log returns ±1.96 SE, geometric mean, vol ±1.96 SE, max drawdown, Sharpe ratio (always on excess returns), t-stat, and **Y\***, the years of data needed before the mean is statistically significant, (1.96 σ / μ)².

## Tabs

| Tab | Question it answers | Lecture topic |
|---|---|---|
| **Cumulative Growth** | How did each series compound over time, and how deep were the drawdowns? | Background |
| **Rolling Returns and Volatility** | At the same window, how wide is the confidence band for the mean versus the vol? Pick **Focus on one series** to see ±1.96 SE bands and the full-sample estimate (dashed). Drag the window from 1 month to 20 years. Below: rolling skewness and excess kurtosis against the band a normal sample would produce, with crises shaded. | Lecture 6 (SE of mean vs. SE of vol, years needed); Lecture 7 (Takeaway on kurtosis) |
| **Correlation** | How correlated are the series, and does correlation stay constant? The table uses the whole range; the rolling chart shows one pair over time with the first series' rolling vol underneath. | Lecture 7 (Fact 6: time-varying correlation) |
| **Return Pattern** | Are returns normal? Each series is standardized (z-scores) and compared with one N(0,1) curve; the tail table counts months beyond 2σ to 5σ against what a normal model predicts. Switch to weekly or daily to watch fat tails fade as the interval lengthens. | Lecture 7 (fat tails, aggregational normality, "Appeal for Normality") |
| **Autocorrelation** | Can yesterday's return predict today's? Bars show autocorrelation of r (inside the band) and of \|r\| (well above it and decaying slowly). | Lecture 7 (Facts 4 and 5: volatility clustering) |
| **Simulation** | If wealth grows at an estimated (μ, σ), what range of outcomes should I expect, and how much does a one-standard-error mistake in μ change the answer? Fan chart, outcome table, VaR/CVaR, shortfall versus the risk-free rate (simulated next to the closed form), max drawdown, Monte Carlo standard error. Tick **Show estimation risk in μ** to rerun at μ − 1.96 SE, μ̂, μ + 1.96 SE with the same random draws. | Lecture 8 (simulation table, "Cons": small errors in μ matter a lot); Lecture 6 (shortfall probabilities) |

## Things to try

1. Rolling tab, US Market, 10-year window: the mean's band is roughly ±10% a year, the vol's roughly ±2%. Shrink the window and watch the band widen.
2. Rolling tab at **Daily** frequency: the mean's band barely changes, the vol's shrinks about 4×. More observations help the vol; only more *years* help the mean.
3. Return Pattern: compare monthly with daily. Count the 4σ events against the normal's prediction.
4. Simulation: turn on estimation risk in μ and compare the three medians, then do the same for σ.

## Data

Monthly: Ken French (CRSP market, T-bill), AQR (Momentum, Value, BAB, QMJ), Yahoo Finance (EEM, EFA, VBMFX). Daily: French, AQR (no daily Momentum exists), Yahoo. US Bonds is VBMFX, a fund, so its returns are net of a small expense ratio. See the Sources section at the bottom of the page.
