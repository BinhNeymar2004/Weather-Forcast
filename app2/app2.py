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
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()

        # Tạo query ban đầu
        query = db.collection("EnvironmentData")

        # Nếu có ID thì lọc theo ID
        if search_id:
            query = query.where("ID", "==", search_id)

        # Nếu có khoảng ngày thì lọc thêm
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                # end_dt tăng thêm 1 ngày để lấy hết dữ liệu trong ngày cuối
                end_dt = end_dt.replace(hour=23, minute=59, second=59)

                query = query.where("time", ">=", start_dt).where("time", "<=", end_dt)
            except ValueError:
                pass  # Nếu nhập sai định dạng ngày thì bỏ qua

        # Lấy dữ liệu từ Firestore
        docs = query.stream()
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
