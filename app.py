from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from datetime import datetime
from helpers import SQL, login_required, encrypt, decrypt, validate_password
import secrets

# make a secret key
secret_key = secrets.token_hex(16)

# configure the app
app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key

static = Blueprint("static", __name__, static_folder="static")
app.register_blueprint(static)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# configure the database
db = SQL("notes.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# home route
@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    # get user id
    user_id = session["user_id"]

    # if the user tries to submit some data
    if request.method == "POST":
        # if the user inputs an eampty note
        title = request.form.get("title")
        if not title:
            flash("Can not submit an empty note!", "error")
            return redirect("/")

        if db.execute(
            "SELECT title FROM notes WHERE title=? AND user_id=?", (title, user_id)
        ):
            flash(f"A note with the Title of {title} already exists.", "info")
            return redirect("/")

        if len(title) > 25:
            flash("Title must be 25 characters or less.", "info")
            return redirect("/")

        note = request.form.get("note")
        now = datetime.now()
        time = now.strftime("%A, %d/%m/%Y, %I:%M %p")

        # insert into the table
        db.execute(
            "INSERT INTO notes(title, content, date_time, user_id) VALUES (?, ?, ?, ?)",
            (title, note, time, user_id),
        )
        return redirect("/")

    # get back the notes
    notes = db.execute(
        "SELECT * FROM notes WHERE user_id=? AND pin_status=0  AND archive_status=0 ORDER BY id DESC",
        (user_id,),
    )

    # get back the pined notes
    pined_notes = db.execute(
        "SELECT * FROM notes WHERE user_id=? AND pin_status=1 AND archive_status=0 ORDER BY id DESC",
        (user_id,),
    )
    return render_template("index.html", notes=notes, pined_notes=pined_notes)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user
    session["user_id"] = None
    session["username"] = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill out all forms to proceed.", "info")
            return redirect(url_for("login"))

        username = username.lower().strip()

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=?", (username,))

        if not rows or not check_password_hash(rows[0]["password"], password):
            flash("You have entered an invalid username or password.", "info")
            return redirect(url_for("login"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = username

        return redirect("/")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        # check if the user provided every information
        if not username or not password or not confirm_password:
            flash("Please fill out all forms to proceed.", "info")
            return redirect(url_for("register"))

        username = username.lower().strip()

        # if user writes a large username
        if len(username) > 25:
            flash("Username must be 25 characters or less.", "info")
            return redirect(url_for("register"))

        # check if username exists
        if db.execute("SELECT username FROM users WHERE username=?", (username,)):
            flash("Username already exsists!", "info")
            return redirect(url_for("register"))

        # check if passwords matches confirmation
        if password != confirm_password:
            flash("Password and Confirm Password do not match.", "error")
            return redirect(url_for("register"))

        # check if password matches password rules
        if not validate_password(password):
            flash(
                "Your password must be a minimum of 8 characters and should contain at least one upper-case and lower-case letter, a number, and a symbol.",
                "error",
            )
            return redirect(url_for("register"))

        # if everything is okay
        hash = generate_password_hash(password)
        db.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)", (username, hash)
        )
        flash("Thanks for signing up. Your account has been created.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]
    username = session["username"]

    if request.method == "POST":
        option = request.form.get("optionBtn")
        if option == "updatePassword":
            current_password = request.form.get("currentPassword")
            new_password = request.form.get("newPassword")
            confirm_password = request.form.get("confirmPassword")

            if not current_password or not new_password or not confirm_password:
                flash("Please fill out all forms to proceed.")
                return redirect(url_for("profile"))

            check_password = check_password_hash(
                (
                    db.execute("SELECT password FROM users WHERE id=?", (user_id,))[0][
                        "password"
                    ]
                ),
                current_password,
            )

            if not check_password:
                flash("Current password is incorrect. Please try again.")
                return redirect(url_for("profile"))

            # check if passwords matches confirmation
            if new_password != confirm_password:
                flash("Password and Confirm Password do not match.", "error")
                return redirect(url_for("profile"))

            # check if password matches password rules
            if not validate_password(new_password):
                flash(
                    "Your new password must be a minimum of 8 characters and should contain at least one upper-case and lower-case letter, a number, and a symbol.",
                    "error",
                )
                return redirect(url_for("profile"))

            # if all goes well
            db.execute(
                "UPDATE users SET password=? WHERE id=?",
                (generate_password_hash(new_password), user_id),
            )
            flash("Your password has been changed successfully.")
            return redirect(url_for("login"))
        else:
            current_password = request.form.get("currentPassword")
            if not current_password:
                flash("Please fill out all forms to proceed.")
                return redirect(url_for("profile"))

            check_password = check_password_hash(
                (
                    db.execute("SELECT password FROM users WHERE id=?", (user_id,))[0][
                        "password"
                    ]
                ),
                current_password,
            )

            if not check_password:
                flash("Current password is incorrect. Please try again.")
                return redirect(url_for("profile"))

            db.execute("DELETE FROM users WHERE id=?", (user_id,))
            db.execute("DELETE FROM notes WHERE user_id=?", (user_id,))
            return redirect(url_for("logout"))

    return render_template("profile.html", username=username)


@app.route("/delete", methods=["POST"])
@login_required
def delete_note():
    user_id = session["user_id"]
    id = request.form.get("id")
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (id, user_id))[0]
    db.execute(
        "INSERT INTO bin(title, content, date_time, pin_status, archive_status, user_id) VALUES(?,?,?,?,?,?)",
        (
            note["title"],
            note["content"],
            note["date_time"],
            note["pin_status"],
            note["archive_status"],
            note["user_id"],
        ),
    )
    db.execute("DELETE FROM notes WHERE id=? AND user_id=?", (id, user_id))
    return redirect("/")


@app.route("/clearNotes")
@login_required
def delete_all_notes():
    # get the user id
    user_id = session["user_id"]

    # get all notes from the notes table
    notes = db.execute("SELECT * FROM notes WHERE user_id=?", (user_id,))

    if notes:
        for note in notes:
            db.execute(
                "INSERT INTO bin(title, content, date_time, pin_status, archive_status, user_id) VALUES(?,?,?,?,?,?)",
                (
                    note["title"],
                    note["content"],
                    note["date_time"],
                    note["pin_status"],
                    note["archive_status"],
                    note["user_id"],
                ),
            )
    else:
        return redirect("/")

    # delete all notes associated with this user
    db.execute("DELETE FROM notes WHERE user_id=?", (user_id,))

    flash("All notes where removed successfuly!", "info")
    return redirect("/")


@app.route("/bin", methods=["POST", "GET"])
@login_required
def bin():
    user_id = session["user_id"]

    if request.method == "POST":
        note_id = request.form.get("id")
        note_title = request.form.get("title")
        operation = request.form.get("operation")

        if operation == "delete":
            db.execute("DELETE FROM bin WHERE user_id=? AND id=?", (user_id, note_id))
            flash(f"{note_title} was deleted indefinitely!", "info")
        else:
            note = db.execute(
                "SELECT * FROM bin WHERE id=? AND user_id=?", (note_id, user_id)
            )[0]
            db.execute("DELETE FROM bin WHERE user_id=? AND id=?", (user_id, note_id))
            db.execute(
                "INSERT INTO notes(title, content, date_time, pin_status, archive_status, user_id) VALUES(?,?,?,?,?,?)",
                (
                    note["title"],
                    note["content"],
                    note["date_time"],
                    note["pin_status"],
                    note["archive_status"],
                    note["user_id"],
                ),
            )
            flash(f"{note_title} was recovered successfully.", "info")
        return redirect(url_for("bin"))

    notes = db.execute(
        "SELECT * FROM bin WHERE user_id=? ORDER BY date_time, id", (user_id,)
    )
    return render_template("bin.html", notes=notes)


@app.route("/delete_recover", methods=["POST"])
@login_required
def delete_recover():
    operation = request.form.get("operation")
    user_id = session["user_id"]

    if operation == "delete":
        db.execute("DELETE FROM bin WHERE user_id=?", (user_id,))
        flash("All notes were deleted indefinitely!", "info")
    else:
        notes = db.execute("SELECT * FROM bin WHERE user_id=?", (user_id,))
        db.execute("DELETE FROM bin WHERE user_id=?", (user_id,))
        for note in notes:
            db.execute(
                "INSERT INTO notes(title, content, date_time, pin_status, archive_status, user_id) VALUES(?,?,?,?,?,?)",
                (
                    note["title"],
                    note["content"],
                    note["date_time"],
                    note["pin_status"],
                    note["archive_status"],
                    note["user_id"],
                ),
            )
        flash("All notes were recovered successfully!", "info")

    return redirect(url_for("bin"))


@app.route("/search", methods=["GET"])
@login_required
def serach():
    user_id = session["user_id"]
    search_term = request.args.get("title")
    if not search_term:
        return redirect("/")

    # search for the looked up note
    notes = db.execute(
        "SELECT * FROM notes WHERE user_id=? AND title LIKE ? ORDER BY id DESC",
        (user_id, "%" + search_term + "%"),
    )

    # if search term was not found
    if not notes:
        flash(f"({search_term}) was not found!", "info")
        return redirect("/")

    flash(f"Search result: {len(notes)}")
    return render_template("search.html", searched_notes=notes)


@app.route("/update", methods=["POST"])
def update():
    user_id = session["user_id"]
    id = request.form.get("id")
    now = datetime.now()
    time = now.strftime("%A, %d/%m/%Y, %I:%M %p")
    title = request.form.get("title")
    content = request.form.get("content")

    if len(title) >= 25:
        flash("Title must be 25 characters or less.", "info")
        return redirect("/")

    db.execute(
        "UPDATE notes set date_time=?, title=?, content=? WHERE id=? AND user_id=?",
        (time, title, content, id, user_id),
    )
    return redirect("/")


@app.route("/archive", methods=["POST"])
def archive():
    user_id = session["user_id"]
    id = request.form.get("id")

    current_archive_status = db.execute(
        "SELECT archive_status FROM notes WHERE id=? AND user_id=?", (id, user_id)
    )[0]["archive_status"]

    if current_archive_status == 1:
        db.execute(
            "UPDATE notes SET archive_status=0 WHERE id=? AND user_id=?", (id, user_id)
        )
        return redirect(url_for("archives"))

    db.execute(
        "UPDATE notes SET archive_status=1 WHERE id=? AND user_id=?", (id, user_id)
    )
    return redirect("/")


@app.route("/archives")
@login_required
def archives():
    user_id = session["user_id"]
    notes = db.execute(
        "SELECT * FROM notes WHERE user_id=? AND archive_status=1",
        (user_id,),
    )
    return render_template("archives.html", notes=notes)


@app.route("/pin", methods=["POST"])
def pin():
    user_id = session["user_id"]
    id = request.form.get("id")

    # get the pin status
    pin_status = db.execute(
        "SELECT pin_status FROM notes WHERE id=? AND user_id=?", (id, user_id)
    )[0]["pin_status"]

    if pin_status == 1:
        db.execute(
            "UPDATE notes SET pin_status=0 WHERE user_id=? AND id=?", (user_id, id)
        )
    else:
        db.execute(
            "UPDATE notes SET pin_status=1 WHERE user_id=? AND id=?", (user_id, id)
        )
    return redirect("/")
