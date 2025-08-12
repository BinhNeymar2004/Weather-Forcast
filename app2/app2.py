from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

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
    results = []
    if request.method == "POST":
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
                ts = data.get("time")
                if hasattr(ts, "strftime"):  # datetime
                    data["time"] = ts.strftime("%Y-%m-%d %H:%M:%S")
                elif hasattr(ts, "to_datetime"):  # Firestore timestamp object
                    data["time"] = ts.to_datetime().strftime("%Y-%m-%d %H:%M:%S")

                results.append(data)

    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(port=5002, debug=True)