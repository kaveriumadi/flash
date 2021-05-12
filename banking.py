import sqlite3
from flask import Flask, request
from flask import jsonify

app = Flask(__name__)
app.config[""] = "sqlite3:///C:/Users\KAVU/eclipse-workspace/flask_practice/python_practice/bank.db"


conn = sqlite3.connect('bank.db')

def commit(conn):
    print('db_commit() ...')
    #import pdb
    #pdb.set_trace()
    conn.commit()
    
def init_db(conn):
    print('init_db() ...')
    cur = conn.cursor()
    return cur

def close_db(conn):
    print('close_db() ...')
    conn.close()
    
@app.route('/cur')   
def create_table(cur):
    print('create_table() ...')
    cur.execute("""DROP TABLE IF EXISTS Banks""")
    cur.execute("""CREATE TABLE Banks
            (bank_name text, ifsc text, accno integer, holder_name text)""")
    
@app.route('/records', methods=['POST'])
def post_recs():
    print('post_recs() ...')
    
    payload = request.json
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()

    for i in payload:
        cur.execute("""INSERT INTO Banks VALUES (?,?,?,?)""",
                    (i['accno'], i['bank_name'], i['ifsc'], i['holder_name']))
 
    commit(conn) 
    return 'success'

@app.route('/fetch_alls', methods=['GET'])
def fetch_recs():
    print('fetch_recs() ...')
    
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()
    #import pdb;pdb.set_trace()
    sql1 = 'SELECT * FROM Banks' 
    cur.execute(sql1)
    recs = cur.fetchall()
    
    print(recs)
    
    return jsonify(recs) 

@app.route('/fetch_one/<int:accno>', methods=['GET'])
def fetch_rec(accno):
    print('fetch_recs() ...')
    
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()
    #import pdb;pdb.set_trace()
    sql1 = f"SELECT * FROM Banks where accno={accno}" 
    cur.execute(sql1)
    recs = cur.fetchall()
    
    
    print(recs)
    
    return jsonify(recs)

@app.route('/update_recs/<int:accno>', methods=['PUT'])    
def update_rec(accno):
    print("update records")
    
    payload = request.json
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()
    #import pdb;pdb.set_trace()
    for i in payload:
        #import pdb;pdb.set_trace()
        var = f"update Banks set bank_name=\'{i['bank_name']}\', ifsc=\'{i['ifsc']}\', holder_name=\'{i['holder_name']}\' where accno={i['accno']}"
        cur.execute(var)
      
    print("updated")
    commit(conn) 
    return 'success'

@app.route('/recs_all', methods=['PUT'])    
def update_recs():
    print("update records")
    payload = request.json
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()
    
    for i in payload:
        var = f"update Banks set bank_name=\'{i['bank_name']}\', ifsc=\{i['ifsc']}\, holder_name=\'{i['holder_name']}\' where accno={i['accno']}"
        cur.execute(var)
      
    print("updated")
    commit(conn) 
    return 'success'


@app.route('/record/<int:accno>', methods=['DELETE'])    
def delete_rec(accno):
    print("delete records")
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()

    sql = f'DELETE from  Banks WHERE accno={accno}'
    cur.execute(sql)
    commit(conn) 
    return 'success'

    
    
if __name__ == '__main__':   
        app.run(debug=True)