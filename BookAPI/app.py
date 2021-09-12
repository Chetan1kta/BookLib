from flask import Flask
from flask_cors import CORS
import pyodbc
import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=.\SQLEXPRESS;"
            "Database=BookDB;"
            "Trusted_Connection=yes;")

@app.route("/booklist/<author_name>", methods=['GET'])
@app.route("/booklist", methods=['GET'])

def booklist(author_name = ""):
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    query = " SELECT b.Id AS [BookId],b.BookName AS [BookName],a.AuthorName FROM tb_Books b INNER JOIN tb_Author a ON a.Id = b.AuthorId "
    if IsNotNull(str(author_name)):
        query = query + " WHERE a.AuthorName LIKE '%" + str(author_name) + "%'"
    data = cursor.execute(query)
    row_headers = [x[0] for x in cursor.description] #this will extract row headers
    rv = data.fetchall()
    del cnxn
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

@app.route("/bookdetail/<int:book_id>",methods = ['GET'])
def bookdetail(book_id=0):
    query = (" SELECT b.BookName AS [BookName],ISNULL(a.AuthorName,'') AS [AuthorName],ISNULL(b.Details,'') AS [Details] "  
             " FROM tb_Books b INNER JOIN tb_Author a ON a.Id = b.AuthorId "
             " WHERE b.Id = " + str(book_id))

    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    data = cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    rv = data.fetchall()
    del cnxn
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

def IsNotNull(value):
    return value is not None and len(value) > 0

if __name__ == 'main':
    app.run(debug=True,port=5000)