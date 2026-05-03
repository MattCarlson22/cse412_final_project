"""Flask frontend for the CSE 412 music library project (Phase 3).

Frontend-only scaffolding. Mock data lives in `mock_data.py`. Auth is a
session cookie backed by a hardcoded user list — wire to PostgreSQL later.
"""

import os, psycopg2

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import mock_data
import postgres.db_connection as db # database initialization script

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-do-not-use-in-prod")


@app.context_processor
def inject_user():
    return {"current_user": session.get("username")}


@app.route("/")
def home():
    return render_template(
        "home.html",
        releases=mock_data.RELEASES,
        collections=mock_data.COLLECTIONS,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        match = next(
            (u for u in mock_data.USERS
             if u["username"] == username and u["password"] == password),
            None,
        )
        if match:
            session["username"] = match["username"]
            flash(f"Welcome back, {match['username']}!", "success")
            return redirect(url_for("home"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif any(u["username"] == username for u in mock_data.USERS):
            flash("Username already taken.", "error")
        else:
            mock_data.USERS.append(
                {"username": username, "email": email, "password": password}
            )
            session["username"] = username
            flash(f"Account created. Welcome, {username}!", "success")
            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/release/<int:release_id>")
def release_detail(release_id):
    release = mock_data.RELEASES_BY_ID.get(release_id)
    if release is None:
        flash("Release not found.", "error")
        return redirect(url_for("home"))
    return render_template("release.html", release=release)


@app.route("/collection/<int:c_id>")
def collection_detail(c_id):
    collection = mock_data.COLLECTIONS_BY_ID.get(c_id)
    if collection is None:
        flash("Collection not found.", "error")
        return redirect(url_for("home"))
    releases = [
        mock_data.RELEASES_BY_ID[rid]
        for rid in collection["release_ids"]
        if rid in mock_data.RELEASES_BY_ID
    ]
    stats = {
        "total_tracks": sum(len(r["tracks"]) for r in releases),
        "formats": sorted({r["format"] for r in releases}),
        "genres": sorted({r["genre"] for r in releases}),
    }
    return render_template("collection.html", collection=collection,
                           releases=releases, stats=stats)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    # macOS reserves port 5000 for AirPlay Receiver, so default to 5001.
    db.init_db()
    port = int(os.environ.get("FLASK_PORT", 5001))
    app.run(debug=True, port=port)
