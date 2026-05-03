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


if __name__ == "__main__":
    init_db()

    #print("\nTESTING SELECT")
    #qres = select("c_id", "collection", "c_id % 2 = 0")
    #print(f"qres type: {type(qres)}")
    #for s in qres:
    #    print(s[0])

    
    #print("\nTESTING INSERT")
    #qres = insert("users", "'password','username','email@mail.com',69")

    #print("\nTESTING query")
    #print(qres)
    #qres = query("""
    #    SELECT *
    #    FROM users
    #    ORDER BY u_id DESC
    #    LIMIT 1;
    #""")
    #print(qres)

    print(get_col_names("collection"))
    print(get_col_names("creates"))
    print(get_col_names("has"))
    print(select())

    _conn.close()
    _cur.close()