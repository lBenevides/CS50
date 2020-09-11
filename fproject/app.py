import os

import datetime
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
import json

from helpers import apology, login_required

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect a database using SQLite
db = sqlite3.connect("database.db",check_same_thread = False)
cursor = db.cursor()

# Configure user type


# Using a dict to store the Groups
Grupos =  {
    "Visão": ["Palácio","Paraíba", "Codiba", "Combat", "Alagoana"],
    "Base": ["Autobate", "Disbate", "Interbahia","Bonfim"], 
    "Fortaleza": ["Dismal", "Fortaleza", "Piauiense","Paraense"],
    "Avançar": ["Fluminense","Tringulo","Juiz de Fora","Volta Redonda","Cominas","Comal","Nova Iguaçu","Dinil"],
    "Planalto": ["Godal", "Campo Grande","Disbac","Porto Velho", "Norte","Tocantins","Brasiliense","Anápolis"],
    "Crescer": ["Paulista","Bandeirantes","União","Dirpal","Bauru","Serve Vale","Belo Jardim","Presidente Prudente"],
    "Sul": ["Batermol","Avic","Rodmaster","Santa Maria","Catarinense", "Chapecoense"],
}



@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return redirect("farol")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        
        #request input data from browser
        password = request.form['password']

        # Ensure username exists and password is correct
        
        cursor.execute("SELECT * from user WHERE username=?", [request.form["username"]])
        result = cursor.fetchone()

        if result is None or not check_password_hash(result[2], password):
            return jsonify({'redirect' : False})
        else:
            # Remember which user has logged in
            session["user_id"] = result[0]
            if result[3] == "Admin":
                session["admin"] = True
            
            
            # Redirect user to home page
            return jsonify({'redirect' : True})
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

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Query database for username
        cursor.execute("SELECT * FROM user WHERE username=?", [request.form["username"]])
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO user (username, hash, user_type) VALUES (?,?,?)", [request.form["username"], generate_password_hash(request.form["password"]), "GPM"])
            db.commit()

            return jsonify({'redirect' : True})
        else:
            return jsonify({'redirect' : False})

        # Ensure username exists and password is correct

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




####################################################################################
################# as funções abaixo são referentes a pagina farol ##################

# essa função serve para restrição de acesso de usuário
@app.route("/farol", methods=["GET", "POST"])
@login_required
def farol():

    if request.method == "POST":
        return jsonify({"g_unit": Grupos[request.form["g_unit"]]})
    else:
        cursor.execute("SELECT * FROM user WHERE id= ?", [ session["user_id"] ] )
        type_user = cursor.fetchone()

        if type_user[3] == "Admin":
            cursor.execute("SELECT * FROM farol")
            result = cursor.fetchall()
        else:
            result = []
            u_grupos = type_user[4].split(",")
            size = len(u_grupos)

            for i in range(size):
                cursor.execute("SELECT * from farol WHERE grupo=?", [ u_grupos[i] ])
                result.extend(cursor.fetchall())

        return render_template("farol.html", groups=Grupos, result = result)

# função serve para passar informações dos setores nas Modal Box
@app.route("/novo", methods=["POST"])
@login_required
def novo():
    
    cursor.execute("SELECT DISTINCT field FROM positions ORDER BY field")
    result = cursor.fetchall()

    return jsonify({"setor": result})


# função para passar as cargos apos a seleção do setor na modal box
@app.route("/cargo", methods=["POST"])
@login_required
def cargo():
    setor = request.form["setor_value"]
    cursor.execute("SELECT position FROM positions WHERE field = ?", [setor])
    result = cursor.fetchall()

    return jsonify({"cargos": result})

# função acompanha o botão novo, para salvar as informações do novo colaborador
@app.route("/salvar", methods=["POST"])
@login_required
def salvar():

    f_grupo = request.form["grupo"]
    f_unidade = request.form["unidade"]
    f_nome = request.form["nome"]
    f_cargo = request.form["cargo"]
    f_risco_c = request.form["risco_c"]
    f_risco_e = request.form["risco_e"]

    cursor.execute("INSERT INTO farol (grupo, unidade, nome, cargo, risco_c, risco_e) VALUES (?,?,?,?,?,?)",[ f_grupo, f_unidade, f_nome, f_cargo, f_risco_c, f_risco_e ])
    lastid = cursor.lastrowid
    db.commit()
    print(lastid)

    return jsonify({'id': lastid})

##### abaixo são as funções do FAROL referente a edição de linha #####

# função ao clicar o botão de editar passar as informações para a modal box
@app.route("/f_editar", methods=["POST"])
@login_required
def f_editar():
    cursor.execute("SELECT * FROM farol WHERE id=?", [request.form["colab_id"]])
    result = cursor.fetchone()

    cursor.execute("SELECT DISTINCT field FROM positions ORDER BY field")
    setor = cursor.fetchall()

    cursor.execute("SELECT field FROM positions where Position=?", [result[4]])
    setor_c = cursor.fetchone()

    cursor.execute("SELECT position from positions where field=?", [setor_c[0]])
    cargos = cursor.fetchall()
    

    return jsonify({'result': result, 'setor': setor, 'setor_c' : setor_c, 'cargos' : cargos})


#função para ATUALIZAR as informações que foram digitadas na modal box de edição
@app.route("/atualizar", methods=["POST"])
@login_required
def atualizar():
    nome = request.form["nome"]
    cargo = request.form["cargo"]
    risco_c = request.form["risco_c"]
    risco_e = request.form["risco_e"]
    colab_id = request.form["colab_id"]

    cursor.execute("UPDATE farol SET nome=?, cargo=?, risco_c=?, risco_e=? WHERE id=?",[nome, cargo, risco_c, risco_e, colab_id])
    db.commit()

    return jsonify({'sucess':'sucess'})


# função ao clicar o botão deletar no farol, para del uma linha
@app.route("/deletar", methods=["POST"])
@login_required
def deletar():

    cursor.execute("DELETE FROM farol WHERE id=?",request.form["colab_id"])
    db.commit()

    return jsonify({'success':'sucess'})



##############################################################
############# codigo da pag Admin irão abaixo ################

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":

        user_id = request.form["user_id"]
        cursor.execute("SELECT * FROM user WHERE id = ?", [user_id])
        result = cursor.fetchone()
        g_list = ["Visão","Base", "Fortaleza", "Avançar", "Planalto", "Crescer", "Sul"]

        return jsonify({'user': result, 'g_list' : g_list})

    else:
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()

        return render_template("admin.html", users = result)

@app.route("/update", methods=["POST"])
@login_required
def update():
    
    user_id = request.form["user_id"]
    s_groups = request.form["s_groups"]
    s_usertype = request.form["s_usertype"]
    if s_usertype == "Admin":
        s_groups = ""
    s_username = request.form["s_username"]

    cursor.execute("UPDATE user SET username = ?, user_type = ?, groups = ?  WHERE id = ?",[s_username,s_usertype, s_groups, user_id])
    db.commit()
    cursor.execute("SELECT * FROM user WHERE id = ?", [user_id])
    result = cursor.fetchone()

    return jsonify({'result' : result})



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)