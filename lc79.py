from flask import Flask, jsonify
import requests

app = Flask(__name__)

SOURCE_URL = "https://wtxmd52.tele68.com/v1/txmd5/sessions"


# ================== 10 THUẬT TOÁN DỰ ĐOÁN MỚI ==================
def algo_bet(history):
    if len(history) < 3:
        return "Tài"
    streak = 1
    for i in range(len(history)-1, 0, -1):
        if history[i] == history[i-1]:
            streak += 1
        else:
            break
    if streak >= 3:
        return history[-1]
    return "Tài" if history[-1] == "Xỉu" else "Xỉu"


def algo_dao(history):
    if len(history) < 6:
        return "Xỉu"
    flips = sum(1 for i in range(1, 6) if history[-i] != history[-i-1])
    if flips >= 4:
        return "Tài" if history[-1] == "Xỉu" else "Xỉu"
    return history[-1]


def algo_2_1(history):
    if len(history) < 6:
        return "Tài"
    last6 = history[-6:]
    pattern = "".join("T" if x == "Tài" else "X" for x in last6)
    if pattern.endswith("TTX") or pattern.endswith("XXT"):
        return history[-1]
    return "Tài" if history[-1] == "Xỉu" else "Xỉu"


def algo_xenke(history):
    if len(history) < 5:
        return "Tài"
    alternating = all(history[i] != history[i-1] for i in range(-1, -5, -1))
    if alternating:
        return "Tài" if history[-1] == "Xỉu" else "Xỉu"
    return history[-1]


def algo_gay(history):
    if len(history) < 7:
        return "Xỉu"
    middle = len(history) // 2
    left = history[:middle]
    right = history[middle:]
    if left[-1] != right[0]:
        return right[-1]
    return history[-1]


def algo_de(history):
    if len(history) < 3:
        return "Tài"
    last3 = history[-3:]
    return "Tài" if last3.count("Tài") > last3.count("Xỉu") else "Xỉu"


def algo_repeat(history):
    if len(history) < 6:
        return "Xỉu"
    return history[-3] if history[-6:-3] == history[-3:] else ("Tài" if history[-1] == "Xỉu" else "Xỉu")


def algo_dao_kep(history):
    if len(history) < 4:
        return "Tài"
    flips = [history[-i] != history[-i-1] for i in range(1, 4)]
    if flips.count(True) >= 2:
        return "Tài" if history[-1] == "Xỉu" else "Xỉu"
    return history[-1]


def algo_chuoi(history):
    if len(history) < 8:
        return "Tài"
    last = history[-1]
    streak = 1
    for i in range(len(history)-2, -1, -1):
        if history[i] == last:
            streak += 1
        else:
            break
    return last if streak >= 3 else ("Tài" if last == "Xỉu" else "Xỉu")


def algo_smart_mix(history):
    if len(history) < 6:
        return "Tài"
    weights = {
        "bet": 1.2 if history[-1] == history[-2] else 0.8,
        "dao": 1.1 if history[-1] != history[-2] else 0.9,
        "de": 1.3 if history[-3:].count("Tài") > history[-3:].count("Xỉu") else 0.7,
    }
    score_tai = weights["bet"] + weights["de"]
    score_xiu = weights["dao"] + (2 - weights["de"])
    return "Tài" if score_tai >= score_xiu else "Xỉu"


# ================== PHÂN TÍCH DỰ ĐOÁN ==================
def du_doan_tu_lichsu(history):
    if len(history) < 4:
        return "Tài", 60

    algos = [
        algo_bet,
        algo_dao,
        algo_2_1,
        algo_xenke,
        algo_gay,
        algo_de,
        algo_repeat,
        algo_dao_kep,
        algo_chuoi,
        algo_smart_mix
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
@app.route("/", methods=["GET"])
def get_prediction():
    try:
        res = requests.get(SOURCE_URL, timeout=10)
        data = res.json()

        if "list" not in data or len(data["list"]) < 10:
            return jsonify({"error": "Không đủ dữ liệu"}), 400

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
