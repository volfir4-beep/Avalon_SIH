from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# LANDING PAGE
# =========================================================

@app.route('/')
def index():
    return render_template('landing_page.html')


# =========================================================
# DASHBOARD
# =========================================================

@app.route('/dashboard')
def dashboard():

    # -----------------------------------------------------
    # TEMPORARY SYSTEM DATA
    # -----------------------------------------------------
    # For now these values are hard-coded.
    # Later we can replace this with SQLite/database data.
    # -----------------------------------------------------

    systems = [

        {
            "system_id": "SYS-001",
            "anomaly": 12.4,
            "normal": 87.6,
            "health": 94.6
        },

        {
            "system_id": "SYS-002",
            "anomaly": 7.8,
            "normal": 92.2,
            "health": 97.1
        },

        {
            "system_id": "SYS-003",
            "anomaly": 24.3,
            "normal": 75.7,
            "health": 81.5
        },

        {
            "system_id": "SYS-004",
            "anomaly": 3.2,
            "normal": 96.8,
            "health": 98.7
        },

        {
            "system_id": "SYS-005",
            "anomaly": 18.6,
            "normal": 81.4,
            "health": 88.3
        }

    ]

    # -----------------------------------------------------
    # DASHBOARD SUMMARY VALUES
    # -----------------------------------------------------

    total_systems = len(systems)

    # Temporary values
    total_anomalies = 12
    total_threats = 4
    uptime = 99.8

    return render_template(
        'dashboard.html',

        systems=systems,

        total_systems=total_systems,

        total_anomalies=total_anomalies,

        total_threats=total_threats,

        uptime=uptime
    )


# =========================================================
# SYSTEM DETAILS PAGE
# =========================================================

@app.route('/system/<system_id>')
def system_details(system_id):

    # -----------------------------------------------------
    # TEMPORARY SYSTEM DETAILS
    # -----------------------------------------------------
    # Later these values will be retrieved using system_id
    # from your database.
    # -----------------------------------------------------

    health_score = 94.6

    anomaly_percentage = 12.4


    # Temporary anomaly information

    anomaly_reason = (
        "The system has been flagged due to an abnormal "
        "deviation in temperature and pressure readings. "
        "The detected pattern indicates a possible "
        "multivariate inconsistency."
    )


    # Temporary anomaly weights

    anomaly_weights = {

        "freeze": 15,

        "spike": 30,

        "multivariate_inconsistency": 25,

        "noise_burst": 10,

        "drift": 20

    }


    return render_template(

        'system_details.html',

        system_id=system_id,

        health_score=health_score,

        anomaly_percentage=anomaly_percentage,

        anomaly_reason=anomaly_reason,

        anomaly_weights=anomaly_weights

    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == '__main__':

    app.run(
        debug=True
    )