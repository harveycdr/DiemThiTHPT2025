import json, time, threading, requests

fields = ["STT", "Id", "TOAN", "VAN", "LI", "HOA", "NGOAI_NGU", "SU", "DIA", "SINH", "GIAO_DUC_CONG_DAN", "TIN_HOC", "TONGDIEM"]

def lay_diem(d):
  line = ";".join(str(d[field]) for field in fields) + "\n"
  return line.replace("-1", "")

def run_thread(func, param_list, workers=10):
  def call(param, index, results):
    data = func(param)
    results[index] = data

  for i in range(0, len(param_list), workers):  # lấy 100 số báo danh
    sub_list = param_list[i:i+workers]
    threads = []
    results = [None for j in range(workers)]
    for index in range(len(sub_list)):
      param = sub_list[index]
      t = threading.Thread(target=call, args=(param, index, results))
      t.start()
      threads.append(t)

    # Đợi tất cả thread xong
    for t in threads:
      t.join()

    for item in results:
      yield item

def fetch_diem_thi(sbd: str) -> tuple:
  url = f"https://s6.tuoitre.vn/api/diem-thi-thpt.htm?sbd={sbd}&year=2025"

  try:
    r = requests.get(url, timeout=10)

    # Trường hợp lấy dữ liệu thành công
    if r.status_code == 200 and r.text.strip():
      d = r.json()
      if d.get("total") == 1:
        return True, lay_diem(d["data"][0])  # Giả sử bạn có hàm lay_diem để xử lý dữ liệu

    # Trường hợp bị giới hạn (quá nhiều request)
    if r.status_code == 429:
      time.sleep(1)  # Đợi 1 giây rồi thử lại
      return fetch_diem_thi(sbd)

    # Trường hợp không tìm thấy dữ liệu hoặc lỗi khác
    return False, (f"Không tìm thấy {sbd}", r.status_code)

  except Exception as ex:
    return False, (f"Lỗi: {ex}", getattr(r, "status_code", -1))
    

f = open("diemthHaNoi.csv", mode="a", encoding="utf-8")
sbd_list = [f"{1:02}{i:06}" for i in range(1, 124600 + 1)]

for r in run_thread(fetch_diem_thi, sbd_list):
  success, msg = r
  if success:
    print(msg, end="")
    f.write(msg)
  else:
    print(msg)
f.close()
