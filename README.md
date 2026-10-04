TAPE — Bybit NGN P2P Market History

TAPE is an open-source market-observation project that turns Bybit NGN P2P listings into structured, queryable historical data.

Most P2P marketplaces show what is available right now, but they provide limited context about how prices, liquidity, trade limits, and payment methods have changed over time. TAPE addresses this gap by collecting repeated market snapshots and preserving them for later analysis.

The project is useful for anyone who wants to study NGN P2P market conditions, compare historical observations, inspect individual advertisements, or build tools on top of the collected data. It also provides a foundation for contributors interested in data collection, storage, analysis, and market-history visualization.

The project started from a simple question:

What has the P2P market actually been doing over the past few days?

Instead of relying only on current marketplace prices, TAPE records observations and makes them available for historical comparison.

What the project does

TAPE provides a small data pipeline for collecting, storing, and analyzing Bybit P2P market activity in NGN. Its main capabilities include:

* Collecting Bybit P2P advertisement data at defined points in time
* Supporting multiple assets, including USDT, BTC, and ETH
* Recording both Buy and Sell-side market observations
* Preserving individual advertisement details rather than storing only summary prices
* Capturing fields such as price, available quantity, minimum and maximum order amounts, and payment methods
* Storing market snapshots and advertisement records in SQLite
* Querying historical observations by asset, side, and date
* Comparing market ranges and other historical indicators
* Providing a foundation for dashboards, research tools, and further analysis

By preserving both snapshot-level and advertisement-level data, TAPE helps users move beyond a single current price and examine how market conditions change over time.

Technical Stack

* Python
* SQLite
* Requests
* Git / GitHub
* HTML / JavaScript for the presentation layer

Project Structure

tape-p2p-market-history/
│
├── tape_snapshot.py       # Collects and stores P2P market snapshots
├── tape_core.py           # Core observation and calculation logic
├── tape_query.py          # Queries historical observations
├── requirements.txt       # Python dependencies
│
└── experiments/
    ├── bybit_full_test.py # Early API investigation
    └── bybit_scraper.py   # Earlier scraper experiments

How it started

The project began as an investigation into how Bybit P2P market data could be collected programmatically.

Several approaches and endpoints were tested before arriving at the current collection approach. The experimental scripts are kept in the experiments/ directory to document that development process.

The current collector was then built around the data that could be successfully retrieved and stored.

Data Pipeline

Bybit P2P
    ↓
Data collection
    ↓
Response parsing
    ↓
SQLite storage
    ↓
Historical queries
    ↓
Market observations
    ↓
Dashboard / presentation

Current Status

TAPE is an experimental project and is still being developed.

It is intended for market observation and historical comparison, not price prediction or guaranteed trading results.

The project currently focuses on NGN P2P observations.

API / Data Access

The project uses an undocumented Bybit P2P data interface identified during the course of the investigation.

For security, maintenance, and responsible disclosure reasons, the exact endpoint details and request configuration are not documented here.

If you are interested in the technical implementation or the data collection approach, feel free to contact me.

Disclaimer

TAPE is an independent experimental project and is not affiliated with or endorsed by Bybit.

Market observations are historical data and should not be interpreted as financial advice or a guarantee of future prices.
