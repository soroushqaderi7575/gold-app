from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# ---------------- گرفتن قیمت واقعی ----------------
def get_price():
    try:
        url = "https://call5.tgju.org/ajax.json?rev=2&items=geram18"
        r = requests.get(url, timeout=10)
        data = r.json()

        return int(data["items"]["geram18"]["p"])

    except:
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
    <input name="S" placeholder="سود % (7)" value="7" style="padding:10px;width:200px;"><br><br>
    <input name="T" placeholder="مالیات % (10)" value="10" style="padding:10px;width:200px;"><br><br>
    <input name="W" placeholder="وزن (گرم)" style="padding:10px;width:200px;"><br><br>

    <button style="padding:10px 20px;">محاسبه</button>

</form>

</body>
</html>
"""


@app.route("/")
def home():
    price = get_price()
    return render_template_string(HTML, price=price if price else "نامشخص")


@app.route("/calc", methods=["POST"])
def calc():
    price = get_price()

    if not price:
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
    <p>هر گرم: {int(per_gram)}</p>
    <p>کل: {int(total)}</p>
    <br><a href="/">برگشت</a>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
