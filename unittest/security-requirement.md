# Security Requirements

## SR1
`json_search()` phải kiểm tra quyền truy cập theo `role` dựa trên `policy.py`.

## SR2
Nếu role không đủ quyền, hàm phải trả về `[]`.

## SR3
Nếu role được phép và key tồn tại, hàm phải trả về kết quả tìm kiếm.

## SR4
Role không hợp lệ không được truy cập dữ liệu nhạy cảm.

## SR5
Sau khi thêm kiểm soát quyền, chức năng tìm kiếm ban đầu vẫn phải hoạt động đúng.
