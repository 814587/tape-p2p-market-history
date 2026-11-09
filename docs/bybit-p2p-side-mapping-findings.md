Bybit P2P API — Side Parameter Verification

1. Overview

This document records findings from live testing of Bybit’s P2P advertisement system.

The purpose of this investigation was to establish the actual meaning of the API’s side parameter by comparing returned advertisement information against the public Bybit P2P interface.

The investigation identified a discrepancy between the side mapping presented in the API documentation and the behaviour observed during testing.

2. Verified Side Mapping

API parameter	P2P direction
side=0	Buy USDT
side=1	Sell USDT

The observed API side values correspond directly to the Buy and Sell directions displayed in the Bybit P2P interface.

3. Why This Mapping Was Established

The mapping was not determined by assumption or interpretation of the parameter names.

It was established through live API requests and independent comparison with the public P2P interface.

The investigation involved:

1. Querying the API using the different side values.
2. Examining the advertisement records returned by each request.
3. Comparing the returned information against advertisements displayed on the corresponding Bybit P2P interface.
4. Checking whether individual advertisement details could be identified in both sources.

This allowed the side mapping to be tested against actual displayed market advertisements.

4. Evidence A — Buy-side Verification

API results from the tested side were compared against the public Bybit P2P Buy USDT interface.

Two advertisements were identified through exact merchant-name and price matches.

Reference	API price	UI price	Result
Match A	₦1,382.99	₦1,382.99	Exact match
Match B	₦1,383.00	₦1,383.00	Exact match

The merchant identities have been anonymized in the published evidence image.

Why this matters:

Matching both the merchant names and their individual prices provides stronger verification than comparing general market prices alone.

It establishes that the advertisements returned by the tested API side were also present on the public Buy USDT interface.

Evidence image: evidence/bybit-buy-side-verification.png

5. Evidence B — Sell-side Verification

A separate test was conducted using the other API side.

The returned advertisement prices were compared against prices displayed on the public Bybit P2P Sell USDT interface.

This comparison produced matching price observations.

However, exact merchant-name matching was not established for this test.

Evidence limitation:

This is documented as a price-level observation rather than an exact advertisement identity verification.

Evidence image: evidence/bybit-sell-side-price-observation.png

6. Documentation Discrepancy

The mapping observed during live testing does not agree with the mapping presented in Bybit’s published API documentation.

This creates a potential problem for developers who rely exclusively on the published parameter descriptions.

An incorrectly interpreted side parameter can cause developers to:

* Retrieve the wrong P2P direction.
* Mislabel Buy and Sell advertisements.
* Interpret market prices incorrectly.
* Build applications that display the opposite market direction from what they intended.

The discrepancy deserves clarification in Bybit’s developer documentation.

The reason for the discrepancy has not been established.

7. Conclusion

Based on the live API tests and comparisons with the public Bybit P2P interface, the observed mapping is:

* side=0 — Buy USDT
* side=1 — Sell USDT

These findings are based on observed endpoint behaviour, not assumptions about parameter naming.

This documentation is published to help developers understand the tested behaviour and avoid incorrect interpretation of Bybit P2P market data.

Verification note: These findings represent observations made during testing on 9 November 2026. API behaviour and documentation may change, so independent revalidation is recommended.
