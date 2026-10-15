"""
Downloads the daily source files into data/raw/daily (skips files already present).

Run: python3 scripts/fetch_daily.py

- Ken French F-F_Research_Data_Factors_daily (Mkt-RF, RF)
- AQR daily factor files: BAB, QMJ, HML Devil (large xlsx, git-ignored)
- Yahoo Finance daily adjusted closes: EEM, EFA, VBMFX

AQR does not publish a daily Momentum Indices file, so MOM stays monthly-only.
"""
import io
import urllib.request
import zipfile
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
DAILY = ROOT / "data" / "raw" / "daily"
DAILY.mkdir(parents=True, exist_ok=True)

FRENCH_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
AQR_BASE = "https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/"
AQR_FILES = {
    "bab-daily.xlsx": "Betting-Against-Beta-Equity-Factors-Daily.xlsx",
    "qmj-daily.xlsx": "Quality-Minus-Junk-Factors-Daily.xlsx",
    "hml-devil-daily.xlsx": "The-Devil-in-HMLs-Details-Factors-Daily.xlsx",
}
YAHOO = {"EEM_daily.csv": "EEM", "EFA_daily.csv": "EFA", "VBMFX_daily.csv": "VBMFX"}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return r.read()


def main():
    ff = DAILY / "F-F_Research_Data_Factors_daily.csv"
    if not ff.exists():
        with zipfile.ZipFile(io.BytesIO(fetch(FRENCH_URL))) as z:
            ff.write_bytes(z.read("F-F_Research_Data_Factors_daily.csv"))
        print("fetched", ff.name)

    for name, remote in AQR_FILES.items():
        path = DAILY / name
        if not path.exists():
            path.write_bytes(fetch(AQR_BASE + remote))
            print("fetched", name)

    for name, ticker in YAHOO.items():
        path = DAILY / name
        if not path.exists():
            df = yf.download(ticker, start="1986-01-01", interval="1d", auto_adjust=True, progress=False)
            df.columns = df.columns.get_level_values(0)
            df[["Close"]].rename(columns={"Close": ticker}).to_csv(path, index_label="Date")
            print("fetched", name, len(df), "rows")


if __name__ == "__main__":
    main()
