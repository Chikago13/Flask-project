PG_CONNECT= dict(host = '127.0.0.1', database = 'mybase', user= 'alex', password = '12345')

def connect_mybase():
    import psycopg2
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    return psycopg2.connect(**PG_CONNECT)

def connect(dbname):
    if dbname == 'mybase':
        conn = connect_mybase()
    else:
        return None
    return conn


def cuery(dbname, sql, args=None, one=False, upd=False, debug=False, fetch_upd_return=False):
    con = connect(dbname)
    try:
        cur = con.cursor()
        try:
            if args is None:
                if debug:
                    print(sql)
                cur.execute(sql)
            else:
                if debug:
                    print(cur.mogrify(sql, args))
                cur.execute(sql, args)
            if upd:
                con.commit()
                if fetch_upd_return:
                    return cur.fetchone()
                else:
                    return cur.rowcount
            if one:
                return cur.fetchone()
            else:
                return cur.fetchall()
        except Exception as e:
            print(e)
            if upd:
                con.rollback()
        finally:
            cur.close()
    except Exception as e:
        print(e)
        pass
    finally:
        con.close()