import sqlite3

DB = "bybit_p2p.db"


def get_observation(token, date=None, session=None):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM observations
        WHERE token = ?
    """
    params = [token.upper()]

    if date:
        query += " AND observation_date = ?"
        params.append(date)

    if session:
        query += " AND session = ?"
        params.append(session)

    query += " ORDER BY observation_date DESC, id DESC LIMIT 1"

    row = conn.execute(query, params).fetchone()
    conn.close()

    return row


def calculate_spread(row):
    if not row:
        return None

    buy_low = row["buy_low"]
    buy_high = row["buy_high"]
    sell_low = row["sell_low"]
    sell_high = row["sell_high"]

    if None in (buy_low, buy_high, sell_low, sell_high):
        return None

    gap_low = buy_low - sell_high
    gap_high = buy_high - sell_low

    return {
        "gap_low": gap_low,
        "gap_high": gap_high
    }


def format_observation(token, row):
    if not row:
        return f"No {token.upper()} observation recorded."

    result = calculate_spread(row)

    msg = (
        f"{token.upper()} / {row['currency']} — {row['session']}\n\n"
        f"Buy:  {row['buy_low']:,.2f} – {row['buy_high']:,.2f}\n"
        f"Sell: {row['sell_low']:,.2f} – {row['sell_high']:,.2f}\n"
    )

    if result:
        msg += (
            f"\nObserved spread:\n"
            f"{result['gap_low']:,.2f} – {result['gap_high']:,.2f}"
        )

    return msg


if __name__ == "__main__":
    for token in ("BTC", "ETH", "USDT"):
        row = get_observation(token)
        print("=" * 40)
        print(format_observation(token, row))
