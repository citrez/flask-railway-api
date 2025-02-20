from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL configuration from Railway environment variables
DB_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DB_URL)

@app.route('/update_record', methods=['POST'])
def update_record():
    data = request.json
    record_id = data.get('id')
    new_price = data.get('price')

    if not record_id or not new_price:
        return jsonify({"error": "Missing 'id' or 'price'"}), 400

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE whiskey_prices SET price = %s WHERE id = %s",
            (new_price, record_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Record updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
