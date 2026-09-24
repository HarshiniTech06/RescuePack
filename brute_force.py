def brute_force_knapsack(items, capacity):

    # ========================================
    # NUMBER OF ITEMS
    # ========================================

    n = len(items)

    best_value = 0
    best_weight = 0
    best_items = []

    combinations_checked = 0


    # ========================================
    # CHECK EVERY POSSIBLE COMBINATION
    # ========================================

    # There are 2^n possible combinations.
    #
    # Example:
    # 5 items -> 2^5 = 32 combinations
    #
    # Each binary bit represents:
    # 0 = Do not select item
    # 1 = Select item

    for mask in range(1 << n):

        total_weight = 0
        total_value = 0
        selected_items = []


        # ====================================
        # CHECK EACH ITEM
        # ====================================

        for i in range(n):

            # Check whether item i is selected

            if mask & (1 << i):

                total_weight += items[i]["weight"]

                total_value += items[i]["value"]

                selected_items.append(
                    items[i]["name"]
                )


        # ====================================
        # COUNT COMBINATION
        # ====================================

        combinations_checked += 1


        # ====================================
        # CHECK CAPACITY
        # ====================================

        if total_weight <= capacity:

            # =================================
            # CHECK BEST SOLUTION
            # =================================

            if total_value > best_value:

                best_value = total_value

                best_weight = total_weight

                best_items = selected_items


    # ========================================
    # RETURN RESULT
    # ========================================

    return {

        "best_value":
            best_value,

        "best_weight":
            best_weight,

        "best_items":
            best_items,

        "combinations_checked":
            combinations_checked,

        "time_complexity":
            "O(2^n)"

    }