Automation với web và request.
Automation với web. Sẽ kết hợp với playwright để automation.


user -> API -> Server
Server -> API -> user

Automation với request.
Cấu trúc 1 request API sẽ bao gồm:
- Phương thức API: GET, POST, PUT, PATCH, DELETE, …
- URL API: Sẽ là 1 url được bắt đầu bởi HTTP/HTTPS
- Headers: Thường là sẽ chưa những key xác thực, và những thông tin quan trong.
- Body: Nó sẽ chưa những thông tin mình cần đưa lên server
- Params: Nó sẽ chưa những thông tin không quan trong hoặc những thông tin đê theo dõi.

Cấu trúc response của 1 API:
- Nó có thể là 1 trang html
- Nó có thể là 1 đoạn json
- Nó có thể là 1 đoạn text
- Nó có thể là 1 chuỗi binary (bytes) (hình ảnh hoặc video)
- Nó có thể là định dạng urlencoded