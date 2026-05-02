import psycopg2, os

_tables = ["users", "collection", "musicgroup", "musician", "releases", "track", "creates", "has"]

def get_db_connection():
    conn = psycopg2.connect(
        dbname="musicdb", user="postgres", password="password", host="localhost", port="5432"
    )
    return conn


_conn = get_db_connection()
_cur = _conn.cursor()


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

            #print(f"{tbl}: ({cols})") # FIXME: tester line

            _cur.copy_from(f, tbl, sep=",", columns=cols)
            _conn.commit()

def insert(tbl="releases", vals = ""):
    """Insert vals into tbl.

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
    
    _cur.execute(f"INSERT INTO {tbl} ({cols}) VALUES ({vals})")
    return "insertion successful"


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

def _drop_tables():

    for tbl in _tables:
        _cur.execute(f"DROP TABLE IF EXISTS {tbl.lower()} CASCADE")


if __name__ == "__main__":
    init_db()

    print("\nTESTING SELECT")
    qres = select("c_id", "collection", "c_id % 2 = 0")
    print(f"qres type: {type(qres)}")
    for s in qres:
        print(s[0])

    
    print("\nTESTING INSERT")
    qres = insert("users", "'password','username','email@mail.com',69")

    print("\nTESTING query")
    print(qres)
    qres = query("""
        SELECT *
        FROM users
        ORDER BY u_id DESC
        LIMIT 1;
    """)
    print(qres)

    _conn.close()
    _cur.close()