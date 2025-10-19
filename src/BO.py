from bayes_opt import BayesianOptimization
import numpy as np

# --- pretend KPI for now ------------------------------------------------------
rng = np.random.default_rng(42)  # reproducible "random" J values

def compute_kpi_dummy(max_vel_x, acc_lim_x):
    """
    Stand-in for your real KPI (cumulative RMSE for distance + yaw).
    Returns J in [0.5, 10].
    """
    return float(rng.uniform(0.5, 10.0))

# BO maximizes, so return -J
def evaluate(max_vel_x, acc_lim_x):
    J = compute_kpi_dummy(max_vel_x, acc_lim_x)
    print(f"trial -> params: max_vel_x={max_vel_x:.4f}, acc_lim_x={acc_lim_x:.4f}  |  J={J:.4f}")
    return -J  # maximize(-J) == minimize(J)

# --- search space -------------------------------------------------------------
pbounds = {
    "max_vel_x": (0.05, 1.20),
    "acc_lim_x": (0.05, 0.30),
}

# --- optimizer ----------------------------------------------------------------
optimizer = BayesianOptimization(
    f=evaluate,
    pbounds=pbounds,
    random_state=123,           # exploration reproducibility
    allow_duplicate_points=True # handy while you're mocking J
)

# Use Expected Improvement (good when minimizing a scalar like J)
# Lower xi -> greedier exploitation; higher -> more exploration
optimizer.maximize(init_points=3, n_iter=0, acq="ei", xi=0.01)

# Step-wise loop so we can early-stop once J < 1 (i.e., target > -1)
max_total_iters = 30  # safety cap
for i in range(max_total_iters):
    optimizer.maximize(init_points=0, n_iter=1, acq="ei", xi=0.01)

    best_target = optimizer.max["target"]    # this is -J*
    best_J = -best_target
    print(f"[iter {i+1}] current best J = {best_J:.4f} at {optimizer.max['params']}")

    if best_J < 1.0:
        print("✅ Early stop: reached J < 1")
        break

# --- results ------------------------------------------------------------------
print("\n=== BO summary ===")
print("best params:", optimizer.max["params"])
print("best J     :", -optimizer.max["target"])
# If you want to inspect all trials:
# for r in optimizer.res: print(r)
