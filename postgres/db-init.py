import psycopg2, os

_tables = ["users", "collection", "musicgroup", "musician", "releases", "track", "creates", "has"]

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="musicdb", user="postgres", password="password", host="localhost", port="5432"
    )
    return conn


def init_db(conn, cur):
    _drop_tables(conn, cur)

    cur.execute(open("postgres/init/init.sql", "r").read())
    
    cwd = os.getcwd() + "/postgres/init/db-files/"
    for tbl in _tables:
        tbldir = cwd + tbl + ".csv"
        with open(tbldir, "r", encoding='UTF-8') as f:
            cols = f.readline().lower().split(",")
            cols[-1] = cols[-1].removesuffix("\n")

            print(f"{tbl}: ({cols})") # FIXME: tester line

            cur.copy_from(f, tbl, sep=",", columns=cols)
            conn.commit()


def _drop_tables(conn, cur):

    for tbl in _tables:
        cur.execute(f"DROP TABLE IF EXISTS {tbl.lower()} CASCADE")


if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()
    init_db(conn, cur)
    conn.close()
    cur.close()