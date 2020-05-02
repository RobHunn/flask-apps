from flask import Flask, request, render_template, jsonify, url_for, session, redirect
from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.bitcoin import BtcConverter

app = Flask(__name__)
app.config["SECRET_KEY"] = '_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def base():
    """Show base.html."""
    c = CurrencyRates()
    x = c.get_rates("USD")
    res = {item: "{0:.2f}".format(round(x[item], 2)) for item in x}
    session["rates"] = res
    b = BtcConverter()
    bit = {}
    bit["bitcoin_usd"] = round(b.get_latest_price("USD"), 2)
    bit["bitcoin_eur"] = round(b.get_latest_price("EUR"), 2)
    bit["bitcoin_gbp"] = round(b.get_latest_price("GBP"), 2)
    cc = CurrencyCodes()
    bit["name_usd"] = cc.get_currency_name("USD")
    bit["name_eur"] = cc.get_currency_name("EUR")
    bit["name_gbp"] = cc.get_currency_name("GBP")
    bit["symbol"] = b.get_symbol()
    bit["symbol_eur"] = cc.get_symbol("EUR")
    bit["symbol_gbp"] = cc.get_symbol("GBP")
    session["bit"] = bit
    return render_template("base.html", rates=res, bit=bit)


@app.route("/current-rate", methods=["POST"])
def current():
    """Show current.html."""
    rate_sel = request.form["rate"]
    c = CurrencyRates()
    x = c.get_rates(rate_sel)
    res2 = {item: "{0:.2f}".format(round(x[item], 2)) for item in x}

    cc = CurrencyCodes()
    name = cc.get_currency_name(rate_sel)
    symbol = cc.get_symbol(rate_sel)
    return render_template(
        "current.html",
        rates=session.get("rates"),
        bit=session.get("bit"),
        rates2=res2,
        selected=rate_sel,
        name=name,
        symbol=symbol,
    )


@app.route("/convert", methods=["POST"])
def convert():
    """Show index.html."""
    c = CurrencyRates()
    amount = request.form.get('amount')
    rate_from = request.form.get('rate-from')
    rate_too = request.form.get('rate-too')

    cc = CurrencyCodes()
    name_from = cc.get_currency_name(rate_from)
    name_to = cc.get_currency_name(rate_too)
    symbol = cc.get_symbol(rate_too)

    if not amount:
        con_rate = "{0:.2f}".format(round(c.get_rate(rate_from, rate_too), 2))
        return render_template("convert.html", con_rate=con_rate, name_from=name_from, name_to=name_to, symbol=symbol, rates=session.get("rates"), bit=session.get("bit"))

    else:
        con_rate = "{0:.2f}".format(
            round(c.convert(rate_from, rate_too, amount), 2))
        return render_template("convert.html",
                               con_rate=con_rate, name_from=name_from,
                               name_to=name_to, symbol=symbol,
                               rates=session.get("rates"), bit=session.get("bit"))
