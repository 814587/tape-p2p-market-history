Bybit P2P Side Mapping: A Live Testing Finding

Background

Bybit’s published P2P API documentation describes the meaning of its Buy and Sell side parameters.

However, live testing and comparison with the public Bybit P2P interface revealed a discrepancy between the documented mapping and the actual observed behaviour.

Observed Side Mapping

The following mapping was verified through live testing:

Side value	Actual P2P direction
0	Buy USDT
1	Sell USDT

These values correspond to the Buy and Sell directions displayed in Bybit’s P2P interface.

Evidence

Buy-side verification

Two advertisements returned during testing were identified on the public Bybit P2P interface using matching merchant names and prices.

The published evidence image conceals merchant identities while preserving the matching prices and relevant interface details.

Sell-side verification

A separate comparison was conducted for the other side.

The API prices were observed and compared with prices displayed on the public P2P interface. This was a price-level observation rather than an exact merchant-identity match.

Documentation discrepancy

The observed live behaviour does not agree with the side mapping presented in Bybit’s published API documentation.

Developers relying exclusively on that documented mapping may interpret the returned P2P advertisements incorrectly.

The documentation should be reviewed and corrected to reflect the observed behaviour.

Conclusion

Live testing supports this mapping:

* 0 = Buy USDT
* 1 = Sell USDT

This finding is published to help developers understand the actual behaviour of Bybit’s P2P interface and avoid incorrect interpretations when working with P2P market data.

Note: This is an independently conducted technical observation. It does not establish why the documentation discrepancy exists.
