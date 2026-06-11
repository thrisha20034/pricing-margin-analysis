# Insights Summary — Pricing & Margin Analysis

## Executive Summary

This analysis examined pricing and discount patterns across the Superstore dataset to understand what drives margin variation across product categories. The key finding: discount depth above 20% consistently destroys margin without generating proportional revenue volume — particularly in the Furniture category.

---

## Finding 1 — Technology leads on margin; Furniture is loss-heavy

| Category | Avg Margin % |
|---|---|
| Technology | ~17% |
| Office Supplies | ~17% |
| Furniture | ~4% |

Furniture consistently underperforms. The Tables sub-category has negative average margins, meaning the business loses money on the majority of table sales.

---

## Finding 2 — Heavy discounting does not lift revenue meaningfully

Orders with discounts above 20% show an average margin of **-5.3%**, compared to **+18.7%** for undiscounted orders. Critically, order volume in the high-discount band does not compensate for this margin destruction — suggesting discounts in this range are unnecessary concessions rather than volume drivers.

**Implication:** A pricing rule capping discounts at 15–20% for Furniture and certain Technology sub-categories would recover significant margin with minimal revenue risk.

---

## Finding 3 — The worst offenders: Tables and Bookcases

Tables average a -8% margin across all orders. The problem is compounded by frequent high discounts (>30%) that appear to be applied without clear business justification.

Bookcases show a similar pattern at smaller scale.

**Recommendation:** Review the discount approval process for these sub-categories. Require margin floor sign-off before discounts above 20% are applied.

---

## Finding 4 — Copiers are resilient to discounting

Copiers maintain strong margins even at moderate discount levels (10–20%). This makes them a candidate for strategic promotions — unlike Tables, discounts here tend to be offset by high average selling prices.

---

## Finding 5 — Consumer segment most exposed to discount erosion

The Consumer segment drives the highest volume of high-discount orders and shows the lowest average margins among the three segments. Corporate and Home Office customers show better margin discipline.

---

## Recommended Actions

1. **Cap discounts on Tables and Bookcases at 15%** — recover estimated 4–6% margin improvement.
2. **Set a margin floor alert in the order system** — flag any order projected to fall below 5% margin before approval.
3. **Review Copier pricing strategy** — strong margins suggest room for selective premium pricing.
4. **Monitor the Consumer segment quarterly** — track whether discount concessions are converting to repeat purchase or one-off margin giveaways.
