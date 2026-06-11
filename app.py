from flask import Flask, render_template_string
import requests
import re

app = Flask(__name__)

URL = "https://www.tgju.org/profile/geram18"


def get_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        html = r.text

        m = re.search(r"نرخ فعلی[:\s]*([\d,]+)", html)

        if m:
            return m.group(1)

    except:
        pass

    return "نامشخص"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Gold App</title>
</head>
<body style="font-family:tahoma;text-align:center;margin-top:50px;">

<h2>قیمت طلای ۱۸ عیار</h2>

<h1>{{price}}</h1>

<form method="post" action="/calc">
    اجرت %: <input name="A"><br><br>
    سود % (7 پیشفرض): <input name="S"><br><br>
    مالیات % (10 پیشفرض): <input name="T"><br><br>
    وزن (گرم): <input name="W"><br><br>

    <button type="submit">محاسبه</button>
</form>

</body>
</html>
"""


@app.route("/")
def home():
    price = get_price()
    return render_template_string(HTML, price=price)


@app.route("/calc", methods=["POST"])
def calc():
    from flask import request

    price = int(get_price().replace(",", ""))

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
    app.run()