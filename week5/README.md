# Week 5 - So sánh 3 phương thức phân trang

Trong bài này, hệ thống quản lý thư viện sử dụng 3 phương thức phân trang cho resource `books`:

- Page-based pagination
- Offset-limit pagination
- Cursor-based pagination

Mục đích là để so sánh cách hoạt động, ưu điểm, nhược điểm và trường hợp sử dụng của từng phương thức.

---

## 1. Page-based Pagination

### Cách hoạt động
Người dùng truyền số trang và số phần tử mỗi trang.

Ví dụ:

```http
GET /books/page-based?page=1&pageSize=3
```

Ý nghĩa:
- `page=1`: lấy trang đầu tiên
- `pageSize=3`: mỗi trang có 3 phần tử

### Ưu điểm
- Dễ hiểu, dễ sử dụng
- Phù hợp với giao diện có số trang: 1, 2, 3, ...
- Dễ cài đặt trong bài tập hoặc demo

### Nhược điểm
- Khi dữ liệu lớn thì hiệu năng không cao
- Nếu dữ liệu thay đổi liên tục, kết quả giữa các trang có thể bị lệch

### Khi nào nên dùng
- Bài tập cá nhân
- Demo
- Hệ thống nhỏ
- Giao diện có phân trang theo số trang

---

## 2. Offset-limit Pagination

### Cách hoạt động
Người dùng truyền vị trí bắt đầu và số lượng phần tử cần lấy.

Ví dụ:

```http
GET /books/offset-limit?offset=0&limit=3
```

Ý nghĩa:
- `offset=0`: bắt đầu từ phần tử đầu tiên
- `limit=3`: lấy 3 phần tử

Ví dụ khác:

```http
GET /books/offset-limit?offset=3&limit=3
```

Ý nghĩa:
- bỏ qua 3 phần tử đầu
- lấy 3 phần tử tiếp theo

### Ưu điểm
- Đơn giản, dễ cài đặt
- Phù hợp khi cần lấy dữ liệu theo vị trí
- Dễ hiểu với người mới học

### Nhược điểm
- Hiệu năng giảm khi `offset` lớn
- Có thể bị trùng hoặc thiếu dữ liệu nếu danh sách thay đổi trong lúc phân trang

### Khi nào nên dùng
- Dữ liệu không quá lớn
- Bài tập, demo, MVP
- Khi muốn phân trang đơn giản theo vị trí

---

## 3. Cursor-based Pagination

### Cách hoạt động
Người dùng truyền `cursor`, thường là id cuối cùng của trang trước, để lấy dữ liệu tiếp theo.

Ví dụ:

```http
GET /books/cursor?limit=3
```

Lần đầu chưa có cursor, hệ thống trả 3 phần tử đầu tiên.

Ví dụ tiếp:

```http
GET /books/cursor?cursor=3&limit=3
```

Ý nghĩa:
- lấy 3 phần tử có `id > 3`

### Ưu điểm
- Hiệu quả hơn khi dữ liệu lớn
- Ổn định hơn khi dữ liệu thay đổi liên tục
- Phù hợp với kiểu tải thêm dữ liệu như load more hoặc infinite scroll

### Nhược điểm
- Khó hiểu hơn 2 cách còn lại
- Khó nhảy trực tiếp đến trang số 5, 6, ...
- Cài đặt phức tạp hơn

### Khi nào nên dùng
- Hệ thống thực tế có nhiều dữ liệu
- Dữ liệu thay đổi thường xuyên
- Cần tối ưu hiệu năng

---

## 4. Bảng so sánh

| Phương thức | Cách truyền tham số | Dễ cài đặt | Dễ sử dụng | Hiệu năng dữ liệu lớn | Ổn định khi dữ liệu thay đổi |
|---|---|---|---|---|---|
| Page-based | `page`, `pageSize` | Cao | Cao | Trung bình / Thấp | Thấp |
| Offset-limit | `offset`, `limit` | Cao | Cao | Thấp | Thấp |
| Cursor-based | `cursor`, `limit` | Trung bình | Trung bình | Cao | Cao |

---

## 5. Kết luận

Trong bài này:

- **Page-based** phù hợp để trình bày bài tập vì dễ hiểu
- **Offset-limit** đơn giản và phổ biến trong các ví dụ cơ bản
- **Cursor-based** nâng cao hơn, phù hợp với hệ thống lớn và dữ liệu thay đổi thường xuyên

Với bài tập cá nhân môn học, có thể ưu tiên:
- Page-based
- Offset-limit

Cursor-based nên được dùng để thể hiện thêm sự hiểu biết và so sánh.

---

## 6. Các endpoint đã dùng

### Page-based

```http
GET /books/page-based?page=1&pageSize=3
```

### Offset-limit

```http
GET /books/offset-limit?offset=0&limit=3
```

### Cursor-based

```http
GET /books/cursor?limit=3
GET /books/cursor?cursor=3&limit=3
```