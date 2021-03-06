from flask import Flask, render_template, g, request, session, redirect, url_for
from db.db import connect_db, get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


# helper
def get_cur_user():
    user_res = None
    if "user" in session:
        user = session["user"]
        db = get_db()
        user_query = db.execute(
            "select id, name, password, expert, admin from users where name = ?", [user]
        )
        user_res = user_query.fetchone()

    return user_res


@app.route("/")
def index():
    user = get_cur_user()
    db = get_db()
    query = db.execute('select questions.id as question_id, questions.question, askers.name as asker_name, experts.name as expert_name from questions join users as askers on askers.id = questions.ask_by_id join users as experts on experts.id = questions.expert_id where questions.answer_text is not null')
    res = query.fetchall()
    return render_template("home.html", user=user, res = res)


@app.route("/register", methods=["GET", "POST"])
def register():
    user = get_cur_user()
    if request.method == "POST":
        db = get_db()
        password = request.form["inputPassword"]
        username = request.form["inputName"]
        hash = generate_password_hash("password", method="sha256")
        db.execute(
            "insert into users (name,password,expert,admin) values (?,?,?,?)",
            [username, hash, "0", "0"],
        )
        db.commit()
        session["user"] = request.form["inputName"]

        return redirect(url_for("index"))

    return render_template("register.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    user = get_cur_user()
    if request.method == "POST":
        password = request.form["inputPassword"]
        username = request.form["inputName"]
        db = get_db()
        user_query = db.execute(
            "select id, name, password from users where name = ?", [username]
        )
        res = user_query.fetchone()
        if res == None or not check_password_hash(res["password"], password):
            return "User name or password incorrect!"
        else:
            session["user"] = res["name"]
            return redirect(url_for("index"))

    return render_template("login.html", user=user)


@app.route("/question/<qid>")
def question(qid):
    user = get_cur_user()
    db = get_db()
    db.execute('select questions.id as question_id, questions.question, askers.name as asker_name, experts.name as expert_name from questions join users as askers on askers.id = questions.ask_by_id join users as experts on experts.id = questions.expert_id where questions.id = ?',[question_id])

    return render_template("question.html", user=user)


@app.route("/answer/<q_id>", methods=['GET','POST'])
def answer(q_id):
    user = get_cur_user()
    db = get_db()

    if request.method == 'POST':
        answer = request.form['answer']
        db.execute('update questions set answer_text = ? where id = ? ',[answer,q_id])
        db.commit()
        return redirect(url_for('unanswered'))

    query = db.execute('select id, question from questions where id = ?',[q_id])
    question = query.fetchone()
    return render_template("answer.html", user=user, question=question)


@app.route("/ask", methods=["GET", "POST"])
def ask():
    user = get_cur_user()
    db = get_db()

    if request.method == "POST":
        expert = request.form["expert"]
        question = request.form["question"]
        db.execute(
            " insert into questions (question, ask_by_id, expert_id) values (?,?,?)",
            [question, user["id"], expert],
        )
        db.commit()

        return redirect(url_for("index"))

    expert_query = db.execute("select id, name from users where expert = 1")
    expert_res = expert_query.fetchall()
    return render_template("ask.html", user=user, experts=expert_res)


@app.route("/unanswered")
def unanswered():
    user = get_cur_user()
    db = get_db()
    question_query = db.execute(
        "select questions.id, questions.question, users.name from questions join users on users.id = questions.ask_by_id where questions.answer_text is null and questions.expert_id = ? ",[user['id']])
    questions = question_query.fetchall()

    return render_template("unanswered.html", user=user, questions=questions)


@app.route("/users")
def users():
    user = get_cur_user()
    db = get_db()
    users_query = db.execute("select id, name, expert, admin from users")
    users_res = users_query.fetchall()
    return render_template("users.html", user=user, users=users_res)


@app.route("/promote/<user_id>")
def promote(user_id):
    user = get_cur_user()
    db = get_db()
    db.execute("update users set expert = 1 where id = ?", [user_id])
    db.commit()
    return redirect(url_for("users"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
