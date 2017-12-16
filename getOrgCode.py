import cx_Oracle as cx
import re
from backports import configparser

def generate_namedtuple(cur):
    from collections import namedtuple
    fieldnames = [d[0].lower() for d in cur.description]
    Record = namedtuple('Record', fieldnames)
    rows = cur.fetchall()
    if not rows:
        return
    else:
        return map(Record._make, rows)

def generate_dicts(cur):
    fieldnames = [d[0].lower() for d in cur.description]
    while True:
        rows = cur.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(zip(fieldnames, row))


cf = configparser.ConfigParser()
cf.read("config.ini")

bsp_user = cf.get("orcaledb", "db_user")
bsp_pwd = cf.get("orcaledb", "db_pass")
bshost = cf.get("orcaledb", "db_host")

conn = cx.connect(bsp_user + '/' + bsp_pwd + '@' + bshost + '/orcl')
cursor = conn.cursor()

orgName = '林业'

cursor.execute("select t.short_code from pub_organ t where t.short_name like '%" + orgName + "%'")

row = cursor.fetchall()

cursor.close()
conn.close()

for r in row:
    print(r,end="")

