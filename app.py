from flask import Flask, jsonify, request, render_template, redirect, url_for
import os

import pyodbc

app = Flask(__name__)

# -------------------------
# DB CONNECTION
# -------------------------

# The connection string is read from the environment so no machine names or
# credentials are stored in the repository. See .env.example.
DEFAULT_CONNECTION = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=ProactiveTQ;"
    "Trusted_Connection=yes;"
)


def get_db_connection():
    return pyodbc.connect(os.environ.get("PTQ_DB_CONNECTION", DEFAULT_CONNECTION))

# -------------------------
# HELPERS
# -------------------------

def format_ticket(row):
    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "category": row[3],
        "status": row[4],    
    }

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

# -------------------------
# GET ALL TICKETS
# -------------------------

@app.route("/tickets", methods=["GET"])
def get_tickets():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Tickets ORDER BY id DESC")
        rows = cursor.fetchall()

        tickets = [format_ticket(row) for row in rows]
        return jsonify(tickets)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# CREATE TICKET
# -------------------------

@app.route("/tickets", methods=["POST"])
def create_ticket():
    conn = None
    cursor = None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        status = data.get("status", "").strip()

        if not title or not description or not status:
            return jsonify({"error": "All fields are required"}), 400

        allowed_statuses = ["Open", "In Progress", "Resolved", "Closed", "Innovation"]
        if status not in allowed_statuses:
            return jsonify({"error": "Invalid status"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Tickets (title, description, status) VALUES (?, ?, ?)",
            (title, description, status)
        )
        conn.commit()

        return jsonify({"message": "Ticket created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# GET SINGLE TICKET
# -------------------------

@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Ticket not found"}), 404

        return jsonify(format_ticket(row))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# UPDATE TICKET
# -------------------------

@app.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    conn = None
    cursor = None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        status = data.get("status", "").strip()

        if not title or not description or not status:
            return jsonify({"error": "All fields are required"}), 400

        allowed_statuses = ["Open", "In Progress", "Resolved", "Closed", "Innovation"]
        if status not in allowed_statuses:
            return jsonify({"error": "Invalid status"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tickets WHERE id = ?", (ticket_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Ticket not found"}), 404

        cursor.execute("""
            UPDATE Tickets
            SET title = ?, description = ?, status = ?
            WHERE id = ?
        """, (title, description, status, ticket_id))

        conn.commit()

        return jsonify({"message": "Ticket updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# DELETE TICKET
# -------------------------

@app.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tickets WHERE id = ?", (ticket_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Ticket not found"}), 404

        cursor.execute("DELETE FROM Tickets WHERE id = ?", (ticket_id,))
        conn.commit()

        return jsonify({"message": "Ticket deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# ADD WORKLOG
# -------------------------

@app.route("/tickets/<int:ticket_id>/worklogs", methods=["POST"])
def add_worklog(ticket_id):
    conn = None
    cursor = None
    try:
        data = request.get_json()

        message = data.get("message", "").strip()
        if not message:
            return jsonify({"error": "Message required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO WorkLogs (ticket_id, message)
            VALUES (?, ?)
        """, (ticket_id, message))

        conn.commit()

        return jsonify({"message": "Worklog added"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# GET WORKLOGS
# -------------------------

@app.route("/tickets/<int:ticket_id>/worklogs", methods=["GET"])
def get_worklogs(ticket_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT message, created_at
            FROM WorkLogs
            WHERE ticket_id = ?
            ORDER BY created_at DESC
        """, (ticket_id,))

        rows = cursor.fetchall()

        worklogs = [
            {"message": row[0], "created_at": str(row[1])}
            for row in rows
        ]

        return jsonify(worklogs)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
