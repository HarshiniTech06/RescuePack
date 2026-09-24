from brute_force import brute_force_knapsack
from branch_bound import branch_and_bound_knapsack
import time


# =====================================================
# RESCUEPACK
# =====================================================

print("========================================")
print("          🚑 RESCUEPACK")
print("   Emergency Resource Optimization")
print("========================================")


# =====================================================
# GET CAPACITY
# =====================================================

capacity = float(
    input("\nEnter vehicle capacity (kg): ")
)


# =====================================================
# GET NUMBER OF RESOURCES
# =====================================================

n = int(
    input("Enter number of resources: ")
)


items = []


# =====================================================
# GET RESOURCE DETAILS
# =====================================================

for i in range(n):

    print(f"\nResource {i + 1}")

    name = input("Enter resource name: ")

    weight = float(
        input("Enter weight (kg): ")
    )

    value = float(
        input("Enter priority/value: ")
    )

    items.append({
        "name": name,
        "weight": weight,
        "value": value
    })


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
# DISPLAY OPTIMIZATION RESULT
# =====================================================

print("\n\n========================================")
print("        OPTIMIZATION RESULT")
print("========================================")


# =====================================================
# BRUTE FORCE RESULT
# =====================================================

print("\n------ 🔵 BRUTE FORCE ------")

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

print("\n------ 🟢 BRANCH AND BOUND ------")

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
# SEARCH REDUCTION
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
# FINAL COMPARISON
# =====================================================

print("\n========================================")
print("             COMPARISON")
print("========================================")


# Check whether both algorithms
# found the same optimal value

if (
    brute_result["best_value"]
    == bb_result["best_value"]
):

    print(
        "\n✅ Both algorithms found the "
        "same optimal value."
    )

else:

    print(
        "\n❌ Results are different."
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
# END
# =====================================================

print("\n========================================")
print("               END")
print("========================================")