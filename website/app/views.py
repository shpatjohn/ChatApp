from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint 
from .database import DataBase

view = Blueprint("views", __name__)


# GLOBAL CONSTANTS
NAME_KEY = 'name'
ADMIN = 'admin'
MSG_LIMIT = 20

# VIEWS


@view.route("/login", methods=["POST", "GET"])
def login():
    """
    displays main login page and handles saving name in session
    :exception POST
    :return: None
    """
    if request.method == "POST":  # if user input a name
        global name
        name = request.form["inputName"]
        if len(name) >= 2 and name != 'admin':
            session[NAME_KEY] = name
            flash(f'Velkommen! {name}.')
            return redirect(url_for("views.home"))
        elif name == 'admin':
            session[NAME_KEY] = name
            flash(f'Du inde som {name}.!')
            return redirect(url_for("views.home"))
        else:
            flash("1Name must be longer than 1 character.")



    return render_template("login.html", **{"session": session})


@view.route("/logout")
def logout():
    """
    logs the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash(f'DDu er nu logget ud.')
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})


@view.route("/math")
def math():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("math.html", **{"session": session})
@view.route("/divide")
def divide():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("divide.html", **{"session": session})
@view.route("/multiply")
def multiply():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("multiply.html", **{"session": session})
@view.route("/subtract")
def subtract():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("subtract.html", **{"session": session})

@view.route("/history")
def history():
    if NAME_KEY not in session:
        flash("LLogin for at se dine beskeder")
        return redirect(url_for("views.login"))

    json_messages = get_history(session[NAME_KEY])
    print(json_messages)
    return render_template("history.html", **{"history": json_messages})


@view.route("/delete_messages")
def delete_messages():
    """
    :Delete messages
    """
    if NAME_KEY not in session:
        flash("KKun til læren!")
        return redirect(url_for("views.login"))
    if NAME_KEY in session and name == 'admin':
        db = DataBase()
        msgs = db.delete_messages()
        jsonify(msgs) 
    return render_template("index.html", **{"session": session})

@view.route("/get_name")
def get_name():
    """
    :return: a json object storing name of logged in user
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    """
    :return: all messages stored in database
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)

    return jsonify(messages)

@view.route("/get_history")
def get_history(name):
    """
    :param name: str
    :return: all messages by name of user
    """
    db = DataBase()
    msgs = db.get_messages_by_name(name)
    messages = remove_seconds_from_messages(msgs)

    return messages


# UTILITIES
def remove_seconds_from_messages(msgs):
    """
    removes the seconds from all messages
    :param msgs: list
    :return: list
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return messages


def remove_seconds(msg):
    """
    :return: string with seconds trimmed off
    """
    return msg.split(".")[0][:-3]