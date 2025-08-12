from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Kết nối Firebase
cred = credentials.Certificate(
    r"C:/Dich Vu Ket Noi/Buoi2/quanlylop-f00c2-firebase-adminsdk-fbsvc-8bf5f19693.json"
)
if not firebase_admin._apps:  # Tránh khởi tạo lại nếu đã connect
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    stats_data = {}
    
    if request.method == "POST":
        action = request.form.get("action", "search")  # Mặc định là "search"
        
        if action == "search":
            search_id = request.form.get("id", "").strip()
            if search_id:
                docs = (
                    db.collection("EnvironmentData")
                    .where("ID", "==", search_id)
                    .stream()
                )
                for doc in docs:
                    data = doc.to_dict()
                    # Chuyển Firestore Timestamp thành string
                    ts = data.get("Time")
                    if hasattr(ts, "strftime"):  # datetime
                        data["Time"] = ts.strftime("%Y-%m-%d %H:%M:%S")
                    elif hasattr(ts, "to_datetime"):  # Firestore timestamp object
                        data["Time"] = ts.to_datetime().strftime("%Y-%m-%d %H:%M:%S")
                    search_results.append(data)
        
        elif action == "stats":
            start_date = request.form.get("start_date", "").strip()
            end_date = request.form.get("end_date", "").strip()
            query = db.collection("EnvironmentData")
            if start_date and end_date:
                try:
                    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                    end_dt = end_dt.replace(hour=23, minute=59, second=59)
                    query = query.where("time", ">=", start_dt).where("Time", "<=", end_dt)
                except ValueError:
                    pass  # Nếu nhập sai định dạng ngày thì bỏ qua
            docs = query.stream()
            data_list = [doc.to_dict() for doc in docs]
            if data_list:
                df = pd.DataFrame(data_list)
                stats_data = {
                    "Temperature": {
                        "mean": df["Temperature"].mean(),
                        "max": df["Temperature"].max(),
                        "min": df["Temperature"].min(),
                    },
                    "Humidity": {
                        "mean": df["Humidity"].mean(),
                        "max": df["Humidity"].max(),
                        "min": df["Humidity"].min(),
                    },
                    "Wind": {
                        "mean": df["Wind"].mean(),
                        "max": df["Wind"].max(),
                        "min": df["Wind"].min(),
                    },
                    "Pressure": {
                        "mean": df["Pressure"].mean(),
                        "max": df["Pressure"].max(),
                        "min": df["Pressure"].min(),
                    }
                }

    return render_template("search.html", search_results=search_results, stats=stats_data)

if __name__ == "__main__":
    app.run(port=5002, debug=True)