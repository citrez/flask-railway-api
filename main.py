from flask import Flask, request, jsonify
import psycopg2
import os
import logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


app = Flask(__name__)

# PostgreSQL configuration from Railway environment variables
DB_URL = os.getenv("DATABASE_URL")


def connect_db():
    return psycopg2.connect(DB_URL)


@app.route("/update_record", methods=["POST"])
def update_record():
    logging.info("test")
    data = request.json
    record_id = data.get("id")
    # new_price = data.get('action')

    if not record_id:
        return jsonify({"error": "Missing 'id' or 'price'"}), 400

    try:
        conn = connect_db()
        cursor = conn.cursor()
        logging.info("executing")
        cursor.execute(
            "UPDATE whiskey_hammer_live_auction SET action = %s WHERE id = %s", (1, record_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("done executing")
        return (
            jsonify({"status": "success", "message": "Record updated successfully"}),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/hello", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)
