from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ================== NGUỒN DỮ LIỆU ==================
SOURCE_URL = "https://wtxmd52.tele68.com/v1/txmd5/sessions"


# ================== THUẬT TOÁN DỰ ĐOÁN CHUẨN (VOTE AI) ==================
def algo_vote_max_v3(history):
    if len(history) < 10:
        return {"prediction": "Tài", "confidence": 55}

    # ========= 9 thuật toán con =========
    def weighted_recent(h):
        w_t = sum((i+1)/len(h) for i,v in enumerate(h[-10:]) if v=="Tài")
        w_x = sum((i+1)/len(h) for i,v in enumerate(h[-10:]) if v=="Xỉu")
        return "Tài" if w_t >= w_x else "Xỉu"

    def long_chain_reverse(h):
        last = h[-1]
        chain = 1
        for v in reversed(h[:-1]):
            if v == last:
                chain += 1
            else:
                break
        return "Xỉu" if last=="Tài" and chain>=3 else ("Tài" if last=="Xỉu" and chain>=3 else last)

    def alternation(h):
        flips = sum(1 for i in range(1, 6) if h[-i]!=h[-i-1])
        return "Tài" if flips >= 4 and h[-1]=="Xỉu" else ("Xỉu" if flips >=4 else h[-1])

    def pattern_repeat(h):
        for size in range(2, min(6, len(h)//2)+1):
            a = "".join(h[-size:])
            b = "".join(h[-2*size:-size])
            if a == b:
                return h[-size]
        return weighted_recent(h)

    def momentum(h):
        t = h[-5:].count("Tài")
        return "Tài" if t>=3 else "Xỉu"

    def rebound(h):
        if len(h)<5: return "Tài"
        if h[-1]!=h[-2] and h[-3]==h[-4]:
            return h[-3]
        return h[-1]

    def volatility(h):
        flips = sum(1 for i in range(1, len(h)) if h[i]!=h[i-1])
        ratio = flips / len(h)
        return "Tài" if ratio < 0.45 else "Xỉu" if ratio > 0.55 else ("Xỉu" if h[-1]=="Tài" else "Tài")

    def entropy(h):
        t = h.count("Tài")
        x = len(h) - t
        diff = abs(t - x)
        if diff <= len(h)//6:
            return "Tài" if h[-1]=="Xỉu" else "Xỉu"
        return "Tài" if t > x else "Xỉu"

    def trend_lock(h):
        recent = h[-8:]
        if recent.count("Tài")>=6: return "Tài"
        if recent.count("Xỉu")>=6: return "Xỉu"
        return "Tài" if h[-1]=="Xỉu" else "Xỉu"

    # ========= Gộp & gán trọng số =========
    algos = [weighted_recent, long_chain_reverse, alternation, pattern_repeat,
             momentum, rebound, volatility, entropy, trend_lock]

    votes = []
    weights = []

    for fn in algos:
        vote = fn(history)
        votes.append(vote)

        # Trọng số động: thuật toán nào “đoán đúng” nhiều trong 10 lần gần nhất thì được điểm cao
        past_score = 0
        for i in range(2, min(len(history), 12)):
            sub = history[:-i]
            if len(sub) < 8:
                break
            if fn(sub) == history[-i+1]:
                past_score += 1
        weights.append(max(1, past_score/3))

    # Tổng hợp phiếu
    total_T = sum(w for v,w in zip(votes,weights) if v=="Tài")
    total_X = sum(w for v,w in zip(votes,weights) if v=="Xỉu")

    prediction = "Tài" if total_T > total_X else "Xỉu"
    confidence = int((abs(total_T - total_X) / (total_T + total_X)) * 100 + 60)
    confidence = min(confidence, 95)  # không bao giờ vượt 95%

    return {
        "prediction": prediction,
        "confidence": confidence
    }


# ================== API TRẢ KẾT QUẢ ==================
@app.route("/api/taixiumd5", methods=["GET"])
def get_prediction():
    try:
        res = requests.get(SOURCE_URL, timeout=10)
        data = res.json()

        if "list" not in data or len(data["list"]) < 10:
            return jsonify({"error": "Không đủ dữ liệu"}), 400

        # Lấy 15 phiên gần nhất
        history_raw = data["list"][:15]
        history = ["Tài" if item["resultTruyenThong"].upper() == "TAI" else "Xỉu" for item in history_raw]

        # Dự đoán dựa trên lịch sử
        result = algo_vote_max_v3(history)
        du_doan = result["prediction"]
        do_tin_cay = result["confidence"]

        # Phiên mới nhất
        newest = data["list"][0]
        dices = newest.get("dices", [0, 0, 0])
        total = sum(dices)
        phien = newest.get("id", 0)

        return jsonify({
            "id": "tuananhdz",
            "phien": phien,
            "xuc_xac_1": dices[0],
            "xuc_xac_2": dices[1],
            "xuc_xac_3": dices[2],
            "tong": total,
            "du_doan": du_doan,
            "do_tin_cay": do_tin_cay
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================== CHẠY SERVER ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
