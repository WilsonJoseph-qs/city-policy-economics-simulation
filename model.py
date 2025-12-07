import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# ==========================
# 1. GLOBAL PARAMETERS
# ==========================

YEARS = 10
RUNS = 20000

POPULATION = 8_500_000  # approximate NYC population

# Childcare program assumptions
CHILDREN_COUNT = 900_000
CHILDCARE_PARTICIPATION = 0.55
CHILDCARE_COST_PER_CHILD_YEAR1 = 6000  # USD per year
CHILDCARE_ANNUAL_GROWTH = 0.02        # 2% cost drift

# Free bus system assumptions
BUS_OPERATING_COST_YEAR1 = 4_000_000_000   # yearly ops
BUS_LOST_FARES_YEAR1 = 900_000_000         # no ticket revenue
BUS_ANNUAL_GROWTH = 0.02                   # 2%

# Optional capex every 5 years (e.g. fleet renewal)
BUS_CAPEX_EVERY_N_YEARS = 5
BUS_CAPEX_AMOUNT = 2_000_000_000

# City-run grocery store assumptions
GROCERY_STORES = 120
GROCERY_COST_PER_STORE_YEAR1 = 3_500_000
GROCERY_SUBSIDY_RATE = 0.20              # city covers 20% of cost
GROCERY_ANNUAL_GROWTH = 0.03             # 3%

# Uncertainty (lognormal shock)
SIGMA = 0.18  # volatility of costs


# ==========================
# 2. HELPER FUNCTIONS
# ==========================

def lognormal_shock(sigma: float) -> float:
    """
    Returns a multiplicative cost shock.
    Using lognormal so cost never becomes negative.
    """
    return np.random.lognormal(mean=0.0, sigma=sigma)


def simulate_one_path(years: int = YEARS) -> float:
    """
    Simulate ONE 10-year path of total program cost.
    Returns the total cost over the entire horizon.
    """

    total_cost = 0.0

    childcare_cost = CHILDCARE_COST_PER_CHILD_YEAR1
    bus_cost = BUS_OPERATING_COST_YEAR1 + BUS_LOST_FARES_YEAR1
    grocery_cost_per_store = GROCERY_COST_PER_STORE_YEAR1

    for year in range(1, years + 1):

        # Random shocks per program
        childcare_shock = lognormal_shock(SIGMA)
        bus_shock = lognormal_shock(SIGMA)
        grocery_shock = lognormal_shock(SIGMA)

        # ---- Childcare program ----
        childcare_year_cost = (
            CHILDREN_COUNT
            * CHILDCARE_PARTICIPATION
            * childcare_cost
            * childcare_shock
        )

        # ---- Bus program ----
        bus_year_cost = bus_cost * bus_shock

        # Add capex in certain years
        if year % BUS_CAPEX_EVERY_N_YEARS == 0:
            bus_year_cost += BUS_CAPEX_AMOUNT * lognormal_shock(SIGMA)

        # ---- Grocery program ----
        grocery_base = GROCERY_STORES * grocery_cost_per_store
        grocery_year_cost = grocery_base * GROCERY_SUBSIDY_RATE * grocery_shock

        # ---- Sum all programs ----
        year_total = childcare_year_cost + bus_year_cost + grocery_year_cost
        total_cost += year_total

        # ---- Update drifts for next year ----
        childcare_cost *= (1 + CHILDCARE_ANNUAL_GROWTH)
        bus_cost *= (1 + BUS_ANNUAL_GROWTH)
        grocery_cost_per_store *= (1 + GROCERY_ANNUAL_GROWTH)

    return total_cost


def run_monte_carlo(runs: int = RUNS, years: int = YEARS) -> np.ndarray:
    """
    Run many simulations and return array of total 10-year costs.
    """
    results = np.empty(runs)
    for i in range(runs):
        results[i] = simulate_one_path(years)
        if (i + 1) % 2000 == 0:
            print(f"Completed {i + 1} / {runs} simulations...")
    return results


def summarize_results(results: np.ndarray) -> dict:
    """
    Compute key statistics on the simulation results.
    """
    summary = {
        "mean": results.mean(),
        "median": np.median(results),
        "std": results.std(),
        "min": results.min(),
        "max": results.max(),
        "p10": np.percentile(results, 10),
        "p25": np.percentile(results, 25),
        "p75": np.percentile(results, 75),
        "p90": np.percentile(results, 90),
    }

    # Per capita cost over 10 years
    summary["per_capita_mean"] = summary["mean"] / POPULATION

    return summary


def save_results(results: np.ndarray, summary: dict, results_dir: str = "results"):
    """
    Save raw simulation results and summary to CSV files.
    """
    os.makedirs(results_dir, exist_ok=True)

    df = pd.DataFrame({"total_10yr_cost": results})
    df.to_csv(os.path.join(results_dir, "simulation_output.csv"), index=False)

    summary_df = pd.DataFrame(list(summary.items()), columns=["metric", "value"])
    summary_df.to_csv(os.path.join(results_dir, "summary_stats.csv"), index=False)


def plot_distribution(results: np.ndarray, results_dir: str = "results"):
    """
    Plot a histogram of the distribution of total 10-year costs.
    """
    os.makedirs(results_dir, exist_ok=True)

    plt.figure()
    plt.hist(results / 1e9, bins=50)  # convert to billions for nicer scale
    plt.xlabel("Total 10-year cost (billion USD)")
    plt.ylabel("Frequency")
    plt.title("Distribution of 10-year Total Cost (Monte Carlo)")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "cost_distribution.png"))
    plt.close()


# ==========================
# 3. MAIN EXECUTION
# ==========================

if __name__ == "__main__":

    np.random.seed(42)  # for reproducibility

    print("Running Monte Carlo simulation...")
    results = run_monte_carlo()

    print("\nComputing summary statistics...")
    summary = summarize_results(results)

    print("\n===== SUMMARY =====")
    for k, v in summary.items():
        if "per_capita" in k:
            print(f"{k:15s}: ${v:,.2f}")
        else:
            print(f"{k:15s}: ${v:,.2f}")

    print("\nSaving results to 'results/' ...")
    save_results(results, summary)

    print("Generating distribution plot...")
    plot_distribution(results)

    print("\nDone. Check the 'results' folder for:")
    print("- simulation_output.csv")
    print("- summary_stats.csv")
    print("- cost_distribution.png")
