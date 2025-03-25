import pymysql

class ConnectDB:

    config = {
          "host":'47.103.126.208',
          "user":'siyuan',
          "password":'123456',
          "database":'mall',
          "charset":'utf8',
          #"cursorclass":"pymysql.cursors.DictCursor"

    }

    def __init__(self):
        self.connect = pymysql.connect(**self.config)


    def select_datas(self, sql):
        with self.connect.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql)
            data = cur.fetchall()
        return data

    def charge_datas(self, sql):
        pass

    def connect_close(self):
        self.connect.close()

    def __call__(self, act=None, sql=None, connect=True):
        if connect:
            if act == 'select':
                datas = self.select_datas(sql)
                return datas
            elif act in ['update', 'insert', 'delete']:
                self.charge_datas(sql)
                return self
        else:
            self.connect_close()

if __name__ == '__main__':
    connect_db = ConnectDB()
    sql = "SELECT * FROM ls_user WHERE nickname LIKE '%思源%';"
    data1 = connect_db('select', sql)
    data2 = connect_db('select', sql)
    connect_db(connect=False)