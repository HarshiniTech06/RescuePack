from brute_force import brute_force_knapsack
from branch_bound import branch_and_bound_knapsack
import time


# =====================================================
# RESCUEPACK - TEST DATA
# =====================================================

items = [

    {
        "name": "Oxygen Cylinder",
        "weight": 8,
        "value": 100
    },

    {
        "name": "Defibrillator",
        "weight": 6,
        "value": 95
    },

    {
        "name": "Emergency Medicines",
        "weight": 4,
        "value": 90
    },

    {
        "name": "First Aid Kit",
        "weight": 3,
        "value": 70
    },

    {
        "name": "PPE Kit",
        "weight": 2,
        "value": 40
    }

]


# =====================================================
# CAPACITY
# =====================================================

capacity = 20


# =====================================================
# DISPLAY INPUT
# =====================================================

print("========================================")
print("           🚑 RESCUEPACK")
print("    Emergency Resource Optimization")
print("========================================")

print("\nMission: Ambulance Emergency Support")

print(
    "Vehicle Capacity:",
    capacity,
    "kg"
)

print("\nAvailable Resources:")

for item in items:

    print(
        "-",
        item["name"],
        "| Weight:",
        item["weight"],
        "kg",
        "| Priority:",
        item["value"]
    )


# =====================================================
# RUN BRUTE FORCE
# =====================================================

start_time = time.perf_counter()

brute_result = brute_force_knapsack(
    items,
    capacity
)

end_time = time.perf_counter()

brute_time_ms = (
    end_time - start_time
) * 1000


# =====================================================
# RUN BRANCH AND BOUND
# =====================================================

start_time = time.perf_counter()

bb_result = branch_and_bound_knapsack(
    items,
    capacity
)

end_time = time.perf_counter()

bb_time_ms = (
    end_time - start_time
) * 1000


# =====================================================
# CALCULATE SEARCH REDUCTION
# =====================================================

combinations = brute_result[
    "combinations_checked"
]

nodes = bb_result[
    "nodes_explored"
]


if combinations > 0:

    search_reduction = (
        (combinations - nodes)
        / combinations
    ) * 100

else:

    search_reduction = 0


# =====================================================
# BRUTE FORCE RESULT
# =====================================================

print("\n========================================")
print("          🔵 BRUTE FORCE")
print("========================================")

print("\nSelected Resources:")

if brute_result["best_items"]:

    for item in brute_result["best_items"]:

        print("-", item)

else:

    print("- No resources selected")


print(
    "\nTotal Weight:",
    brute_result["best_weight"],
    "kg"
)

print(
    "Total Priority:",
    brute_result["best_value"]
)

print(
    "Combinations Checked:",
    brute_result["combinations_checked"]
)

print(
    "Execution Time:",
    round(brute_time_ms, 4),
    "ms"
)

print(
    "Time Complexity:",
    brute_result["time_complexity"]
)


# =====================================================
# BRANCH AND BOUND RESULT
# =====================================================

print("\n========================================")
print("        🟢 BRANCH AND BOUND")
print("========================================")

print("\nSelected Resources:")

if bb_result["best_items"]:

    for item in bb_result["best_items"]:

        print("-", item)

else:

    print("- No resources selected")


print(
    "\nTotal Weight:",
    bb_result["best_weight"],
    "kg"
)

print(
    "Total Priority:",
    bb_result["best_value"]
)

print(
    "Nodes Explored:",
    bb_result["nodes_explored"]
)

print(
    "Branches Pruned:",
    bb_result["branches_pruned"]
)

print(
    "Execution Time:",
    round(bb_time_ms, 4),
    "ms"
)

print(
    "Time Complexity:",
    bb_result["time_complexity"]
)


# =====================================================
# COMPARISON
# =====================================================

print("\n========================================")
print("             COMPARISON")
print("========================================")


# Check optimal values

if (
    brute_result["best_value"]
    == bb_result["best_value"]
):

    print(
        "\n✅ Both algorithms found "
        "the same optimal value."
    )

else:

    print(
        "\n❌ Algorithms produced "
        "different results."
    )


# Check optimal weights

if (
    brute_result["best_weight"]
    == bb_result["best_weight"]
):

    print(
        "✅ Both solutions have "
        "the same total weight."
    )


print(
    "\nSearch Reduction:",
    round(search_reduction, 2),
    "%"
)


print(
    "\nBrute Force:",
    brute_result["combinations_checked"],
    "combinations checked"
)

print(
    "Branch & Bound:",
    bb_result["nodes_explored"],
    "nodes explored"
)

print(
    "Branches Pruned:",
    bb_result["branches_pruned"]
)


# =====================================================
# FINAL RESULT
# =====================================================

print("\n========================================")
print("          FINAL OPTIMAL SOLUTION")
print("========================================")

print(
    "\nMaximum Priority:",
    brute_result["best_value"]
)

print(
    "Total Weight:",
    brute_result["best_weight"],
    "kg"
)

print(
    "Unused Capacity:",
    capacity - brute_result["best_weight"],
    "kg"
)

print("\nResources Selected:")

for item in brute_result["best_items"]:

    print("-", item)


# =====================================================
# END
# =====================================================

print("\n========================================")
print("                 END")
print("========================================")