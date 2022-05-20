import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import motor.motor_asyncio
from bson import json_util
import json
import datetime
import pandas as pd


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONNECTION_STRING = "mongodb+srv://shalin:shalin.7031@cluster0.e8nnx.mongodb.net/test"

######################################################## UTILITY FUNCTIONS ##############################################

async def getDataFromDB(colName):
    
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection(colName)
    cursor = collection.find()
    
    try:
        data = await cursor.to_list(None)
        return json.loads(json_util.dumps(data))

    except Exception:
        return "Unable To Connect To The Server"


async def getIdsData(ids, colName,idcode):
    data = []
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection(colName)

    try:
        for id in ids:
            cursor = await collection.find_one({idcode: {'$eq': id}})
            data.append(cursor)
        return json.loads(json_util.dumps(data))

    except Exception:
        return "Unable To Connect To The Server"



async def getIdData(id, colName, idcode):
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection(colName)

    try:
        cursor = await collection.find_one({idcode: {'$eq': id}})
        return json.loads(json_util.dumps(cursor))

    except Exception:
        return "Unable To Connect To The Server"


async def checkLoginData(colName, userName, password):

    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection(colName)
    
    try:
        # cursor = await collection.find_one({"$and": [{'userName': userName, 'password' : password}]})
        # cursor = await collection.find_one({'userName': userName, 'password' : password}, projection = {'_id': False, 'password': False, 'centres': False, 'members': False})
        cursor = await collection.find_one({'userName': userName, 'password' : password})
        if cursor:
            # statusCursor = json.loads(cursor)
            statusCursor = {'status' : True}
            statusCursor.update(cursor)
            return json.loads(json_util.dumps(statusCursor))
        else:
            return json.loads(json_util.dumps({'status' : False}))
        
    except Exception:
        return json.loads(json_util.dumps(False))



async def addDataToDB(colName, dataObj):  
   
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection(colName)
   
    try:
        await collection.insert_one(dataObj)
        return "Successfully Added Your Data"

    except Exception:
        return "Duplicate Data Entered OR Unable To Connect To The Server"


async def appendParentToDB(parentID, parentName, studentId):  
   
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection("parents")
   
    try:
        result = await collection.update_one({'pid' : parentID}, {'$set': {'name' : parentName, 'sid':studentId}})
        return { "status" : True, 'pid': parentID }

    except Exception:
        return { "status" : False, 'pid': None }


async def updateParentData(parentId, parent):  
   
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection("parents")
   
    try:
        result = await collection.update_one({'pid': parentId}, { '$set' : {'name' : parent['name'], 'userName' : parent['userName'] , 'password' : parent['password']}})
        # result = await collection.update_one({'_id': centreId}, { '$push' : {'centreName' : centre['centreName']}})
        return "Centre Details Updated Successfully"

    except Exception:
        return "Unable To Connect To The Server"


async def getIndexFromDB(colName):
    
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)

    database = client["edAssist"]
    collection = database.get_collection(colName)
    
    try:
        return await collection.count_documents({})

    except Exception:
        return "Unable To Connect To The Server"



def getNextId(colName):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return int(loop.run_until_complete(getIndexFromDB(colName))) + 1


############################################################ API FUNCTIONS ############################################################
@app.get("/")
def info():
    return "Welcome to EdAssist"


@app.get("/checkParentLogin")
def checkLogin(userName : str, password : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(checkLoginData("parents", userName, password))



@app.get("/getStudentCourseList")
def getStudentCourseList(sid : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ids = loop.run_until_complete(getIdData(sid, 'students', 'sid'))['courses']
    print(ids)
    # return loop.run_until_complete(getIdsData(ids, 'centre')))
    return (loop.run_until_complete(getIdsData(ids, 'courses', 'subid')))


@app.get("/registerParent/")
def registerParent(parentName: str, userName: str, password: str):
    parentName = parentName.upper()
    pid = 'p'+ str(getNextId("parents"))
    sid = 'std' + str(getNextId("parents"))
    parent = {
        "pid" : pid,
        "name" : parentName,
        "userName" : userName,
        "password" : password,
        "sid" : sid
    }
   
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(addDataToDB("parents", parent))

    if(result == "Successfully Added Your Data"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(appendParentToDB(pid, parentName, sid))
    else:
        return result

@app.get("/getParentDetails")
def getParentDetails(parentID : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(getIdData(parentID, "parents",'pid'))

@app.get("/getStudentDetails")
def getStudentDetails(studentID : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(getIdData(studentID, "students",'sid'))

@app.get("/getTeacherDetails")
def getStudentDetails(teacherID : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(getIdData(teacherID, "teachers",'tid'))

@app.get("/getStudentFromParent")
def getStudentFromParent(parentID : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sid = loop.run_until_complete(getIdData(parentID, "parents",'pid'))['sid']
    return loop.run_until_complete(getIdData(sid, "students",'sid'))



