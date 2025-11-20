from flask import Flask, jsonify
import requests
import statistics

app = Flask(__name__)

# =========================================
# AI THUẬT TOÁN (20 thuật toán bạn gửi)
# =========================================

def ai1_frequency(history, totals):
    if len(history) < 6:
        return {"du_doan": "Tài", "do_tin_cay": 65.2}
    window = history[-6:]
    t = window.count("Tài")
    x = window.count("Xỉu")
    if t > x + 1:
        return {"du_doan": "Xỉu", "do_tin_cay": 88.3}
    if x > t + 1:
        return {"du_doan": "Tài", "do_tin_cay": 87.5}
    return {"du_doan": history[-1], "do_tin_cay": 73.4}

def ai2_parity_chain(history, totals):
    if len(totals) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 66.7}
    last5 = totals[-5:]
    evens = sum(1 for t in last5 if t % 2 == 0)
    if evens >= 4:
        return {"du_doan": "Xỉu", "do_tin_cay": 91.2}
    if evens <= 1:
        return {"du_doan": "Tài", "do_tin_cay": 90.4}
    return {"du_doan": "Tài" if totals[-1] >= 11 else "Xỉu", "do_tin_cay": 71.9}

def ai3_moving_avg(history, totals):
    if len(totals) < 4:
        return {"du_doan": "Tài", "do_tin_cay": 65.8}
    avg4 = sum(totals[-4:]) / 4
    if avg4 > 10.9:
        return {"du_doan": "Tài", "do_tin_cay": 85.6}
    if avg4 < 10.1:
        return {"du_doan": "Xỉu", "do_tin_cay": 84.8}
    return {"du_doan": history[-1], "do_tin_cay": 72.1}

def ai4_streak_detector(history, totals):
    if len(history) < 4:
        return {"du_doan": "Tài", "do_tin_cay": 64.3}
    last = history[-1]
    streak = 1
    for i in range(len(history) - 2, -1, -1):
        if history[i] == last:
            streak += 1
        else:
            break
    if streak >= 4:
        return {"du_doan": "Xỉu" if last == "Tài" else "Tài", "do_tin_cay": 92.8}
    return {"du_doan": last, "do_tin_cay": 70.5}

def ai5_alternating_pattern(history, totals):
    if len(history) < 6:
        return {"du_doan": "Tài", "do_tin_cay": 66.2}
    seq = "".join("T" if h == "Tài" else "X" for h in history[-6:])
    if seq.endswith(("TXTX", "XTXT")):
        next_pred = "Tài" if seq[-1] == "X" else "Xỉu"
        return {"du_doan": next_pred, "do_tin_cay": 89.4}
    return {"du_doan": history[-1], "do_tin_cay": 68.9}

def ai6_total_variability(history, totals):
    if len(totals) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 67.0}
    window = totals[-5:]
    mean = sum(window) / 5
    var = max(window) - min(window)
    if mean >= 11 and var <= 2:
        return {"du_doan": "Tài", "do_tin_cay": 87.2}
    if mean <= 10 and var <= 2:
        return {"du_doan": "Xỉu", "do_tin_cay": 86.6}
    return {"du_doan": history[-1], "do_tin_cay": 73.8}

def ai7_short_cycle(history, totals):
    if len(history) < 3:
        return {"du_doan": "Tài", "do_tin_cay": 61.7}
    tail = history[-3:]
    if tail[0] == tail[2] and tail[0] != tail[1]:
        return {"du_doan": tail[0], "do_tin_cay": 88.9}
    return {"du_doan": history[-1], "do_tin_cay": 70.3}

def ai8_even_bias_long(history, totals):
    if len(totals) < 8:
        return {"du_doan": "Tài", "do_tin_cay": 64.6}
    last8 = totals[-8:]
    evens = sum(1 for t in last8 if t % 2 == 0)
    if evens >= 6:
        return {"du_doan": "Xỉu", "do_tin_cay": 91.1}
    if evens <= 2:
        return {"du_doan": "Tài", "do_tin_cay": 90.7}
    return {"du_doan": "Tài" if totals[-1] >= 11 else "Xỉu", "do_tin_cay": 71.5}

def ai9_median_check(history, totals):
    if len(totals) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 65.1}
    med = statistics.median(totals[-5:])
    if med > 10.6:
        return {"du_doan": "Tài", "do_tin_cay": 84.3}
    return {"du_doan": "Xỉu", "do_tin_cay": 84.1}

def ai10_trend_slope(history, totals):
    if len(totals) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 63.7}
    slope = (totals[-1] - totals[-5]) / 4
    if slope >= 0.6:
        return {"du_doan": "Tài", "do_tin_cay": 89.6}
    if slope <= -0.6:
        return {"du_doan": "Xỉu", "do_tin_cay": 89.4}
    return {"du_doan": "Tài" if totals[-1] >= 11 else "Xỉu", "do_tin_cay": 72.2}

def ai11_weighted_vote(history, totals):
    if len(history) < 6 or len(totals) < 6:
        return {"du_doan": "Tài", "do_tin_cay": 66.4}
    tcount = history[-6:].count("Tài")
    mean6 = statistics.mean(totals[-6:])
    parity = sum(1 for t in totals[-6:] if t % 2 == 0)
    score = 0
    if tcount > 3: score += 1
    if mean6 >= 11: score += 1
    if parity <= 2: score += 1
    if score >= 2:
        return {"du_doan": "Tài", "do_tin_cay": 86.5}
    if score <= 0:
        return {"du_doan": "Xỉu", "do_tin_cay": 85.9}
    return {"du_doan": history[-1], "do_tin_cay": 74.2}

def ai12_recent_trend(history, totals):
    if len(history) < 3:
        return {"du_doan": "Tài", "do_tin_cay": 62.3}
    trend = history[-2:]
    if trend[0] == trend[1]:
        return {"du_doan": trend[0], "do_tin_cay": 80.6}
    return {"du_doan": history[-1], "do_tin_cay": 70.1}

def ai13_balance(history, totals):
    t = history.count("Tài")
    x = history.count("Xỉu")
    if abs(t - x) >= 5:
        return {"du_doan": "Xỉu" if t > x else "Tài", "do_tin_cay": 83.2}
    return {"du_doan": history[-1], "do_tin_cay": 71.6}

def ai14_gradient(history, totals):
    if len(totals) < 4:
        return {"du_doan": "Tài", "do_tin_cay": 63.4}
    grad = totals[-1] - totals[-4]
    if grad > 1.5:
        return {"du_doan": "Tài", "do_tin_cay": 87.3}
    if grad < -1.5:
        return {"du_doan": "Xỉu", "do_tin_cay": 87.0}
    return {"du_doan": history[-1], "do_tin_cay": 74.0}

def ai15_stability(history, totals):
    if len(totals) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 64.5}
    diff = max(totals[-5:]) - min(totals[-5:])
    if diff <= 2:
        return {"du_doan": "Xỉu", "do_tin_cay": 81.8}
    return {"du_doan": "Tài", "do_tin_cay": 75.3}

def ai16_flip_after_loss(history, totals, win_log=[]):
    if len(win_log) > 0 and not win_log[-1]:
        return {"du_doan": "Xỉu" if history[-1] == "Tài" else "Tài", "do_tin_cay": 81.2}
    return {"du_doan": history[-1], "do_tin_cay": 72.6}

def ai17_recent_variance(history, totals):
    if len(totals) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 66.1}
    var = max(totals[-5:]) - min(totals[-5:])
    return {"du_doan": "Tài" if var > 4 else "Xỉu", "do_tin_cay": 78.8}

def ai18_sequence(history, totals):
    if len(history) < 5:
        return {"du_doan": "Tài", "do_tin_cay": 64.9}
    seq = "".join("T" if h == "Tài" else "X" for h in history[-5:])
    if seq in ["TTTTT", "XXXXX"]:
        return {"du_doan": "Xỉu" if history[-1] == "Tài" else "Tài", "do_tin_cay": 89.9}
    return {"du_doan": history[-1], "do_tin_cay": 70.9}

def ai19_long_term_mean(history, totals):
    if len(totals) < 10:
        return {"du_doan": "Tài", "do_tin_cay": 65.7}
    mean10 = statistics.mean(totals[-10:])
    if mean10 > 11:
        return {"du_doan": "Tài", "do_tin_cay": 84.7}
    if mean10 < 10:
        return {"du_doan": "Xỉu", "do_tin_cay": 83.9}
    return {"du_doan": history[-1], "do_tin_cay": 71.3}

def ai20_adaptive(history, totals):
    if len(history) < 8:
        return {"du_doan": "Tài", "do_tin_cay": 66.5}
    ratio = history[-8:].count("Tài") / 8
    if ratio > 0.75:
        return {"du_doan": "Xỉu", "do_tin_cay": 90.6}
    if ratio < 0.25:
        return {"du_doan": "Tài", "do_tin_cay": 90.2}
    return {"du_doan": history[-1], "do_tin_cay": 72.4}


# Danh sách thuật toán gộp chung
algos = [
    ai1_frequency, ai2_parity_chain, ai3_moving_avg, ai4_streak_detector,
    ai5_alternating_pattern, ai6_total_variability, ai7_short_cycle,
    ai8_even_bias_long, ai9_median_check, ai10_trend_slope,
    ai11_weighted_vote, ai12_recent_trend, ai13_balance, ai14_gradient,
    ai15_stability, ai16_flip_after_loss, ai17_recent_variance,
    ai18_sequence, ai19_long_term_mean, ai20_adaptive
]

# =========================================
# API LẤY KẾT QUẢ THẬT + CHẠY AI
# =========================================

history = []   # Lưu lịch sử Tài/Xỉu
totals = []    # Lưu lịch sử tổng

@app.route("/api/taixiu", methods=["GET"])
def taixiu():

    try:
        # Lấy dữ liệu thật
        real_api = "http://163.61.111.170:3001"
        res = requests.get(real_api, timeout=5)
        data_real = res.json()

        ketqua = data_real.get("Ket_qua")
        tong = data_real.get("Tong")

        # Cập nhật lịch sử
        if ketqua:
            history.append(ketqua)
        if tong:
            totals.append(tong)

        # Chạy 20 AI
        votes = []
        for ai in algos:
            out = ai(history, totals)
            votes.append(out)

        # Chọn AI có độ tin cậy cao nhất
        best = max(votes, key=lambda x: x["do_tin_cay"])

        data = {
            "Phien": data_real.get("Phien"),
            "Xuc_xac_1": data_real.get("Xuc_xac_1"),
            "Xuc_xac_2": data_real.get("Xuc_xac_2"),
            "Xuc_xac_3": data_real.get("Xuc_xac_3"),
            "Tong": tong,
            "Ket_qua": ketqua,
            "du_doan": best["du_doan"],
            "do_tin_cay": best["do_tin_cay"],
            "id": "phú lỏ"
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": "Không lấy được dữ liệu thật", "chi_tiet": str(e)})


@app.route("/")
def home():
    return "API Tài Xỉu AI Python 3 đang chạy OK!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
