from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# Kết nối Firebase
cred = credentials.Certificate("C:/Dich Vu Ket Noi/Buoi2/quanlylop-f00c2-firebase-adminsdk-fbsvc-8bf5f19693.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Lấy thời gian thực từ server
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "ID": request.form.get("id", "").strip(),
            "Name": request.form.get("name", "").strip(),
            "Time": current_time,
            "Temperature": float(request.form.get("temperature", 0)),
            "Humidity": float(request.form.get("humidity", 0)),
            "Wind": float(request.form.get("wind", 0)),
            "Pressure": float(request.form.get("pressure", 0))
        }

        db.collection("EnvironmentData").add(data)
        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
