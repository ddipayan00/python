import json
import dbconnect
import traceback as tb
import psycopg2
#############################################

# event["queryStringParameters"]["name"]

# name = list(event["queryStringParameters"].keys())        ****

# "path": "/getOne",
# "queryStringParameters": {
#       "name": "Dip"
# },

# "multiValueQueryStringParameters": {
#   "name": [
#       "Dip"
#   ],
#   "age": [
#       "20"
#   ]
# },

# "path": "/getOne",

# "resourcePath": "/dev/getOne",

# "stage": "dev"
#############################################
items = []
# def test(event,context):
#     status = ""
#     name = list(event["queryStringParameters"].keys())
#     chg = event["queryStringParameters"]["name"]
#     nam = str(name[0])
#     temp = {}
#     try:
#         flag = False
#         conn = dbconnect.connection()
#         query = conn.cursor()
#         x = query.execute("SELECT * FROM items WHERE " + str(nam) + " = '" + str(chg) + "';")
#         y = query.fetchall()
#         print(list(y))
#         #conn.commit()
#         query.close()
#         conn.close()
#         status = "New Item Added"
#         body = {
#             "message": "Go Serverless v1.0! Your function executed successfully! (CREATE)",
#             "status": status,
#             "output": temp,
#         }
#         response = {
#             "statusCode": 200,
#             "body": json.dumps(body)
#         }
#         return response
#     except Exception as e:
#         body = {
#             "message": "Go Serverless v1.0! Your function executed successfully! (CREATE)",
#             "output": e
#         }
#         response = {
#             "statusCode": 503,
#             "body": json.dumps(body, default=str)
#         }
#         tb.print_exc()
#         return response


def create(event, context):
    status = ""
    name = list(event["queryStringParameters"].keys())
    chg = event["queryStringParameters"]["name"]
    nam = str(name[0])
    temp = {}
    try:
        conn = dbconnect.connection()
        query = conn.cursor()
        q = "SELECT id FROM items WHERE " + str(nam) + " = '" + str(chg) + "';"
        print(q)
        query.execute(q)
        id = list(query.fetchall())
        if query.rowcount != 0:
            d = int(id[0][0])
            status = "Item Is Already Present"
            temp = {"id": d, nam: chg}
        else:
            query.execute("INSERT INTO items (" +
                          str(nam) + ") VALUES ('" +
                          str(chg) + "') RETURNING id;")
            id = list(query.fetchall())
            d = int(id[0][0])
            temp = {"id": d, nam: chg}
            conn.commit()
            status = "New Item Added"
        query.execute("SELECT * FROM items;")
        y = query.fetchall()
        z = []
        if query.rowcount == 0:
            status = "All Items Are Missing"
        else:
            for x in range(len(y)):
                t = {"id": y[x][0], "name": y[x][1]}
                tem = t.copy()
                z.append(tem)
        query.close()
        conn.close()
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (CREATE)",
            "status": status,
            "output": temp,
            "items": z
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (CREATE)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }
        tb.print_exc()
        return response
def getAll(event, context): # GET ALL METHOD
    status = ""
    try:
        conn = dbconnect.connection()
        query = conn.cursor()
        query.execute("SELECT * FROM items;")
        y = query.fetchall()
        z = []
        if query.rowcount == 0:
            status = "All Items Are Missing"
        else:
            status = "All Items Are Available"
            for x in range(len(y)):
                t = {"id":y[x][0],"name":y[x][1]}
                temp = t.copy()
                z.append(temp)
        query.close()
        conn.close()
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (GET ALL)",
            "status": status,
            "items": z
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (GET ALL)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }

        return response

def getOne(event, context): # GET ONE METHOD
    print(psycopg2.__version__)
    status = ""
    name = list(event["queryStringParameters"].keys())
    chg = event["queryStringParameters"]["name"]
    nam = str(name[0])
    try:
        conn = dbconnect.connection()
        query = conn.cursor()
        ################################################
        # c = query.execute("SELECT * FROM items WHERE " +
        #                   str(nam) + " = '" +
        #                   str(chg) + "';")
        ################################################
        p = "SELECT * FROM items WHERE name = %s;"
        c = query.execute(p,(chg,))
        ################################################
        l = query.fetchall()
        zl = []
        conn.commit()
        if query.rowcount == 0:
            status = "Item Missing"
            zl = {"id":c,"name":chg}
        else:
            status = "Item Available"
            for x in range(len(l)):
                t = {"id": l[x][0], nam: l[x][1]}
                tem = t.copy()
                zl.append(tem)
        query.execute("SELECT * FROM items;")
        y = query.fetchall()
        z = []
        if len(y) == 0:
            status = "All Items Are Missing"
        else:
            for x in range(len(y)):
                t = {"id": y[x][0], "name": y[x][1]}
                tem = t.copy()
                z.append(tem)
        query.close()
        conn.close()
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (GET ONE)",
            "status":status,
            "output": zl,
            "items": z
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (GET ONE)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }
        return response

def insert(event, context): # PUT METHOD
    status = ""
    temp = {}
    name = list(event["queryStringParameters"].keys())
    nam = str(name[0])
    chg = event["queryStringParameters"][nam]
    iq = str(name[1])
    chgid = event["queryStringParameters"][iq]
    try:
        conn = dbconnect.connection()
        query = conn.cursor()
        query.execute("SELECT * FROM items WHERE " +
                      str(iq) + " = '" +
                      str(chgid) + "';")
        if query.rowcount != 0:
            query.execute("UPDATE items SET " +
                          str(nam) + " = '" +
                          str(chg) + "' WHERE " +
                          str(iq) + " = " +
                          str(chgid) + "  RETURNING id;")
            conn.commit()
            status = "Item Updated Again"
            temp = {"id": int(chgid), nam: chg}
        else:
            id = query.execute("INSERT INTO items (" +
                               str(nam) + ") VALUES ('" +
                               str(chg) + "') RETURNING id;")
            temp = {"id": id, nam: chg}
            conn.commit()
            status = "New Item Added"
        query.execute("SELECT * FROM items;")
        y = query.fetchall()
        z = []
        for x in range(len(y)):
            t = {"id": y[x][0], nam: y[x][1]}
            tem = t.copy()
            z.append(tem)
        query.close()
        conn.close()
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (INSERT)",
            "status": status,
            "output": temp,
            "items": z
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (INSERT)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }
        return response

def update(event, context): # PATCH METHOD
    status = ""
    temp = {}
    name = list(event["queryStringParameters"].keys())
    nam = str(name[0])
    chg = event["queryStringParameters"][nam]
    iq = str(name[1])
    chgid = event["queryStringParameters"][iq]
    try:
        conn = dbconnect.connection()
        query = conn.cursor()
        query.execute("SELECT * FROM items WHERE " +
                      str(iq) + " = '" +
                      str(chgid) + "';")
        if query.rowcount != 0:
            query.execute("UPDATE items SET " +
                          str(nam) + " = '" +
                          str(chg) + "' WHERE " +
                          str(iq) + " = " +
                          str(chgid) + "  RETURNING id;")
            conn.commit()
            status = "Item Updated"
            temp = {"id": int(chgid), nam: chg}
        else:
            temp = {"id": int(chgid), nam: chg}
            status = "Item Missing"
        query.execute("SELECT * FROM items;")
        y = query.fetchall()
        z = []
        if query.rowcount == 0:
            status = "All Items Are Missing"
        for x in range(len(y)):
            t = {"id": y[x][0], nam: y[x][1]}
            tem = t.copy()
            z.append(tem)
        query.close()
        conn.close()
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (UPDATE)",
            "status": status,
            "output": temp,
            "items": z
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (UPDATE)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }
        return response

def deleteOne(event, context): # DELETE ONE METHOD
    status = ""
    temp = {}
    name = list(event["queryStringParameters"].keys())
    chg = event["queryStringParameters"]["name"]
    nam = str(name[0])
    try:
        z = []
        conn = dbconnect.connection()
        query = conn.cursor()
        id = query.execute("SELECT * FROM items;")
        y = query.fetchall()
        if len(y) == 0:
            status = "All Items Are Missing"
            temp = {"id": id, nam: chg}
        else:
            id = query.execute("DELETE FROM items WHERE " +
                               str(nam) + " = '" +
                               str(chg) + "' RETURNING id;")

            temp = {"id": id, nam: chg}
            if query.rowcount == 0:
                status = "Item Missing"
                query.execute("SELECT * FROM items;")
                y = query.fetchall()
            else:
                conn.commit()
                status = "Item Deleted"
                query.execute("SELECT * FROM items;")
                y = query.fetchall()
        for x in range(len(y)):
            t = {"id": y[x][0], nam: y[x][1]}
            tem = t.copy()
            z.append(tem)
        query.close()
        conn.close()
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (DELETE ONE)",
            "status": status,
            "output": temp,
            "items": z
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (DELETE ONE)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }
        return response

def deleteAll(event, context):  # DELETE METHOD
    conn = dbconnect.connection()
    query = conn.cursor()
    query.execute("DELETE FROM items;")
    temp = []
    conn.commit()
    status = "All Items Are Deleted"
    query.close()
    conn.close()
    try:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (DELETE ALL)",
            "status": status,
            "items": temp
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    except Exception as e:
        body = {
            "message": "Go Serverless v1.0! Your function executed successfully! (DELETE ALL)",
            "output": e
        }
        response = {
            "statusCode": 503,
            "body": json.dumps(body,default=str)
        }
        return response

# Use this code if you don't use the http event with the LAMBDA-PROXY
# integration
# """
# return {
#     "message": "Go Serverless v1.0! Your function executed successfully!",
#     "event": event
# }
# ""
