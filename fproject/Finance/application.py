import os

import cs50
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = cs50.SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    t_users = db.execute("SELECT * FROM users WHERE id= :user_id",user_id=session["user_id"])
    t_shares = db.execute("SELECT * FROM shares WHERE user_id = :user_id", user_id=session["user_id"])

    cash_amount = t_users[0]["cash"]
    current_price = {}
    for row in t_shares:
        cash_amount += (row["price"] * row["quantity"])
        current_price[row["symbol"]] = lookup(row["symbol"])["price"]

    return render_template("index.html", users=t_users, shares=t_shares, cash_amount=cash_amount, current_price=current_price)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        row = db.execute("SELECT * FROM users WHERE id = :user_id", user_id =session["user_id"])
        quote = lookup(request.form.get("symbol").upper())
        share=request.form.get("shares")

        if quote is None:
            return render_template("buy.html", invalid=True)

        else:
            if row[0]["cash"] >= (quote["price"] * float(share)):
                cash_result = row[0]["cash"] - (quote["price"] * float(share))
                db.execute("UPDATE users SET cash = :value WHERE id = :user_id", value = cash_result, user_id = session["user_id"])

                db.execute("INSERT INTO transactions (user_id, symbol, name, price, quantity, date) VALUES (:user_id, :symbol, :name, :price, :quantity, :date)",
                user_id=session["user_id"], symbol=quote["symbol"], name=quote["name"], price=quote["price"], quantity=int(share), date=datetime.datetime.now())

                share_rows = db.execute("SELECT * FROM shares WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=quote["symbol"])

                if len(share_rows) == 0:
                    db.execute("INSERT INTO shares (user_id, symbol, name, price, quantity, date) VALUES (:user_id, :symbol, :name, :price, :quantity, :date)",
                    user_id=session["user_id"], symbol=quote["symbol"], name=quote["name"], price=quote["price"], quantity=int(share), date=datetime.datetime.now())
                else:
                    avgprice = (share_rows[0]["price"] * share_rows[0]["quantity"] + (int(share) * quote["price"]) )/(int(share) +share_rows[0]["quantity"])
                    db.execute("UPDATE shares SET price = :avgprice, quantity = :quantity WHERE user_id = :user_id AND symbol = :symbol",avgprice=avgprice, quantity=(share_rows[0]["quantity"] + int(share)),user_id=session["user_id"], symbol=quote["symbol"])
                return render_template("buy.html", bought=True)
            else:
                return render_template("buy.html", fail=True)
    else:
        return render_template("buy.html")

    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    t_transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", transactions=t_transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if lookup(request.form.get("symbol").upper()) is None:
            return render_template("quote.html", invalid = True)
        else:
            return render_template("quote.html", quotes = True, info = lookup(request.form.get("symbol")))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 0:
            add = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        else:
            return render_template("register.html", invalid_username=True)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    t_shares = db.execute("SELECT * FROM shares WHERE user_id = :user_id", user_id=session["user_id"])

    if request.method == "POST":
        t_shares2 = db.execute("SELECT * FROM shares WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=request.form.get("symbol"))

        if t_shares2[0]["quantity"] < int(request.form.get("shares")):
            return render_template("sell.html", shares=t_shares, invalid=True)

        elif t_shares2[0]["quantity"] == int(request.form.get("shares")):
            db.execute("DELETE FROM shares WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=request.form.get("symbol"))

            cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
            cash= (cash[0]["cash"] + (int(request.form.get("shares"))* lookup(request.form.get("symbol"))["price"]))
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash = cash, user_id = session["user_id"])

            quote = lookup(request.form.get("symbol").upper())
            share = request.form.get("shares")
            db.execute("INSERT INTO transactions (user_id, symbol, name, price, quantity, date) VALUES (:user_id, :symbol, :name, :price, :quantity, :date)",
            user_id=session["user_id"], symbol=quote["symbol"], name=quote["name"], price=quote["price"], quantity= (-1 * int(share)), date=datetime.datetime.now())

            t_shares = db.execute("SELECT * FROM shares WHERE user_id = :user_id", user_id=session["user_id"])
            return render_template("sell.html", shares=t_shares)

        else:
            db.execute("UPDATE shares SET quantity = :quantity WHERE user_id = :user_id AND symbol= :symbol",
            quantity = (t_shares2[0]["quantity"] -int(request.form.get("shares"))) , user_id = session["user_id"], symbol=request.form.get("symbol"))

            cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
            cash= (cash[0]["cash"] + (int(request.form.get("shares"))* lookup(request.form.get("symbol"))["price"]))
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash = cash, user_id = session["user_id"])

            quote = lookup(request.form.get("symbol").upper())
            share = request.form.get("shares")
            db.execute("INSERT INTO transactions (user_id, symbol, name, price, quantity, date) VALUES (:user_id, :symbol, :name, :price, :quantity, :date)",
            user_id=session["user_id"], symbol=quote["symbol"], name=quote["name"], price=quote["price"], quantity= (-1 * int(share)), date=datetime.datetime.now())

            t_shares = db.execute("SELECT * FROM shares WHERE user_id = :user_id", user_id=session["user_id"])
            return render_template("sell.html", shares=t_shares)


    else:
        return render_template("sell.html", shares=t_shares)





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
