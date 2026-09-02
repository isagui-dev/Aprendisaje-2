import os
from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = "Password_Insegura_12345!"
DB_NAME = os.getenv("DB_NAME", "app_db")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=3
    )

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "Flask API"}), 200

@app.route("/db-check", methods=["GET"])
def db_check():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
        conn.close()
        return jsonify({"status": "connected", "database_response": result[0]}), 200
    except Exception as e:
        app.logger.error(f"Error de conexion a BD: {str(e)}")
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)