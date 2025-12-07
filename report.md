# 10-Year Fiscal Impact Simulation of NYC Welfare Policies Using Monte Carlo Modeling

## 1. Project Overview

This project builds a 10-year fiscal model to test whether a hypothetical New York City mayor’s large-scale social welfare policies are financially sustainable.

The model simulates the total cost of three major programs:

1. Universal childcare
2. A free / fast city bus system
3. City-run grocery stores with subsidies

Instead of assuming fixed numbers, the model uses **Monte Carlo simulation** to incorporate uncertainty and cost volatility. This is similar to how hedge funds and public finance analysts model risk.

---

## 2. Objectives

- Estimate the **expected 10-year total cost** of the welfare package.
- Quantify the **risk and volatility** of these costs.
- Understand **best-case vs worst-case** scenarios.
- Estimate **per-capita burden** on citizens.
- Provide a **risk-aware perspective** on whether such policies are fiscally realistic.

---

## 3. Assumptions

### 3.1 City & Population

- City: New York City (hypothetical scenario)
- Population: 8.5 million

### 3.2 Programs Modeled

#### Program 1 – Universal Childcare

- Children covered: 900,000
- Participation rate: 55%
- Cost per child (Year 1): \$6,000/year
- Annual real cost growth: 2%

#### Program 2 – Free Public Bus System

- Operating cost (Year 1): \$4.0 billion
- Lost ticket revenue (Year 1): \$0.9 billion
- Annual cost drift: 2%
- Capex renewal: \$2.0 billion every 5 years

#### Program 3 – City-Run Grocery Stores

- Number of stores: 120
- Cost per store (Year 1): \$3.5 million
- City subsidy: 20% of base cost
- Annual cost drift: 3%

### 3.3 Uncertainty Modeling

- Each program’s yearly cost is multiplied by a **lognormal shock**.
- Volatility parameter: `sigma = 0.18`
- This reflects:
  - cost overruns
  - inflation spikes
  - supply chain disruptions
  - unexpected participation changes

---

## 4. Methodology

### 4.1 Deterministic Core

For each year:

- Compute childcare cost:
  - `children × participation × cost_per_child`
- Compute bus cost:
  - `operating_cost + lost_fares (+ capex in renewal years)`
- Compute grocery subsidy cost:
  - `stores × cost_per_store × subsidy_rate`
- Apply annual growth to each program’s base cost for the next year.

### 4.2 Stochastic Layer (Monte Carlo)

- For each year and each program, apply a random multiplicative shock:
  - `shock = lognormal(mean=0, sigma=0.18)`
- Run **20,000 simulations**, each covering a 10-year horizon.
- In each simulation, sum total costs across all programs and all 10 years.

This yields a **distribution of possible 10-year cost outcomes**, not just a single number.

---

## 5. Results

> Mean total cost (10 years): $92.62 billion  
Median: $92.55 billion  
Standard deviation: $3.71 billion  
Min observed: $78.72 billion  
Max observed: $107.81 billion  
P10: $87.90 billion  
P25: $90.08 billion  
P75: $95.06 billion  
P90: $97.41 billion  

Per-capita 10-year cost: $10,896  
Per-capita annual cost: ~$1,090



### 5.1 Key Statistics (10-Year Total Cost)

Mean total cost: $92.62 billion

Median total cost: $92.55 billion

Standard deviation: $3.71 billion

10th percentile (P10): $87.90 billion (very optimistic scenario)

90th percentile (P90): $97.41 billion (very pessimistic scenario)

Minimum / Maximum observed in simulations: $78.72 billion / $107.81 billion

### 5.2 Per Capita Cost

- Mean per-capita 10-year burden: $10,896

  Approximate per year: $1,090 per person per year

### 5.3 Distribution

The histogram (`results/cost_distribution.png`) shows:

- A right-skewed distribution (typical of lognormal cost models).
- Most scenarios concentrated around the mean.
- A tail of high-cost outcomes representing rare but dangerous cost explosions.

---

## 6. Interpretation

The Monte Carlo simulation shows that the proposed welfare package would cost New York City an estimated $92.6 billion over 10 years, with a standard deviation of just $3.7 billion, indicating that the total cost is relatively predictable despite underlying volatility.

Across 20,000 simulated paths, the cost distribution was tight, with 80% of outcomes falling between $87.9 billion (P10) and $97.4 billion (P90).
Even in the most extreme scenarios, costs remained within a realistic fiscal band (min: $78.7B, max: $107.8B).

The average per-capita cost over a decade is approximately $10,896, or roughly $1,090 per year, suggesting that while the program is expensive, it is not fiscally explosive.

Overall, the policies appear costly but stable, with limited risk of catastrophic budget overruns under normal economic uncertainty.
---

## 7. Conclusion

This project shows that:

- Large-scale welfare policies **cannot be evaluated** using only fixed, single-number projections.
- A proper assessment needs:
  - uncertainty,
  - volatility,
  - best- and worst-case scenarios,
  - and probabilistic reasoning.

By using **Monte Carlo simulation**, this model provides a more realistic picture of the fiscal risk of ambitious social policies.

---

## 8. Skills Demonstrated

- Quantitative finance concepts (Monte Carlo, distributions, volatility)
- Public finance & policy analysis
- Python (NumPy, pandas, matplotlib)
- Risk modeling using lognormal shocks
- Long-term forecasting and cost modeling
- Data visualization and reporting

---

## 9. Possible Extensions

- Add more programs (housing, healthcare, education).
- Include revenue modeling and city budget constraints.
- Model GDP growth and debt-to-GDP ratios.
- Use scenario analysis (recession vs boom cases).
- Adapt the model to **another city** (e.g., Hong Kong, Singapore, or Warsaw).
