BÁO CÁO ỨNG DỤNG TRA CỨU VÀ LỌC DỮ LIỆU MÔI TRƯỜNG TỪ FIREBASE
1. Mục tiêu
Xây dựng một ứng dụng web cho phép:
- Lấy dữ liệu môi trường (ID trạm, tên trạm, thời gian, nhiệt độ, độ ẩm, tốc độ gió, áp suất) từ cơ sở dữ liệu Firebase Firestore.
- Cho phép người dùng tìm kiếm dữ liệu theo ID hoặc tên trạm.
- Bổ sung chức năng lọc dữ liệu theo ngày để thu hẹp kết quả.
- Hiển thị dữ liệu trên bảng giao diện web theo thời gian thực, bao gồm cả cột Time từ DB.
2. Công nghệ sử dụng
- Ngôn ngữ lập trình: Python (Flask Framework).
- Frontend: HTML, CSS (Bootstrap).
- Cơ sở dữ liệu: Firebase Firestore.
- Thư viện hỗ trợ Firebase:
- firebase_admin (kết nối Python với Firebase).
- google-cloud-firestore (truy vấn dữ liệu Firestore).
- Triển khai lọc ngày: Sử dụng truy vấn kết hợp (where) và chỉ mục (index) trong Firestore.
3. Quy trình thực hiện
Bước 1: Kết nối Firebase
- Tạo project trên Firebase Console.
- Tải file serviceAccountKey.json và cấu hình kết nối trong Python:
- cred = credentials.Certificate("serviceAccountKey.json")
- firebase_admin.initialize_app(cred)
- db = firestore.client()
Bước 2: Truy vấn dữ liệu
- Lấy dữ liệu từ collection EnvironmentData trên Firestore.
- Nếu người dùng nhập từ khóa tìm kiếm → dùng where() để lọc.
- Nếu người dùng chọn ngày → chuyển ngày sang dạng datetime và truy vấn với điều kiện >= và <.
Bước 3: Hiển thị dữ liệu
- Dữ liệu trả về được render ra file HTML thông qua Flask render_template.
- Bảng hiển thị đầy đủ các cột:
- ID, Name, Time, Temperature, Humidity, Wind, Pressure.
4. Kết quả đạt được
Ứng dụng đã kết nối thành công với Firebase Firestore.
Cho phép tìm kiếm dữ liệu môi trường theo ID hoặc tên trạm.
Cho phép lọc theo ngày hoạt động đúng.
Bảng hiển thị đầy đủ dữ liệu từ Firestore, bao gồm thời gian (Time).
Dữ liệu được lấy theo thời gian thực.
App1:
<img width="1864" height="913" alt="image" src="https://github.com/user-attachments/assets/90883ac3-7ab0-4352-9094-2b5ea7704968" />
App2:
<img width="1866" height="909" alt="image" src="https://github.com/user-attachments/assets/73232115-611e-4227-9eb8-1f92c8cdad67" />
Trang thống kê:
<img width="1862" height="916" alt="image" src="https://github.com/user-attachments/assets/06e1411f-d8b4-4e0a-9851-c2bec40e5427" />

