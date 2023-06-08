import psycopg2
import psycopg2.extras

class db_data:

    conn_string = "host='devdb.cnapx.net' dbname = 'korensdb' user = 'cpxapp' password = 'cpxapp!@#$' port = '21011' "


    def fetch_data(self, sql):
        
        conn = psycopg2.connect(self.conn_string)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        cur.execute(sql)
        data_list = cur.fetchall()
        
        convert = []

        for row in data_list:
            convert.append(dict(row))
            
        cur.close()
        conn.close()
        return convert
    
