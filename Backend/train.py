from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import joblib
import os

CSV_FILE = "traffic_log.csv"
MODEL_FILE = "ddos_model.pkl"

# Load captured traffic data
if not os.path.exists(CSV_FILE):
    print("[ERROR] No traffic log found. Exiting.")
    exit()

df = pd.read_csv(CSV_FILE)

# Check if "Size" column exists
if "Size" not in df.columns or df.empty:
    print("[ERROR] Traffic log is empty or missing 'Size' column. Exiting.")
    exit()

# Remove NaN values
df.dropna(subset=["Size"], inplace=True)

# Feature Scaling
scaler = MinMaxScaler()
df["Size"] = scaler.fit_transform(df[["Size"]])

# Load existing model if available
if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
    print("[INFO] Existing model loaded.")
else:
    model = IsolationForest(contamination=0.1)
    print("[INFO] New model created.")

# Train the Isolation Forest Model
df["Anomaly"] = model.fit_predict(df[["Size"]])

# Save updated model
joblib.dump(model, MODEL_FILE)
print("[+] Model saved successfully!")

# Save detected anomalies
df[df["Anomaly"] == -1].to_csv("suspicious_traffic.csv", index=False)
print("[+] Anomalies saved to suspicious_traffic.csv!")
