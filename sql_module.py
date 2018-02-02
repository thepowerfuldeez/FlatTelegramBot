import contextlib
import sqlite3


def execute_query(query, values=None):
    with contextlib.closing(sqlite3.connect('offerings.sqlite')) as con:
        if values:
            with con as cur:
                cur.execute(query, values)
        else:
            cur = con.cursor()
            cur.execute(query)
            return list(cur)
