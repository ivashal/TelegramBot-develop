import psycopg2
import urllib.parse as urlparse
import os
import state

if state.local:
    # tmp="postgres://postgres:postgres@127.0.0.1:5432/WORDS"
    tmp = "postgres://vninlnnvrzhuus:88f285ca4ebecf41e3b42c1d8f732b0fd1c80fc99df372b685f2d03196ed0574@ec2-54-243-47-252.compute-1.amazonaws.com:5432/d8pt0b38lc0vem"

class DBInteraction():
    if state.local==False:
        cur_env = os.environ['DATABASE_URL']
    else:
        cur_env=tmp
    url = urlparse.urlparse(cur_env)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    conn = psycopg2.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    def checkConnection(self):
        if self.conn.closed!=0:
            if state.local==False:
                self.cur_env=os.environ['DATABASE_URL']
            else:
                self.cur_env=tmp;
            self.url = urlparse.urlparse(self.cur_env)
            self.dbname = self.url.path[1:]
            self.user = self.url.username
            self.password = self.url.password
            self.host = self.url.hostname
            self.port = self.url.port
            self.conn=psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

    def deleteUsedWords(self):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute("delete from used")
            self.conn.commit()

    def getUsedWords(self,chat_id):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute("select upper(word) from used where chat_id='"+chat_id+"'")
            res=cursor.fetchall()
            return res

    def addUsedWord(self,wrd,chat_id):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute("insert into used(word,chat_id) values('" + wrd + "', '"+chat_id+"')")
            self.conn.commit()

    def DML(self,str):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            for el in str:
                cursor.execute(el)
            self.conn.commit()

    def query(self,str):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute(str)
            res=cursor.fetchall()
            return res

    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.close();
