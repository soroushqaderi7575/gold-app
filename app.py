from flask import Flask, request, render_template_string
from price import get_price
import os

app = Flask(__name__)


HTML = """
<h2>قیمت طلا</h2>
<h1>{{price}}</h1>
<p>{{status}}</p>

<form method="post" action="/calc">
<input name="W" placeholder="وزن"><br>
<button>محاسبه</button>
</form>
"""


@app.route("/")
def home():
    price, online, t = get_price()

    if price:
        if online:
            status = "🟢 آنلاین"
        else:
            status = f"🟡 آفلاین - {t}"
    else:
        status = "🔴 خطا"

    return render_template_string(HTML, price=price, status=status)


@app.route("/calc", methods=["POST"])
def calc():
    price, _, _ = get_price()

    if not price:
        return "no price"

    w = float(request.form.get("W") or 0)

    return f"total: {price * w}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
