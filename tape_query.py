import sqlite3
from datetime import date, timedelta

DB = "bybit_p2p.db"


def get_history(token, days=None, start_date=None, end_date=None):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    token = token.upper()

    if end_date is None:
        end_date = date.today().isoformat()

    if start_date is None:
        if days:
            start = date.today() - timedelta(days=days - 1)
            start_date = start.isoformat()
        else:
            start_date = "1900-01-01"

    rows = conn.execute("""
        SELECT
            observation_date,
            token,
            session,
            buy_low,
            buy_high,
            sell_low,
            sell_high
        FROM observations
        WHERE token = ?
          AND observation_date BETWEEN ? AND ?
        ORDER BY observation_date DESC, id DESC
    """, (token, start_date, end_date)).fetchall()

    conn.close()
    return rows


def spread(row):
    return (
        row["buy_low"] - row["sell_high"],
        row["buy_high"] - row["sell_low"]
    )


def show_history(token, days=None, start_date=None, end_date=None):
    rows = get_history(token, days, start_date, end_date)

    if not rows:
        print(f"No observations found for {token.upper()}.")
        return

    print(f"{token.upper()} / NGN")
    print("=" * 45)

    for row in rows:
        low, high = spread(row)

        print(f"{row['observation_date']} — {row['session']}")
        print(
            f"Buy:  ₦{row['buy_low']:,.2f} – "
            f"₦{row['buy_high']:,.2f}"
        )
        print(
            f"Sell: ₦{row['sell_low']:,.2f} – "
            f"₦{row['sell_high']:,.2f}"
        )
        print(
            f"Spread: ₦{low:,.2f} – "
            f"₦{high:,.2f}"
        )
        print()


if __name__ == "__main__":
    show_history("USDT")
