from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/api/taixiu", methods=["GET"])
def taixiu():
    api_url = "https://sunwintxnhahaha-1mw9.onrender.com/api/taixiu/sunwin"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()  # dữ liệu từ API gốc

        result = []
        # Nếu data là dict, chuyển thành list để loop
        items = data if isinstance(data, list) else [data]

        for item in items:
            phien = item.get("Phien", "N/A")
            x1 = int(item.get("Xuc_xac1", 0))
            x2 = int(item.get("Xuc_xac2", 0))
            x3 = int(item.get("Xuc_xac3", 0))
            tong = int(item.get("Tong", x1 + x2 + x3))
            du_doan = item.get("Du_doan", "N/A")
            id_phu = item.get("id", "N/A")

            result.append({
                "Phiên": phien,
                "Xúc xắc 1": x1,
                "Xúc xắc 2": x2,
                "Xúc xắc 3": x3,
                "Tổng": tong,
                "Dự đoán": du_doan
              
            })

        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({"error": "Lỗi khi gọi API gốc", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
