import time
from flask import (
    Blueprint, 
    render_template,
    current_app,
    flash,
    redirect,
    session,
    url_for,
    request
)
import functools
import uuid
import datetime
from dataclasses import asdict

from todoApp.forms import LoginForm, RegisterForm, TodoForm
from todoApp.models import User, Todo
from passlib.hash import pbkdf2_sha256


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))
        return route(*args, **kwargs)
    return route_wrapper


@pages.route("/")
@login_required
def index():
    user_data = current_app.db.user.find_one({"email": session["email"]})
    user = User(**user_data)

    todo_data = current_app.db.todo.find({"_id": {"$in": user.todos}})
    todos = [Todo(**todo) for todo in todo_data]

    return render_template(
        "index.html",
        title="Todos App",
        todos_data=todos,
    )


@pages.route("/register", methods=["POST", "GET"])
def register():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )

        current_app.db.user.insert_one(asdict(user))

        flash("User registered successfully", "success")

        return redirect(url_for(".login"))

    return render_template(
        "register.html", title="Todos App - Register", form=form
    )


@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))
        user = User(**user_data)

        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect(url_for(".index"))

        flash("Login credentials not correct", category="danger")

    return render_template("login.html", title="Todos App - Login", form=form)


@pages.route("/logout")
def logout():
    del session["email"]
    del session["user_id"]

    return redirect(url_for(".login"))


@pages.route("/add", methods=["GET", "POST"])
@login_required
def add_todo():
    form = TodoForm()

    if form.validate_on_submit():
        # print("first",form.due_date.data)
        todo = Todo(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data
            # datetime.datetime.fromisoformat(form.due_date.data)
        )
        current_app.db.todo.insert_one(asdict(todo))

        current_app.db.user.update_one(
            {"_id": session["user_id"]}, {"$push": {"todos": todo._id}}
        )

        return redirect(url_for(".todo", _id=todo._id))

    return render_template(
        "new_todo.html", title="Todos App - Add Todo", form=form
    )


@pages.get("/todo/<string:_id>")
def todo(_id: str):
    todo = Todo(**current_app.db.todo.find_one({"_id": _id}))
    return render_template("todo_details.html", todo=todo)


@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required
def edit_todo(_id: str):
    todo = Todo(**current_app.db.todo.find_one({"_id": _id}))
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.due_date = form.due_date.data

        current_app.db.todo.update_one({"_id": todo._id}, {"$set": asdict(todo)})
        return redirect(url_for(".todo", _id=todo._id))
    return render_template("todo_form.html", todo=todo, form=form)

@pages.route("/delete/<string:_id>")
@login_required
def delete_todo(_id:str):
    current_app.db.todo.delete_one({'_id':_id})
    return redirect(url_for(".index"))

@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))

if __name__ == '__main__':
    pages.run(debug=True)
