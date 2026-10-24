# Data Comprehension

There are 5 raw CSV files in `data/`. They are merged into one file (see the Data Merge Summary below), and the model is trained on a smaller version of that merged file (see Files Used for Modeling at the end).
- **commodity_market.csv**
    - Weekly global commodity prices (oil, gas, steel, wheat, copper) and a combined `commodity_stress_index` from 2015 - 2026. Gives the economic backdrop that pushes up fuel and freight costs.
- **country_metadata.csv**
    - One row for each of the 10 countries: region, income group, GDP, trade dependency, port capacity and logistics performance. Shows how exposed or resilient each country on a route is.
    - The 10 countries are: China, India, United States, Germany, Japan, Brazil, United Kingdom, France, Canada and Australia.
- **geopolitical_events.csv**
    - About 10k dated events (strikes, sanctions, conflicts, cyber attacks) with severity, affected region, duration and `risk_increase`. Includes 3 major shocks: COVID, the Russia-Ukraine war and the Red Sea crisis. These are outside risk drivers and possible early warning signals.
- **trade_routes.csv**
    - Lookup table for the 50 routes (`route_id`): origin and destination country, distance, shipping method, cargo type and planned transit days. It links the operations data to the countries.
- **weekly_route_operations.csv**
    - Contains 31,300 rows, one per route per week (50 routes * 626 weeks). It has volume, delay, cost, congestion, weather and geopolitical risk scores, emissions, and the target `route_status` (Normal / Delayed / Disrupted). It is the base table that every other file is merged onto. The model is not trained on this raw file directly.

## Data Merge Summary (TL;DR)

Full details are in `notebooks/01_data_preparation.ipynb`. The result is saved to `data/preprocessed/supply_chain_disruption.csv` (31,300 rows, 48 columns).

**Base file:** `weekly_route_operations.csv`. This is the starting table for the merge, not the final output. Every other file is joined onto it, so the merged file keeps one row per route per week.

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

**For modeling:** don't use a week's event features or `shipping_delay_days` to predict that same week's `route_status`. Use week *t* to predict week *t+1* (The previous week of the desired week you want to predict).

## Files Used for Modeling

| File | Made by | Contents |
|---|---|---|
| `data/preprocessed/supply_chain_disruption.csv` | `01_data_preparation` | All the merged data (31,300 rows, 48 columns). |
| `data/preprocessed/model_ready.csv` | `02_2_feature_selection` | **What the models train on.** Same rows, cut to 11 columns. |

`model_ready.csv` columns:
- **IDs:** `date`, `route_id`
- **Split:** `split` (train or test)
- **Target:** `route_status`
- **Features (7):** `geopolitical_risk_score`, `port_congestion_index`, `weather_disruption_score`, `origin_active_event_risk`, `destination_active_event_risk`, `covid_supply_shock_active`, `russia_ukraine_war_active`

The other merged columns (country details, commodity prices, distance, etc.) were dropped in `02_2_feature_selection`. They mostly helped the model tell which time period a row came from or recognize individual routes, rather than predict disruptions. Go back to `supply_chain_disruption.csv` only if you want to test adding features back.
