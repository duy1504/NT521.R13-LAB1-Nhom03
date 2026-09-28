# Threat Model

## 1. Bối cảnh hệ thống
Hàm json_search() được sử dụng để tìm kiếm dữ liệu trong một đối tượng JSON
trả về từ API giám sát hạ tầng mạng.

Hệ thống có nhiều loại người dùng với quyền truy cập khác nhau:
- admin
- operator
- viewer

Do dữ liệu JSON có thể chứa các thông tin nhạy cảm, hàm json_search()
cần kiểm tra quyền của người dùng trước khi trả về kết quả.

## 2. Actor / Role

### admin
Người quản trị hệ thống, có quyền truy cập các thông tin quản trị và
các dữ liệu nhạy cảm cần thiết để quản lý hệ thống.

### operator
Người vận hành hệ thống, được phép truy cập các thông tin phục vụ
việc giám sát và vận hành nhưng có thể bị hạn chế đối với một số
dữ liệu nhạy cảm.

### viewer
Người dùng chỉ có quyền xem các thông tin thông thường và không được
phép truy cập các dữ liệu nhạy cảm.

## 3. Tài sản cần bảo vệ

Các dữ liệu cần được bảo vệ bao gồm:
- Thông tin định danh thiết bị.
- Thông tin cấu hình hệ thống.
- Khóa hoặc chuỗi xác thực.
- Thông tin xác thực SNMP.
- API key hoặc các trường dữ liệu nhạy cảm khác có trong JSON.

## 4. Trust Boundary

Trust boundary nằm giữa người dùng gọi hàm json_search() và dữ liệu
được hàm trả về.

Hàm không được mặc định tin rằng người gọi có quyền truy cập mọi
trường dữ liệu. Trước khi trả về một trường, hệ thống phải kiểm tra
role của người dùng theo policy được định nghĩa trong policy.py.

Nếu bỏ qua việc kiểm tra role, người dùng có quyền thấp có thể truy cập
các dữ liệu vượt quá quyền hạn của mình.

## 5. Các mối đe dọa

### Threat 1: Information Disclosure

Một người dùng có role viewer có thể gọi:

json_search("apiKey", data, role="viewer")

Nếu hàm không kiểm tra quyền truy cập, API key có thể bị trả về cho
người dùng không được phép xem.

Hậu quả:
- Rò rỉ thông tin nhạy cảm.
- Lộ thông tin xác thực.
- Kẻ tấn công có thể sử dụng thông tin bị lộ để thực hiện các hành vi
  tấn công tiếp theo.

Nhóm STRIDE:
Information Disclosure.

### Threat 2: Elevation of Privilege

Người dùng có quyền thấp như viewer có thể cố gắng truy cập các trường
chỉ dành cho admin hoặc operator.

Nếu json_search() không kiểm tra role trước khi trả kết quả, người dùng
có thể truy cập dữ liệu vượt quá quyền hạn của mình.

Hậu quả:
- Vượt qua cơ chế phân quyền.
- Người dùng có quyền thấp truy cập được dữ liệu dành cho quyền cao hơn.

Nhóm STRIDE:
Elevation of Privilege.
