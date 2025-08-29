from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this for production

# Example EA data
def get_ea_data():
    return {
        "balance": round(random.uniform(1000, 5000), 2),
        "open_trades": random.randint(0, 5),
        "buy_signals": random.randint(0, 3),
        "sell_signals": random.randint(0, 3),
        "equity": round(random.uniform(1000, 5000), 2)
    }

# Login credentials (for demo purposes)
USERNAME = "admin"
PASSWORD = "password"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    data = get_ea_data()
    return render_template("dashboard.html", data=data)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
