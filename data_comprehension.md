# Data Comprehension

There are a total of 5 CSV files to consider:
- **commodity_market.csv**
    - Weekly global commodity prices (oil, gas, steel, wheat, copper) and a combined `commodity_stress_index` from 2015 - 2026. Gives the economic backdrop that pushes up fuel and freight costs.
- **country_metadata.csv**
    - One row for each of the 10 countries: region, income group, GDP, trade dependency, port capacity and logistics performance. Shows how exposed or resilient each country on a route is.
- **geopolitical_events.csv**
    - About 10k dated events (strikes, sanctions, conflicts, cyber attacks) with severity, affected region, duration and `risk_increase`. Includes 3 major shocks: COVID, the Russia-Ukraine war and the Red Sea crisis. These are outside risk drivers and possible early warning signals.
- **trade_routes.csv**
    - Lookup table for the 50 routes (`route_id`): origin and destination country, distance, shipping method, cargo type and planned transit days. It links the operations data to the countries.
- **weekly_route_operations.csv**
    - Contains 31,300 rows, one per route per week (50 routes * 626 weeks). It has volume, delay, cost, congestion, weather and geopolitical risk scores, emissions, and the target `route_status` (Normal / Delayed / Disrupted). This is what we train the prediction model on.
## Data Merge Summary (TL;DR)

Full details are in `notebooks/data_preparation.ipynb`. The result is saved to `data/preprocessed/supply_chain_disruption.csv` (31,300 rows, 48 columns).

**Base file:** `weekly_route_operations.csv`. Every other file is joined onto it, so the output keeps one row per route per week.

1. **Route and country details**
    - Joined `trade_routes.csv` on `route_id` to add each route's origin, destination, distance, shipping method and cargo type.
    - Joined `country_metadata.csv` twice, once for the origin country and once for the destination country (`origin_` / `destination_` columns).

2. **Commodity prices**
    - Joined `commodity_market.csv` on `date`.
    - `fuel_cost_index` and `commodity_price_index` already match `oil_price` and `commodity_stress_index`, so only the 4 new prices were added (gas, steel, wheat, copper).
    - **Watch out:** the last 30 weeks (from 2026-06-07) don't match. Oil is 1.6x and the stress index is 1.25x higher in `commodity_market.csv`. We kept the values from `weekly_route_operations.csv`.

3. **Geopolitical events**, which took the most work because the events aren't weekly and can't be joined directly.
    - **Matched regions:** country regions were grouped into the broader event regions (e.g. "South Asia" becomes "Asia").
    - **Dropped Africa and Middle East events:** events cover 6 regions, but routes only start and end in 4. We don't know which routes pass through the other 2, so those events were dropped (6,655 of 10,000 kept).
    - **Counted active events per week:** an event is active from `date` to `date + duration_days`. For each week, we count the active events in the route's origin and destination regions and add up their `risk_increase`.
    - **Major shocks:** COVID (all routes) and the Russia-Ukraine war (routes to or from Europe) became 0/1 flags. The Red Sea crisis was dropped (Middle East).
    - **Warm-up:** the first 52 weeks are flagged with `events_warmup`, because events that started before 2015 are missing from the file.

**For modeling:** don't use a week's event features or `shipping_delay_days` to predict that same week's `route_status`. Use week *t* to predict week *t+1*.
