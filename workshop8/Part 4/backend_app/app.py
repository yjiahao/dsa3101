from flask import Flask, request, jsonify
import os
import MySQLdb
import pandas as pd

app = Flask(__name__)

def get_connection():
    return MySQLdb.connect(
            host="db",  
            user=os.getenv("MYSQL_USER"),
            passwd=os.getenv("MYSQL_PASSWORD"),
            db=os.getenv("MYSQL_DATABASE")
        )

@app.route("/add_data", methods=["POST"])
def add_data():
    content = request.get_json()
    json_data = content.get("data", [])
    df = pd.read_json(json_data, orient="records")
    
    conn = get_connection()
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO measurements (wing_width, wing_length, seq_id, time_sec, heli_id, group_id)
            VALUES (%s, %s, %s, %s, %s, %s)""", tuple(row))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/get_data", methods=["get"])
def get_data():
    group_id = request.args.get("group_id")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM measurements WHERE group_id = %s;", (group_id,))
    columns = [desc[0] for desc in cur.description]
    results = cur.fetchall()
    data = [dict(zip(columns, row)) for row in results]
    cur.close()
    conn.close()   
    return jsonify(data)

@app.route("/get_alldata", methods=["get"])
def get_alldata():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM measurements")
    columns = [desc[0] for desc in cur.description]
    results = cur.fetchall()
    data = [dict(zip(columns, row)) for row in results]
    cur.close()
    conn.close()   
    return jsonify(data)