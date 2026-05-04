import psycopg2, os
from dotenv import load_dotenv

_tables = ["users", "collection", "musicgroup", "musician", "releases", "track", "creates", "has"]

def get_db_connection():
    load_dotenv()

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn


_conn = get_db_connection()
_cur = _conn.cursor()


###################################################################################


def get_col_names(tbl) -> list:
    """returns a list of strings containing the column names of the inputed table.

    Reads from postgres/init/db-files/tbl.csv
    """
    cols=[]

    if tbl.lower() not in _tables:
        return "invalid table"

    tblpath = os.getcwd() + "/postgres/init/db-files/" + tbl + ".csv"
    with open(tblpath, "r", encoding="UTF-8") as f:
        cols = f.readline().lower().split(',')
        cols[-1] = cols[-1].removesuffix("\n")

    return cols


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
    """Returns list of release IDs belonging to the given collection."""
    titles = {t[0] for t in query(
        f"SELECT DISTINCT title FROM has JOIN creates ON has.g_id = creates.g_id WHERE c_id = {cid}"
    )}
    return [r["id"] for r in get_releases() if r["title"] in titles]


def _get_all_collections():
    """Returns list containing of dictionaries for all collections."""
    collections = []
    for c in select(tbls="collection"):
        collections.append({
            "c_id":        c[0],
            "name":        f"Collection #{c[0]}",
            "release_ids": get_collection_rids(c[0]),
        })
    return collections


def _get_collection_cid(cid):
    """Returns a list containing the desired collection."""
    collections = []
    for c in select(tbls="collection"):
        if cid == c[0]:
            collections.append({
                "c_id":        c[0],
                "name":        f"Collection #{c[0]}",
                "release_ids": get_collection_rids(c[0]),
            })
    return collections


def add_release_to_collection(c_id, r_title, r_contributors):
    """Adds a release to a collection via the Has table.

    Looks up the release's g_id from Creates, then inserts a Has row using
    the first available musician ID that doesn't already exist for this
    (g_id, c_id) pair.  Returns True on success, False otherwise.
    """
    r_title_safe = r_title.replace("'", "''")
    r_contributors_safe = r_contributors.replace("'", "''")

    result = query(
        f"SELECT g_id FROM creates WHERE title = '{r_title_safe}' AND contributors = '{r_contributors_safe}'"
    )
    if not result:
        return False  # release has no group entry — cannot add via this schema

    g_id = result[0][0]

    # Already in collection?
    if query(f"SELECT 1 FROM has WHERE g_id = {g_id} AND c_id = {c_id}"):
        return False

    # Find a musician ID not yet used for this (g_id, c_id) slot
    for row in query("SELECT m_id FROM musician ORDER BY m_id"):
        m_id = row[0]
        if not query(f"SELECT 1 FROM has WHERE g_id = {g_id} AND c_id = {c_id} AND m_id = {m_id}"):
            try:
                _cur.execute(f"INSERT INTO has (g_id, c_id, m_id) VALUES ({g_id}, {c_id}, {m_id})")
                _conn.commit()
                return True
            except:
                _conn.rollback()
                return False
    return False


def remove_release_from_collection(c_id, r_title, r_contributors):
    """Removes a release from a collection by deleting its Has rows.

    Returns True on success, False otherwise.
    """
    r_title_safe = r_title.replace("'", "''")
    r_contributors_safe = r_contributors.replace("'", "''")

    result = query(
        f"SELECT g_id FROM creates WHERE title = '{r_title_safe}' AND contributors = '{r_contributors_safe}'"
    )
    if not result:
        return False

    g_id = result[0][0]
    try:
        _cur.execute(f"DELETE FROM has WHERE g_id = {g_id} AND c_id = {c_id}")
        _conn.commit()
        return True
    except:
        _conn.rollback()
        return False


def get_releases():
    """Returns a dictionary with all releases in the DB"""
    r_tbl = select(tbls="releases") # list of tuples, tuple elems are varying types
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
    t_tbl = select(tbls="track", pred=f"r_title = '{album}'")
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
    u_tbl = select(tbls="users")
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
        collection_ids = select(rows="c_id", tbls="collection", pred=f"u_id = {uid}")

        for id in collection_ids:
            col = get_collections(id[0])[0]     # id is a tuple w/ 1 elem; get_collections returns a list of dictionaries.
            col_list.append(col)
    else: # search by username
        collection_ids = query(
            f"""
            SELECT c_id
            FROM collection JOIN users ON collection.u_id = users.u_id
            WHERE username = '{username}'
            """)

        for id in collection_ids:
            col = get_collections(id[0])[0]
            col_list.append(col)

    return col_list


def init_db():
    """Should be called on app startup to initialize & connect the database."""

    _drop_tables()

    _cur.execute(open("postgres/init/init.sql", "r").read())

    cwd = os.getcwd() + "/postgres/init/db-files/"
    for tbl in _tables:
        tblpath = cwd + tbl + ".csv"
        with open(tblpath, "r", encoding='UTF-8') as f:
            cols = f.readline().lower().split(",")
            cols[-1] = cols[-1].removesuffix("\n")

            _cur.copy_from(f, tbl, sep=",", columns=cols)
            try:
                _conn.commit()
            except:
                _conn.rollback()


def insert(tbl="releases", vals = ""):
    """Insert vals into tbl. Returns False if insertion failed; True if succeeded.

    tbl should be the name of a table in the database.
    vals should be a comma separated list of values to insert into that databse.
    returns the result of the query, if it is executed.
    """

    if vals == "": "no values provided"
    if tbl.lower() not in _tables: return "invalid table"

    tblpath = os.getcwd() + "/postgres/init/db-files/" + tbl + ".csv"
    cols = ""
    with open(tblpath, "r", encoding="UTF-8") as f:
        cols = f.readline().lower()
        cols = cols.removesuffix("\n")

    try:
        _cur.execute(f"INSERT INTO {tbl} ({cols}) VALUES ({vals})")
        _conn.commit()
    except:
        _conn.rollback()
        return False
    return True


def select(rows="*", tbls="releases", pred=""):
    """Performs simple SFW query. Returns list of tuples. NOT RECOMMENDED FOR MULTI TABLE QUERYING: USE query() instead.

    Rows: a string containing the list of rows to be outputted, default *.
    tbls: a string containing a table or list of tables
    pred: the predicate used to filter tuples in the WHERE clause.

    All values are optional. To perform a "SELECT * FROM Track": select(tbls="Track").
    """

    if(pred != ""):
        _cur.execute(f"SELECT {rows} FROM {tbls} WHERE {pred}")
    else:
        _cur.execute(f"SELECT {rows} FROM {tbls}")

    return _cur.fetchall()


def query(q):
    """Can be used to execute any query, in case other functions don't allow that.

    This function is basically here so you can do aggregates & JOIN ON.
    """

    _cur.execute(q)
    return _cur.fetchall()

def restart_connection():
    _cur.close()
    _conn.close()

    _conn = get_db_connection()
    _cur = _conn.cursor()


def _drop_tables():

    for tbl in _tables:
        _cur.execute(f"DROP TABLE IF EXISTS {tbl.lower()} CASCADE")
