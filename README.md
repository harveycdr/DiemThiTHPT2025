# 🎓 Quá trình phân tích lấy dữ liệu điểm thi THPT quốc gia 2025

## 🛠️ Công nghệ sử dụng
- Python (requests)
## 🛠️ Môi trường sử dụng
- VScode, Command Prompt, Excel

## 🚀 Tính năng
- Tổng hợp điểm thi của tất cả thí sinh tham gia thi THPT của các tỉnh thành ở Việt Nam

## Các bước thực hiện

### Tìm số báo danh
- Được biết số báo danh của các thí sinh gồm 6 chữ số
`XX YYYYYY`

- Với `XX` là mã hội đồng (được biết từ 01-65 bao gồm 64 tỉnh thành và mã 65 là Cục Nhà trường - Bộ Quốc phòng).

![Ảnh tìm kiếm cấu trúc sbd dự thi](/images/img1.png)

### Tìm trang web để lấy điểm thi
- Soạn `Tra cứu điểm thi THPT quốc gia` tìm trên google một website tra cứu.

- Lựa chọn trang web đê tra cứu
![Lựa chọn trang web đê tra cứu](/images/img2.png)
Lựa chọn trang [tuổi trẻ online](https://tuoitre.vn/diem-thi.htm). 

Bởi vì, giao diện trang đơn giản và dễ dùng và không có mã capcha.

### Tra cứu
- Chọn ngẫu nhiên một sbd để tra cứu
49000001 là người dự thi số 1 thi ở hội đồng thi Long An.

![Kết quả tra cứu](/images/img3.png)

- Kiểm tra trang web nhận thấy

Khi mở devtool (f12) tab network nhập lại sbd để tra cứu thì trình duyệt sẽ gửi đi một api

![Kết quả tra cứu](/images/img4.png)

![Copy url](/images/img5.png)

url sau khi sau chép 
`https://s6.tuoitre.vn/api/diem-thi-thpt.htm?sbd=49000001&year=2025`

Nhận thấy url trên bao gồm tên miền và 2 phần query

2 phần query này là sbd và năm thi.

### Kiểm thử trên cmd
- Thử dùng lệnh curl để call url trên

`curl https://s6.tuoitre.vn/api/diem-thi-thpt.htm?sbd=49000001&year=2025`

- Kết quả trả về nhanh chóng trên cmd

![Kết quả trả về](/images/img6.png)

Phần trả về là một dạng json rất thích hợp để dùng python phân tích

### Dùng python để lấy tất cả điểm thi lưu vào file .csv (excel)

- Tạo một file python để thực thi

- Dùng thư viện subprocess để gọi url

```
# Gọi curl bằng requests
url = f"https://s6.tuoitre.vn/api/diem-thi-thpt.htm?sbd={sbd}&year=2025"

  try:
    r = requests.get(url, timeout=10)

    # Trường hợp lấy dữ liệu thành công
    if r.status_code == 200 and r.text.strip():
      d = r.json()
      if d.get("total") == 1:
        return True, lay_diem(d["data"][0])
  except:
    ...
```

![Kết quả ](/images/img7.png)

Kết quả trả về đúng mong đợi.

- Phát triển thành hàm để gọi trả về dữ liệu điểm các môn thi.

![Kết quả ](/images/img8.png)

- Dùng vòng lặp để chạy theo mã tỉnh và sbd

```
# số báo danh = XXYYYYYY, XX 1-65, YYYYYY 10^6
#01 là mã tỉnh ở Hà Nội, 124600 là số thí sinh (Có thể không chính xác)
sbd_list = [f"{1:02}{i:06}" for i in range(1, 124600 + 1)]

for sbd in sbd_list:
  fetch_diem_thi(sbd)

```

- Mở file .csv để lưu điểm thi

```
#Mở file csv và ghi vào cuối file
f = open("diemthiHaNoi.csv", mode="a", encoding="utf-8")

for sbd in sbd_list:
  diemthi = fetch_diem_thi(sbd)
  f.write(diemthi)
# f.close() khi ghi xong
```

**Kết quả cuối có được file csv điểm thi THPT 2025**

![Kết quả ](/images/img9.png)

Khi thu thập đủ có thể phần tích dữ liệu điểm thi

### Một số lưu ý

- Điểm thi -1 nghĩa là học sinh không thi môn đó.
- Ta có thể dùng **thread** để gọi nhiều nhiều lần `fetch_diem_thi()`.
- Khi dùng **thread** có thể nhận được mã lỗi từ server `429`. Điều này nghĩa là ta đã gửi quá nhiều requests. Nên cân nhắc việc thêm điều kiện để dừng hoặc dùng `time.sleep()` để chờ sau đó tiếp tục gửi requests.
- Khi nhận được dữ liệu điểm thi dạng `json`. Ta nên nhìn vào trường `STT` thay vì `Số báo danh (Id)` để biết dữ liệu có liền mạch hay không. ![Người không thi sẽ được bỏ qua và code không có lỗi ](/images/img10.png)  


### Phân tích dữ liệu
...
