# Security Requirements

## SR1 - Kiểm tra quyền truy cập theo role

Hàm json_search() phải kiểm tra role của người dùng trước khi trả về
giá trị của một trường dữ liệu.

Việc kiểm tra quyền phải dựa trên các chính sách được định nghĩa
trong policy.py.

## SR2 - Không trả về dữ liệu khi không đủ quyền

Nếu role của người dùng không được phép truy cập một trường dữ liệu,
json_search() phải trả về danh sách rỗng và không được làm lộ giá trị
của trường đó.

## SR3 - Bảo vệ dữ liệu nhạy cảm

Các trường dữ liệu nhạy cảm như API key, thông tin xác thực,
thông tin SNMP hoặc các dữ liệu được đánh dấu hạn chế trong policy.py
chỉ được trả về cho các role được phép truy cập.

## SR4 - Role không hợp lệ không được truy cập dữ liệu nhạy cảm

Nếu role truyền vào không tồn tại hoặc không hợp lệ, hệ thống không
được trả về dữ liệu nhạy cảm.

## SR5 - Không làm thay đổi chức năng tìm kiếm ban đầu

Sau khi bổ sung cơ chế kiểm soát truy cập, json_search() vẫn phải đảm
bảo chức năng tìm kiếm đệ quy hoạt động chính xác trên các dict và list.

Các chức năng ban đầu phải tiếp tục hoạt động:
- Tìm thấy key thì trả về kết quả.
- Không tìm thấy key thì trả về danh sách rỗng.
- Kết quả trả về phải có kiểu list.
