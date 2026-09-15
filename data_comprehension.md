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