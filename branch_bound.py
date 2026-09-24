import heapq


# =====================================================
# CALCULATE UPPER BOUND
# =====================================================

def calculate_bound(
    items,
    level,
    current_weight,
    current_value,
    capacity
):
    """
    Calculate the optimistic upper bound
    of a Branch & Bound node.
    """

    # No more capacity available
    if current_weight >= capacity:
        return current_value

    bound = current_value
    weight = current_weight
    n = len(items)

    i = level


    # =================================================
    # ADD COMPLETE ITEMS
    # =================================================

    while (
        i < n
        and weight + items[i]["weight"] <= capacity
    ):

        weight += items[i]["weight"]
        bound += items[i]["value"]

        i += 1


    # =================================================
    # ADD FRACTION OF NEXT ITEM
    # =================================================

    # The fraction is used ONLY for calculating
    # the optimistic upper bound.
    #
    # The actual knapsack solution is still 0/1.

    if i < n:

        remaining_capacity = (
            capacity - weight
        )

        bound += (
            remaining_capacity
            * items[i]["value"]
            / items[i]["weight"]
        )


    return bound



# =====================================================
# BRANCH AND BOUND KNAPSACK
# =====================================================

def branch_and_bound_knapsack(items, capacity):

    # =================================================
    # SORT ITEMS BY VALUE / WEIGHT RATIO
    # =================================================

    items = sorted(
        items,
        key=lambda x:
            x["value"] / x["weight"],
        reverse=True
    )


    n = len(items)


    # =================================================
    # BEST SOLUTION
    # =================================================

    best_value = 0
    best_weight = 0
    best_items = []


    # =================================================
    # PERFORMANCE COUNTERS
    # =================================================

    nodes_explored = 0
    branches_pruned = 0


    # =================================================
    # INITIAL UPPER BOUND
    # =================================================

    initial_bound = calculate_bound(
        items,
        0,
        0,
        0,
        capacity
    )


    # =================================================
    # PRIORITY QUEUE
    # =================================================

    priority_queue = []


    heapq.heappush(
        priority_queue,
        (
            -initial_bound,
            0,
            0,
            0,
            []
        )
    )


    # =================================================
    # BRANCH AND BOUND SEARCH
    # =================================================

    while priority_queue:

        (
            neg_bound,
            level,
            current_weight,
            current_value,
            selected_items
        ) = heapq.heappop(
            priority_queue
        )


        # Convert negative bound to positive
        upper_bound = -neg_bound


        # Count explored node
        nodes_explored += 1


        # =================================================
        # PRUNE USING UPPER BOUND
        # =================================================

        if upper_bound <= best_value:

            branches_pruned += 1

            continue


        # =================================================
        # ALL ITEMS HAVE BEEN CONSIDERED
        # =================================================

        if level >= n:

            continue


        # Current item
        item = items[level]


        # =================================================
        # BRANCH 1: TAKE THE ITEM
        # =================================================

        new_weight = (
            current_weight
            + item["weight"]
        )

        new_value = (
            current_value
            + item["value"]
        )


        # Check whether item fits
        if new_weight <= capacity:

            new_selected_items = (
                selected_items
                + [item["name"]]
            )


            # =============================================
            # UPDATE BEST SOLUTION
            # =============================================

            if new_value > best_value:

                best_value = new_value

                best_weight = new_weight

                best_items = new_selected_items


            # =============================================
            # CALCULATE UPPER BOUND
            # =============================================

            new_bound = calculate_bound(
                items,
                level + 1,
                new_weight,
                new_value,
                capacity
            )


            # =============================================
            # ADD TAKE BRANCH IF PROMISING
            # =============================================

            if new_bound > best_value:

                heapq.heappush(
                    priority_queue,
                    (
                        -new_bound,
                        level + 1,
                        new_weight,
                        new_value,
                        new_selected_items
                    )
                )

            else:

                branches_pruned += 1


        else:

            # Item exceeds capacity
            branches_pruned += 1


        # =================================================
        # BRANCH 2: DO NOT TAKE THE ITEM
        # =================================================

        exclude_bound = calculate_bound(
            items,
            level + 1,
            current_weight,
            current_value,
            capacity
        )


        # =============================================
        # ADD EXCLUDE BRANCH IF PROMISING
        # =============================================

        if exclude_bound > best_value:

            heapq.heappush(
                priority_queue,
                (
                    -exclude_bound,
                    level + 1,
                    current_weight,
                    current_value,
                    selected_items
                )
            )

        else:

            branches_pruned += 1


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "best_value":
            best_value,

        "best_weight":
            best_weight,

        "best_items":
            best_items,

        "nodes_explored":
            nodes_explored,

        "branches_pruned":
            branches_pruned,

        "time_complexity":
            "O(2^n) worst case"

    }