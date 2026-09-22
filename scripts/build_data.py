"""
Builds data/processed/dataset.json from raw AQR factor files and
yfinance-derived equity index prices.

Run: python3 scripts/build_data.py
"""
import json
import csv
import datetime as dt
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "dataset.json"


def month_key(d):
    return f"{d.year:04d}-{d.month:02d}"


def parse_momentum(path):
    """AQR Momentum Indices, Monthly -> U.S. Large Cap column."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Returns"]
    rows = list(ws.iter_rows(values_only=True))
    out = {}
    for row in rows[2:]:
        date, us_lc = row[0], row[1]
        if date is None or us_lc is None:
            continue
        out[month_key(date)] = float(us_lc)
    return out


def parse_country_factor(path, sheet, country="USA"):
    """AQR HML Devil / BAB / QMJ files share the same layout:
    header row has DATE + ISO3 country codes + aggregates, data starts next row."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    header = None
    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0] == "DATE":
            header = row
            header_idx = i
            break
    col = header.index(country)
    out = {}
    for row in rows[header_idx + 1:]:
        date_val = row[0]
        if not date_val:
            continue
        val = row[col]
        if val is None:
            continue
        if isinstance(date_val, dt.datetime):
            date = date_val
        else:
            date = dt.datetime.strptime(str(date_val), "%m/%d/%Y")
        out[month_key(date)] = float(val)
    return out


def parse_price_csv(path):
    """Monthly price level CSV (from yfinance) -> monthly simple return series."""
    dates, prices = [], []
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            if not row or not row[0] or row[0] == "Date":
                continue
            try:
                d = dt.datetime.strptime(row[0][:10], "%Y-%m-%d")
                p = float(row[1])
            except (ValueError, IndexError):
                continue
            dates.append(d)
            prices.append(p)
    out = {}
    for i in range(1, len(prices)):
        if prices[i - 1] == 0:
            continue
        ret = prices[i] / prices[i - 1] - 1
        out[month_key(dates[i])] = ret
    return out


def series_meta(data, label, category, source, note=""):
    keys = sorted(data.keys())
    return {
        "label": label,
        "category": category,
        "source": source,
        "note": note,
        "start": keys[0] if keys else None,
        "end": keys[-1] if keys else None,
        "data": data,
    }


def main():
    dataset = {
        "generated": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "series": {},
    }

    dataset["series"]["SPX"] = series_meta(
        parse_price_csv(RAW / "SPX_monthly_price.csv"),
        "US Large Cap (S&P 500)",
        "index",
        "Yahoo Finance (^GSPC), price return",
        "Price return only (dividends not reinvested); pre-1988 does not include dividend yield.",
    )
    dataset["series"]["EM"] = series_meta(
        parse_price_csv(RAW / "EM_monthly_price.csv"),
        "Emerging Markets (MSCI EM proxy)",
        "index",
        "Yahoo Finance (EEM ETF), dividend-adjusted",
        "iShares MSCI Emerging Markets ETF used as a liquid proxy for the MSCI EM index.",
    )
    dataset["series"]["EAFE"] = series_meta(
        parse_price_csv(RAW / "EAFE_monthly_price.csv"),
        "Developed ex-US (MSCI EAFE proxy)",
        "index",
        "Yahoo Finance (EFA ETF), dividend-adjusted",
        "iShares MSCI EAFE ETF used as a liquid proxy for the MSCI EAFE index.",
    )
    dataset["series"]["MOM"] = series_meta(
        parse_momentum(RAW / "momentum.xlsx"),
        "Momentum (US Large Cap)",
        "factor",
        "AQR Momentum Indices, Monthly",
        "Long-only momentum index return, not a long/short factor.",
    )
    dataset["series"]["VAL"] = series_meta(
        parse_country_factor(RAW / "hml-devil.xlsx", "HML Devil"),
        "Value (HML Devil, US)",
        "factor",
        "AQR: The Devil in HML's Details, Monthly",
        "Long/short self-financing excess return, US equities.",
    )
    dataset["series"]["BAB"] = series_meta(
        parse_country_factor(RAW / "bab.xlsx", "BAB Factors"),
        "Betting Against Beta (US)",
        "factor",
        "AQR: Betting Against Beta, Monthly",
        "Long/short self-financing excess return, US equities.",
    )
    dataset["series"]["QMJ"] = series_meta(
        parse_country_factor(RAW / "qmj.xlsx", "QMJ Factors"),
        "Quality Minus Junk (US)",
        "factor",
        "AQR: Quality Minus Junk, Monthly",
        "Long/short self-financing excess return, US equities.",
    )

    for key, s in dataset["series"].items():
        print(f"{key}: {s['start']} -> {s['end']} ({len(s['data'])} months)")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dataset, separators=(",", ":")))
    print(f"\nWrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
