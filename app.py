from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    session
)

import time
import os
import mysql.connector

from brute_force import brute_force_knapsack
from branch_bound import branch_and_bound_knapsack


app = Flask(__name__)

# ========================================
# FLASK SESSION SECRET KEY
# ========================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-key"
)


# ========================================
# FRONTEND FOLDER
# ========================================

FRONTEND_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "frontend"
)


# ========================================
# DATABASE CONNECTION
# ========================================

def get_db_connection():

    connection = mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),
        port=int(os.environ.get("MYSQLPORT", 3306)),
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD", ""),
        database=os.environ.get(
            "MYSQLDATABASE",
            "rescuepack_db"
        )
    )

    return connection


# ========================================
# TEST DATABASE CONNECTION
# ========================================

@app.route("/test-db")
def test_db():

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE()")

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Database connection successful",
            "database": result[0]
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ========================================
# TEST USERS TABLE
# ========================================

@app.route("/test-users")
def test_users():

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                username,
                created_at
            FROM users
            """
        )

        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(users)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ========================================
# USER LOGIN
# ========================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No login data received."
            }), 400

        username = data.get(
            "username",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        )

        if username == "" or password == "":

            return jsonify({
                "success": False,
                "message":
                    "Username and password are required."
            }), 400

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                username,
                password_hash
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user is None:

            return jsonify({
                "success": False,
                "message":
                    "Invalid username or password."
            }), 401

        if password != user["password_hash"]:

            return jsonify({
                "success": False,
                "message":
                    "Invalid username or password."
            }), 401

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "username": user["username"]
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# ========================================
# CHECK CURRENT USER
# ========================================

@app.route("/current-user")
def current_user():

    if "user_id" not in session:

        return jsonify({
            "logged_in": False
        })

    return jsonify({
        "logged_in": True,
        "user_id": session["user_id"],
        "username": session["username"]
    })


# ========================================
# LOGOUT
# ========================================

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })


# ========================================
# OPEN LOGIN PAGE
# ========================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_FOLDER,
        "page1.html"
    )


# ========================================
# SERVE FRONTEND FILES
# ========================================

@app.route("/<path:filename>")
def frontend_files(filename):

    file_path = os.path.join(
        FRONTEND_FOLDER,
        filename
    )

    # Prevent invalid file access
    if not os.path.isfile(file_path):

        return jsonify({
            "error": "File not found",
            "file": filename
        }), 404

    return send_from_directory(
        FRONTEND_FOLDER,
        filename
    )


# ========================================
# OPTIMIZATION API
# ========================================

@app.route(
    "/optimize",
    methods=["POST"]
)
def optimize():

    try:

        # ====================================
        # CHECK LOGIN
        # ====================================

        if "user_id" not in session:

            return jsonify({
                "error":
                    "Please login before using RescuePack."
            }), 401

        # ====================================
        # GET DATA FROM FRONTEND
        # ====================================

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No data received."
            }), 400

        # ====================================
        # GET MISSION
        # ====================================

        mission = data["mission"]

        # ====================================
        # GET CAPACITY
        # ====================================

        capacity = float(
            data["capacity"]
        )

        # ====================================
        # GET RESOURCES
        # ====================================

        items = data["items"]

        if not items:

            return jsonify({
                "error":
                    "No resources provided."
            }), 400

        # ====================================
        # CONVERT VALUES
        # ====================================

        for item in items:

            item["weight"] = float(
                item["weight"]
            )

            item["value"] = float(
                item["value"]
            )

        # ====================================
        # BRUTE FORCE
        # ====================================

        start_time = time.perf_counter()

        brute_result = brute_force_knapsack(
            items,
            capacity
        )

        end_time = time.perf_counter()

        # Convert seconds to microseconds
        brute_time_us = (
            end_time - start_time
        ) * 1_000_000


        # ====================================
        # BRANCH AND BOUND
        # ====================================

        start_time = time.perf_counter()

        bb_result = branch_and_bound_knapsack(
            items,
            capacity
        )

        end_time = time.perf_counter()

        # Convert seconds to microseconds
        bb_time_us = (
            end_time - start_time
        ) * 1_000_000


        # ====================================
        # ADD EXECUTION TIMES
        # ====================================

        brute_result[
            "execution_time_us"
        ] = round(
            brute_time_us,
            3
        )

        bb_result[
            "execution_time_us"
        ] = round(
            bb_time_us,
            3
        )


        # ====================================
        # TIME COMPLEXITY
        # ====================================

        brute_result[
            "time_complexity"
        ] = "O(2^n)"

        bb_result[
            "time_complexity"
        ] = "O(2^n) worst case"


        # ====================================
        # SEARCH REDUCTION
        # ====================================

        combinations = brute_result[
            "combinations_checked"
        ]

        nodes = bb_result[
            "nodes_explored"
        ]

        if combinations > 0:

            search_reduction = (
                (
                    combinations - nodes
                )
                /
                combinations
            ) * 100

        else:

            search_reduction = 0


        search_reduction = round(
            search_reduction,
            2
        )


        # ====================================
        # CHECK SAME SOLUTION
        # ====================================

        same_solution = (
            brute_result["best_value"]
            ==
            bb_result["best_value"]
        )


        # ====================================
        # REMAINING CAPACITY
        # ====================================

        remaining_capacity = round(
            capacity -
            brute_result["best_weight"],
            2
        )


        # ====================================
        # SAVE HISTORY
        # ====================================

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO optimization_history (
                user_id,
                mission,
                capacity,
                brute_force_value,
                brute_force_weight,
                combinations_checked,
                branch_bound_value,
                branch_bound_weight,
                nodes_explored,
                branches_pruned,
                search_reduction
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            """,
            (
                session["user_id"],
                mission,
                capacity,
                brute_result["best_value"],
                brute_result["best_weight"],
                brute_result["combinations_checked"],
                bb_result["best_value"],
                bb_result["best_weight"],
                bb_result["nodes_explored"],
                bb_result["branches_pruned"],
                search_reduction
            )
        )

        connection.commit()

        cursor.close()
        connection.close()


        # ====================================
        # SEND RESULTS
        # ====================================

        return jsonify({

            "brute_force":
                brute_result,

            "branch_bound":
                bb_result,

            "comparison": {

                "search_reduction_percent":
                    search_reduction,

                "same_optimal_solution":
                    same_solution,

                "remaining_capacity":
                    remaining_capacity
            }

        })


    # ====================================
    # ERROR HANDLING
    # ====================================

    except KeyError as error:

        return jsonify({
            "error":
                f"Missing required field: {error}"
        }), 400

    except ValueError:

        return jsonify({
            "error":
                "Capacity, weight and value must be valid numbers."
        }), 400

    except Exception as error:

        return jsonify({
            "error":
                str(error)
        }), 500


# ========================================
# START FLASK SERVER
# ========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )