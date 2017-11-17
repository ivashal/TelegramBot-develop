import dbInteraction


def getToken():
    conn=dbInteraction.DBInteraction()
    res=conn.query('select token from tokens')
    return res[0][0]