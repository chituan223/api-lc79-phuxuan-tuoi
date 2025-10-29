from flask import Flask, jsonify
import requests

app = Flask(__name__)

SOURCE_URL = "https://wtxmd52.tele68.com/v1/txmd5/sessions"


# ================== CÁC THUẬT TOÁN DỰ ĐOÁN ==================
def algo_alternate_pro(history):
    if len(history) < 6:
        return "Tài"
    flips = sum(1 for i in range(1, 6) if history[-i] != history[-i-1])
    if flips >= 4:
        return "Tài" if history[-1] == "Xỉu" else "Xỉu"
    return history[-1]


def algo_streak_lock(history):
    if len(history) < 5:
        return "Tài"
    streak = 1
    for i in range(len(history)-2, -1, -1):
        if history[i] == history[-1]:
            streak += 1
        else:
            break
    return history[-1] if streak >= 3 else ("Xỉu" if history[-1] == "Tài" else "Tài")


def algo_reversal(history):
    if len(history) < 5:
        return "Tài"
    if history[-1] == history[-2] == history[-3]:
        return "Xỉu" if history[-1] == "Tài" else "Tài"
    return history[-1]


def algo_short_trend(history):
    if len(history) < 8:
        return "Tài"
    last5 = history[-5:]
    if last5.count("Tài") >= 4:
        return "Tài"
    elif last5.count("Xỉu") >= 4:
        return "Xỉu"
    return "Tài" if history[-1] == "Xỉu" else "Xỉu"


def algo_cycle_balance(history):
    if len(history) < 10:
        return "Tài"
    last10 = history[-10:]
    ratio = last10.count("Tài") / 10
    if ratio > 0.65:
        return "Xỉu"
    elif ratio < 0.35:
        return "Tài"
    else:
        return history[-1]


def algo_pattern_mirror(history):
    if len(history) < 8:
        return "Tài"
    last4 = history[-4:]
    prev4 = history[-8:-4]
    if last4 == prev4:
        return "Xỉu" if history[-1] == "Tài" else "Tài"
    return history[-1]


def algo_symmetry(history):
    if len(history) < 6:
        return "Tài"
    if history[-1] == history[-3] and history[-2] == history[-4]:
        return "Xỉu" if history[-1] == "Tài" else "Tài"
    return history[-1]


def algo_trongso(history):
    if len(history) < 8:
        return "Tài"
    weights = [1, 2, 3, 4, 3, 2, 1, 1]
    score = sum(w if h == "Tài" else -w for h, w in zip(history[-8:], weights))
    if score > 5:
        return "Tài"
    elif score < -5:
        return "Xỉu"
    else:
        return "Tài" if history[-1] == "Xỉu" else "Xỉu"


def algo_cycle_reverse(history):
    if len(history) < 10:
        return "Tài"
    last10 = history[-10:]
    if last10[:5].count("Tài") > last10[5:].count("Tài"):
        return "Xỉu"
    else:
        return "Tài"


def algo_hybrid(history):
    if len(history) < 8:
        return "Tài"
    last6 = history[-6:]
    flips = sum(1 for i in range(1, 6) if last6[i] != last6[i-1])
    ratio_tai = last6.count("Tài") / 6
    if flips >= 4:
        pred = "Tài" if history[-1] == "Xỉu" else "Xỉu"
    elif ratio_tai > 0.66:
        pred = "Xỉu"
    elif ratio_tai < 0.33:
        pred = "Tài"
    else:
        pred = history[-1]
    return pred


# ================== PHÂN TÍCH DỰ ĐOÁN ==================
def du_doan_tu_lichsu(history):
    if len(history) < 4:
        return "Tài", 60

    algos = [
        algo_alternate_pro,
        algo_streak_lock,
        algo_reversal,
        algo_short_trend,
        algo_cycle_balance,
        algo_pattern_mirror,
        algo_symmetry,
        algo_trongso,
        algo_cycle_reverse,
        algo_hybrid
    ]

    results = [algo(history) for algo in algos]
    tai = results.count("Tài")
    xiu = results.count("Xỉu")

    if tai > xiu:
        return "Tài", int(60 + (tai - xiu) * 4)
    elif xiu > tai:
        return "Xỉu", int(60 + (xiu - tai) * 4)
    else:
        return history[-1], 65


# ================== API CHÍNH ==================
@app.route("/api/taixiumd5", methods=["GET"])
def get_prediction():
    try:
        res = requests.get(SOURCE_URL, timeout=10)
        data = res.json()

        if "list" not in data or len(data["list"]) < 10:
            return jsonify({"error": "Không đủ dữ liệu"}), 400

        # Lấy danh sách lịch sử gần nhất (10 phiên)
        history_raw = data["list"][:20]
        history = ["Tài" if item["resultTruyenThong"].upper() == "TAI" else "Xỉu" for item in history_raw]

        newest = data["list"][0]
        dices = newest.get("dices", [0, 0, 0])
        total = sum(dices)
        phien = newest.get("id", 0)

        du_doan, do_tin_cay = du_doan_tu_lichsu(history)

        return jsonify({
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)