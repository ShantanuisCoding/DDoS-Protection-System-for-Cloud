from flask import Flask, jsonify
import pandas as pd
import joblib
import os
import subprocess
from sklearn.preprocessing import MinMaxScaler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model and scaler
MODEL_FILE = "ddos_model.pkl"
CSV_FILE = "traffic_log.csv"

if not os.path.exists(MODEL_FILE):
    print("[ERROR] Model file not found. Train the model first.")
    exit()

model = joblib.load(MODEL_FILE)

# Function to block IP using Windows Firewall
def block_ip(ip):
    try:
        # Using Windows PowerShell to block IP
        command = f'New-NetFirewallRule -DisplayName "Block IP {ip}" -Direction Inbound -Protocol TCP -LocalPort Any -RemoteAddress {ip} -Action Block'
        subprocess.run(['powershell', '-Command', command], check=True)
        print(f"IP {ip} has been blocked.")
    except subprocess.CalledProcessError:
        print(f"Failed to block IP {ip}")

@app.route("/detect_ddos", methods=["GET"])
def detect_ddos():
    # Check if traffic log file exists
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "Traffic log not found!"}), 404
    
    df = pd.read_csv(CSV_FILE)

    # Ensure "Size" column exists
    if "Size" not in df.columns:
        return jsonify({"error": "'Size' column missing in traffic log!"}), 400

    # Handle missing values
    df.dropna(subset=["Size"], inplace=True)

    # Apply MinMaxScaler (same as training)
    scaler = MinMaxScaler()
    df["Size"] = scaler.fit_transform(df[["Size"]])

    # Predict anomalies
    df["Anomaly"] = model.predict(df[["Size"]])

    # Identify malicious IPs
    bad_ips = df[df["Anomaly"] == -1]["Source"].unique().tolist()

    # Block malicious IPs securely using Windows Firewall
    for ip in bad_ips:
        block_ip(ip)

    return jsonify({"status": "DDoS Check Completed", "blocked_ips": bad_ips})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
