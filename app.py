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

#import mock_data
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
        releases=get_releases(),
        collections=get_collections(),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        match = next(
            (u for u in get_users()
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
        elif any(u["username"] == username for u in get_users()):
            flash("Username already taken.", "error")
        elif any(u["email"] == email for u in get_users()):
            flash("Email already taken.", "error")
        else:
            uid = db.query("""SELECT MAX(u_id) FROM users""")[0][0] + 1
            successful = db.insert("users", f"'{username}', '{email}', '{password}', '{uid}'")
            #FIXME: make sure this works
            if(successful):
                session["username"] = username
                flash(f"Account created. Welcome, {username}!", "success")
                return redirect(url_for("home"))
            else:
                flash("Error in account creation.", "error")
                return redirect(url_for("register"))
    return render_template("register.html")


@app.route("/release/<int:release_id>")
def release_detail(release_id):
    release = get_releases_by_id().get(release_id)
    if release is None:
        flash("Release not found.", "error")
        return redirect(url_for("home"))
    return render_template("release.html", release=release)


@app.route("/collection/<int:c_id>")
def collection_detail(c_id):
    collection = get_collections_by_id().get(c_id)
    if collection is None:
        flash("Collection not found.", "error")
        return redirect(url_for("home"))
    releases = [
        #mock_data.RELEASES_BY_ID[rid]
        get_releases_by_id()[rid]
        for rid in collection["release_ids"]
        if rid in get_releases_by_id()
    ]
    stats = {
        "total_tracks": sum(len(r["tracks"]) for r in releases),
        "formats": sorted({r["format"] for r in releases}),
        "genres": sorted({r["genre"] for r in releases}),
    }
    return render_template("collection.html", collection=collection,
                           releases=releases, stats=stats)
# @app.route("/browse")
# def browse():
#     return render_template("browse.html", releases=mock_data.RELEASES)

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/browse")
def browse():
    return render_template("browse.html", releases=get_releases())


# @app.route("/help")
# def help():
#     return render_template("help.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/release/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        contributors = request.form.get("contributors", "").strip()
        r_type = request.form.get("r_type", "")
        r_format = request.form.get("format", "")
        r_date = request.form.get("r_date", "")
        r_label = request.form.get("r_label", "").strip()
        cover = request.form.get("cover", "").strip()
        details = request.form.get("details", "").strip()
        
        if not title or not contributors or not r_type or not r_format or not r_date or not r_label:
            flash("All required fields must be filled out", "error")
            return render_template("add.html")

        good_insert = db.insert(
            "releases",
            f"'{title}', '{contributors}', '{r_type}', '{r_format}', '{r_date}', '{r_label}', '{cover}', '{details}' "
        )
        
        if good_insert:
            flash(f"Release '{title}' added to library!", "success")
            return redirect(url_for("home"))
        else:
            flash("Error adding release", "error")
            return render_template("add.html")
    return render_template("add.html")

@app.route("/release/<int:release_id>/delete", methods=["GET", "POST"])
def delete(release_id):
    release = get_releases_by_id().get(release_id)
    if release is None:
        flash("Release was not found", "error")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        title = release["title"]
        contributors = release["contributors"]
        try:
            db._cur.execute(f"DELETE FROM releases WHERE title = '{title}' AND contributors = '{contributors}'")
            db._conn.commit()
            flash(f"Release '{title}' was deleted.", "success")
            return redirect(url_for("home"))
        except Exception as e:
            print(f"DELETE ERROR: {e}")
            flash(f"Error deleting release", "error")
            return redirect(url_for("home"))
    return render_template("delete.html", release=release)

@app.route("/release/<int:release_id>/edit", methods=["GET", "POST"])
def edit(release_id):
    release = get_releases_by_id().get(release_id)
    if release is None:
        flash("Release was not found", "error")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        org_title = release["title"]
        org_contributors = release["contributors"]
        
        title = request.form.get("title", "").strip()
        contributors = request.form.get("contributors", "").strip()
        r_type = request.form.get("r_type", "")
        r_format = request.form.get("format", "")
        r_date = request.form.get("r_date", "")
        r_label = request.form.get("r_label", "").strip()
        cover = request.form.get("cover", "").strip()
        details = request.form.get("details", "").strip()
        
        if not title or not contributors or not r_type or not r_format or not r_date or not r_label:
            flash("All required fields must be filled out", "error")
            return render_template("edit.html", release=release)
        
        try:
            db._cur.execute(
                f"UPDATE releases SET "
                f"title = '{title}', contributors = '{contributors}', "
                f"r_type = '{r_type}', format = '{r_format}', "
                f"r_date = '{r_date}', r_label = '{r_label}', "
                f"cover = '{cover}', details = '{details}' "
                f"WHERE title = '{org_title}' AND contributors = '{org_contributors}'" 
            )
            db._conn.commit()
            flash(f"Release '{title}' was updated.", "success")
            return redirect(url_for("home"))
        except Exception as e:
            print(f"UPDATE ERROR: {e}")
            flash("Error updating release", "error")
            return redirect(url_for("home"))
    return render_template("edit.html", release = release)

def get_collections(cid=-1):
    """takes an optional input of a collection id, and returns either that collection id or all collections."""
    if cid == -1:
        return _get_all_collections()
    else:
        return _get_collection_cid(cid)


def get_collections_by_id():
    """Returns a dictionary with key pair relationship (collection_id, collection)"""
    return {c["c_id"]: c for c in get_collections()}


def get_collection_rids(cid=0):
    """Returns a list of dictionaries of all collection data"""
    titles = []
    rids = []
    for t in db.query(
        f"""
        SELECT distinct title
        FROM has JOIN creates ON has.g_id = creates.g_id
        WHERE c_id = {cid}
        """
    ): 
        titles.append(t[0])

    rids = []
    for r in get_releases():
        if r["title"] in titles:
            rids.append(r["id"])
    return rids


def _get_all_collections():
    """Returns list containing of dictionaries for all collections."""
    collections = []
    c_tbl = db.select(tbls="collection")

    for c in c_tbl:
        cdict = {
            "c_id":         c[0],
            "name":         f"Collection # {c[0]}",
            "release_ids":  get_collection_rids(c[0])
        }
        collections.append(cdict)
    return collections


def _get_collection_cid(cid):
    """Returns a list containing the desired collection"""
    collections = []
    c_tbl = db.select(tbls="collection")

    for c in c_tbl:
        if cid == c[0]:
            cdict = {
                "c_id":         c[0],
                "name":         f"Collection # {c[0]}",
                "release_ids":  get_collection_rids(c[0])
            }
            collections.append(cdict)
    return collections


def get_releases():
    """Returns a dictionary with all releases in the DB"""
    r_tbl = db.select(tbls="releases") # list of tuples, tuple elems are varying types
    releases = [] # a list of dictionaries

    rid = 1
    for r in r_tbl:
        tracks, genres = get_tracks(r[0])
        rdict = {
            "id":           rid,
            "title":        r[0],
            "contributors": r[1],
            "r_type":       r[2],
            "format":       r[3],
            "r_date":       str( r[4] ),
            "r_label":      r[5],
            "cover":        r[6],
            "genre":        genres,
            "details":      r[7],
            "tracks":       tracks,
        }
        releases.append(rdict)
        rid += 1
    return releases


def get_releases_by_id():
    """Returns a dictionary with a key pair of (release_id, release)""" 
    return {r["id"]: r for r in get_releases()}


def get_tracks(album):
    """ Searches the database for tracks off the given album. 
        Returns a dictionary containing those tracks, and a list of genres."""

    tracks = [] # list of dictionaries
    t_tbl = db.select(tbls="track", pred=f"r_title = '{album}'")
    genres_list = []

    for t in t_tbl:
        if t[5] not in genres_list:
            genres_list.append(t[5])

        tdict = {
            "t_num":    int( t[3] ),
            "title":    t[0],
            "duration": int( t[4] ),
            "genre":    t[5],
            "features": t[6],
        }
        tracks.append(tdict)
    
    # format genres list
    genres = ""
    genres_list.sort()
    for g in genres_list:
        if(genres_list[-1] == g):
            genres += g
        else:
            genres += f"{g}, "
    
    return tracks, genres


def get_users():
    """Returns list of dictionaries containing all user information"""
    u_tbl = db.select(tbls="users")
    user_list = []

    for u in u_tbl:
        udict = {
            "username": u[1],
            "password":      u[0],
            "email":    u[2],
        }
        user_list.append(udict)

    return user_list


def get_user_collections(uid="-1", username="none"):
    """Returns all collections belonging to user with inputted uid or username"""

    col_list = []
    if uid == -1 and username == "none":
        return
    elif username == "none": # search by u_id
        collection_ids = db.select(rows="c_id", tbls="collection", pred=f"u_id = {uid}")

        for id in collection_ids:
            col = get_collections(id[0])[0]     # id is a tuple w/ 1 elem; get_collections returns a list of dictionaries.
            col_list.append(col)
    else: # search by username
        collection_ids = db.query(
            f"""
            SELECT c_id
            FROM collection JOIN users ON collection.u_id = users.u_id
            WHERE username = '{username}'
            """)

        for id in collection_ids:
            col = get_collections(id[0])[0]
            col_list.append(col)
    
    return col_list


if __name__ == "__main__":
    # macOS reserves port 5000 for AirPlay Receiver, so default to 5001.
    db.init_db()

    port = int(os.environ.get("FLASK_PORT", 5001))
    app.run(debug=True, port=port)
