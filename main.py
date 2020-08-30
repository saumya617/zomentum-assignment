from flask import Flask, jsonify, request 
from flask_cors import CORS 
import pymongo 
import datetime
  
connection_url = 'mongodb+srv://saumya:saumya1706@cluster0.uh9ur.mongodb.net/<dbname>?retryWrites=true&w=majority'
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient(connection_url)


Database = client.get_database('project1')

data_table = Database.data_table
ticketdata = Database.ticketdata

data_table.create_index("time", expireAfterSeconds=8*3600)


@app.route('/ticket_status/movietime/<value>/', methods=['GET'])
def ticketstatus(value):
    qObject = {"movietime": int(value)}
    query = data_table.find(qObject)

    ans = {}
    j = 0
    for i in query:
        ans[j] = i
        j += 1
    return jsonify(ans)


@app.route('/details/id/<value>/', methods=['GET'])
def details(value):
    qObject = {"_id": int(value)} 
    query = data_table.find(qObject)
    ans = {}
    j = 0
    for i in query:
        ans[j] = i
        j += 1
    return jsonify(ans)


@app.route('/deletion/', methods=['POST'])
def deletion():
    _id = request.json["_id"]   
    qObject = {
        '_id': _id,
    }
    data_table.delete_one(qObject) 

    return "deletion successful"


@app.route('/update/id/<oldval>/<newVal>', methods=['GET'])
def update(oldval, newVal):

    qObject = {"_id": int(oldval)}  
    upObject = {"movietime": int(newVal)}  
    Query = ""
    newVal = int(newVal) 
    if newVal == 1:
        count1=Database.data_table.count_documents({"movietime":1})
        if count1 < 20:
            Query = data_table.update_one(qObject, {'$set': upObject})   
        else:
            return "no tickets for 1pm"

    elif newVal == 6:
        count6=Database.data_table.count_documents({"movietime":6})
        if count6 < 20:
            Query = data_table.update_one(qObject, {'$set': upObject})
        else:
            return "no tickets for 6pm"

    if Query.acknowledged:
        return "Query updated"
    else:
        return "Query not updated"

@app.route('/bookmyshow', methods=['POST'])
def bookmyshow():
    username = request.json["username"]
    num = request.json["num"]
    movietime = request.json["movietime"]
    if movietime == 6:
        qobject = {"movietime": 6}
        count6= Database.data_table.count_documents(qobject)

        if count6 < 20:
            qobject = {"ctid": "tcid"}
            query = ticketdata.find_one(qobject)
            counter = query["tcid"]
            
            qobject = {
                'username': username,
                '_id': counter+1,
                'num': num,
                'movietime': 6,
                'time':datetime.datetime.utcnow()
            }
            query = data_table.insert_one(qobject)
            
            qobject = {"ctid": "tcid"}
            upobject = {"tcid": counter+1}
            query = ticketdata.update_one(qobject, {'$set': upobject})

        else:
            return "no tickets left for 6pm"

    elif movietime == 1:
        qobject = {"movietime": 1}
        count1=Database.data_table.count_documents(qobject)
        if count1 < 20:
            qobject = {"ctid": "tcid"}
            query = ticketdata.find_one(qobject)
            counter = query["tcid"]

            qobject = {
                'username': username,
                '_id': counter+1,
                'num': num,
                'movietime': 1,
                'time':datetime.datetime.utcnow()
            }
            query = data_table.insert_one(qobject)

            qobject = {"ctid": "tcid"}
            upobject = {"tcid": counter+1}
            query = ticketdata.update_one(qobject, {'$set': upobject})

        else:
            return "no tickets left for 1pm"

    else:
        return "no show"

    return "Query inserted...!!!"


if __name__ == '__main__':
    app.run(debug=True)