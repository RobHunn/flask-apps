from flask import Flask, render_template, request, redirect, g
from flask_debugtoolbar import DebugToolbarExtension
from database.database import connect_db, get_db

# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from helpers.helpers import helper_date

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

debug = DebugToolbarExtension(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    if request.method == "POST":
        date = request.form["date"]
        parse_date = datetime.strptime(date, "%Y-%m-%d")
        database_date = datetime.strftime(parse_date, "%Y%m%d")
        db.execute("insert into log_date (entry_date) values (?)", [database_date])
        db.commit()

    cur = db.execute(
        "select log_date.entry_date, sum(food.protein) as protein, sum(food.carbohydrates) as carbohydrates, sum(food.fat) as fat, sum(food.calories) as calories from log_date left join food_date on food_date.log_date_id = log_date.id left join food on food.id = food_date.food_id group by log_date.id order by log_date.entry_date desc"
    )
    results = cur.fetchall()

    date_results = []

    for i in results:
        single_date = {}
        single_date["entry_date"] = i["entry_date"]
        single_date["protein"] = i["protein"]
        single_date["carbohydrates"] = i["carbohydrates"]
        single_date["fat"] = i["fat"]
        single_date["calories"] = i["calories"]

        d = datetime.strptime(str(i["entry_date"]), "%Y%m%d")
        single_date["html_date"] = datetime.strftime(d, "%B %d, %Y")

        date_results.append(single_date)

    return render_template("home.html", results=date_results)


@app.route("/view/<date>", methods=["GET", "POST"])
def view(date):
    db = get_db()
    cur = db.execute("select id, entry_date from log_date where entry_date = ?", [date])
    date_result = cur.fetchone()

    if request.method == "POST":
        selected = request.form["selected_food"]
        db.execute(
            "insert into food_date (food_id,log_date_id) values (?,?)",
            [selected, date_result["id"]],
        )
        db.commit()

    selected_date = datetime.strftime(helper_date(date_result), "%B %d %Y")
    food_cur = db.execute("select id, name from food")
    res_food = food_cur.fetchall()
    log_cur = db.execute(
        "select food.name, food.protein, food.carbohydrates, food.fat, food.calories from log_date join food_date on food_date.log_date_id = log_date.id join food on food.id = food_date.food_id where log_date.entry_date = ?",
        [date],
    )
    log_res = log_cur.fetchall()
    day_total = {"protein": 0, "carbohydrates": 0, "fat": 0, "calories": 0}
    for food in log_res:
        day_total["protein"] += food["protein"]
        day_total["carbohydrates"] += food["carbohydrates"]
        day_total["fat"] += food["fat"]
        day_total["calories"] += food["calories"]

    return render_template(
        "day.html",
        entry_date=date_result["entry_date"],
        selected_date=selected_date,
        res_food=res_food,
        log_res=log_res,
        day_total=day_total,
    )


@app.route("/food", methods=["GET", "POST"])
def food():
    db = get_db()
    if request.method == "POST":
        carbs = int(request.form["carbohydrates"])
        fat = int(request.form["fat"])
        protein = int(request.form["protein"])
        name = request.form["food-name"]
        calories = protein * 4 + carbs * 4 + fat * 9
        db.execute(
            "insert into food (name,protein,carbohydrates,fat,calories) values (?,?,?,?,?)",
            [name, protein, carbs, fat, calories],
        )
        db.commit()
        return redirect("/food")
    else:
        cur = db.execute("select name,protein,carbohydrates,fat,calories from food")
        res = cur.fetchall()
        return render_template("add_food.html", res=res)
