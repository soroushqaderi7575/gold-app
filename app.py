from flask import Flask, request, render_template_string
import requests
import re
import os

app = Flask(__name__)

URL = "https://www.tgju.org/profile/geram18"


# ---------------- گرفتن قیمت ----------------
def get_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        html = r.text

        m = re.search(r"نرخ فعلی[:\s]*([\d,]+)", html)

        if m:
            return int(m.group(1).replace(",", ""))

    except:
        return None

    return None


# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gold App</title>
</head>

<body style="font-family:tahoma;text-align:center;margin-top:40px;">

<h2>💰 قیمت طلای ۱۸ عیار</h2>

<h1>{{price}}</h1>

<form method="post" action="/calc">

    <input name="A" placeholder="اجرت %" style="padding:10px;width:200px;"><br><br>
    <input name="S" placeholder="سود % (پیشفرض 7)" style="padding:10px;width:200px;"><br><br>
    <input name="T" placeholder="مالیات % (پیشفرض 10)" style="padding:10px;width:200px;"><br><br>
    <input name="W" placeholder="وزن (گرم)" style="padding:10px;width:200px;"><br><br>

    <button style="padding:10px 20px;">محاسبه</button>

</form>

</body>
</html>
"""


# ---------------- صفحه اصلی ----------------
@app.route("/")
def home():
    price = get_price()

    if price is None:
        price = "نامشخص"

    return render_template_string(HTML, price=price)


# ---------------- محاسبه ----------------
@app.route("/calc", methods=["POST"])
def calc():

    price = get_price()
    if price is None:
        return "قیمت در دسترس نیست"

    A = float(request.form.get("A") or 0)
    S = float(request.form.get("S") or 7)
    T = float(request.form.get("T") or 10)
    W = float(request.form.get("W") or 0)

    A_val = price * (A / 100)
    S_val = (price + A_val) * (S / 100)
    T_val = (A_val + S_val) * (T / 100)

    per_gram = price + A_val + S_val + T_val
    total = per_gram * W

    return f"""
    <h2>نتیجه</h2>
    <p>قیمت هر گرم: {int(per_gram)}</p>
    <p>قیمت کل: {int(total)}</p>
    <br><a href="/">برگشت</a>
    """


# ---------------- مهم برای Render ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
