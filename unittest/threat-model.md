# Threat Model

## Actor / Role
- admin: quyền quản trị.
- operator: quyền vận hành.
- viewer: quyền xem hạn chế.

## Asset cần bảo vệ
- API key.
- Thông tin xác thực.
- Thông tin thiết bị và dữ liệu nhạy cảm khác.

## Trust Boundary
`json_search()` phải kiểm tra role trước khi trả dữ liệu.
Không được mặc định mọi role đều có quyền truy cập mọi trường.

## Threats

### Information Disclosure
Role không đủ quyền có thể đọc dữ liệu nhạy cảm nếu hàm không kiểm tra quyền.

### Elevation of Privilege
Role quyền thấp có thể truy cập dữ liệu dành cho role quyền cao hơn.

### Invalid Role
Role không hợp lệ không được phép truy cập dữ liệu nhạy cảm.
