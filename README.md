# NYC Welfare Policy Fiscal Simulation (10-Year Monte Carlo Model)

This project builds a 10-year fiscal simulation to evaluate whether a hypothetical New York City mayor’s large-scale social welfare programs are financially sustainable.  
The model uses **Monte Carlo simulation (20,000 runs)** to capture uncertainty, volatility, cost drift, and rare economic shocks, similar to techniques used in quantitative finance and public policy analysis.

---

## Project Objectives

- Estimate the **expected 10-year cost** of proposed welfare programs.
- Quantify **risk, volatility, and uncertainty** using lognormal stochastic shocks.
- Generate **best-case and worst-case fiscal scenarios**.
- Compute **per-capita financial burden**.
- Provide a **data-driven assessment** of policy sustainability.

---

## Programs Modeled

### **1. Universal Childcare**
- 900,000 children  
- 55% participation  
- \$6,000 per child per year  
- 2% annual cost drift  

### **2. Free & Fast Bus Transportation System**
- \$4.0B annual operating cost  
- \$0.9B in lost fare revenue  
- 2% yearly growth  
- \$2B capex every 5 years  

### **3. City-Run Grocery Stores**
- 120 stores  
- \$3.5M per store  
- 20% city subsidy  
- 3% annual growth  

Each program is subjected to **lognormal cost shocks** representing inflation spikes, supply-chain disruptions, participation changes, and cost overruns.

---

## Methodology

### **Monte Carlo Simulation**
- 20,000 simulated fiscal paths  
- 10-year horizon  
- Lognormal uncertainty (`sigma = 0.18`)  
- Yearly cost drift per program  
- Random shocks applied independently to:
  - Childcare
  - Transportation
  - Grocery subsidies

### **Outputs Generated**
- `simulation_output.csv` – raw results of all runs  
- `summary_stats.csv` – key metrics  
- `cost_distribution.png` – histogram of total costs  

---

## Key Results (From Simulation)

### **10-Year Total Cost Distribution**
- **Mean:** \$92.62 billion  
- **Median:** \$92.55 billion  
- **Standard deviation:** \$3.71 billion  
- **P10:** \$87.90 billion  
- **P90:** \$97.41 billion  
- **Min observed:** \$78.72 billion  
- **Max observed:** \$107.81 billion  

### **Per-Capita Impact**
- **10-year per-capita cost:** \$10,896  
- **Annual per-capita cost:** ~\$1,090  

### Interpretation  
The welfare package is **expensive but stable**, with limited risk of extreme overruns.  
Most scenarios fall within a narrow band, suggesting predictable fiscal behavior under uncertainty.

---

##  Project Structure

NYC_Welfare_MonteCarlo_Model/
│
├── model.py # Monte Carlo simulation engine
├── report.md # Full technical report
└── results/
├── simulation_output.csv
├── summary_stats.csv
└── cost_distribution.png


--

##  How to Run the Model

**1. Install dependencies**

pip install numpy pandas matplotlib
2. Run the simulation

python model.py

All output files will appear inside the results/ directory.

