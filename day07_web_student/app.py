from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from functools import wraps
from pathlib import Path
import pandas as pd

# 统一定义项目根目录，只写一次
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "day07-classroom-demo-key"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("请先登录后再访问数据看板。", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    return redirect(url_for("dashboard") if "username" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == "student" and password == "day07":
            session["username"] = username
            flash("登录成功，欢迎进入电商用户分析系统。", "success")
            return redirect(url_for("dashboard"))
        flash("账号或密码错误。演示账号：student / day07", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("你已安全退出。", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    category = request.args.get("category", "全部")
    from services.data_service import load_dashboard_data
    dashboard_data = load_dashboard_data(BASE_DIR, category)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=category,
        **dashboard_data,
    )


@app.route("/assistant")
@login_required
def assistant():
    return render_template("assistant.html", username=session["username"])


@app.route("/api/ask", methods=["POST"])
@login_required
def ask():
    from services.qa_service import answer_question
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"ok": False, "answer": "请输入一个与项目数据有关的问题。"}), 400
    return jsonify({"ok": True, "answer": answer_question(BASE_DIR, question)})

@app.route("/segments")
@login_required
def segment_detail():
    df = pd.read_csv(BASE_DIR / "data/segment_analysis.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df_sort = df.sort_values(by="流失率", ascending=False)
    analysis = "数据观察：新用户流失率最高，达到53.5%，随着用户在网时长增加流失率持续下降，长期留存用户流失率仅0.9%，新用户是运营留存核心人群。"
    return render_template("segments.html", data=df_sort.to_dict("records"), analysis_text=analysis)

@app.route("/user_stage")
@login_required
def user_stage():
    import pandas as pd
    df = pd.read_csv(BASE_DIR / "data/segment_analysis.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df_sort = df.sort_values(by="流失率", ascending=False)
    analysis = "数据观察：新用户流失率最高，达到53.5%，随着用户在网时长增加流失率持续下降，长期留存用户流失率仅0.9%，新用户是运营留存核心人群。"
    return render_template("segments.html", data=df_sort.to_dict("records"), analysis_text=analysis)

@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False, port=5000)