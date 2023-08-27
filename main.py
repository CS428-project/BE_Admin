from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import pyodbc
import models
# from database import Database

image_path = "./image/"


#               CONNECTION TO DATABASE
def database_connection():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=mssql-138433-0.cloudclusters.net,18705;PORT=18705;DATABASE=eCommerce;UID=Admin;PWD=Admin123')


#               DATABASE COMMAND
class Database:
    def __init__(self):
        self.conn = database_connection()
        self.cursor = self.conn.cursor()
        pass

    #get List of Mentor
    def getListMentor(self) -> list:
        command = "EXEC sp_getListMentor"
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append({x for x in i})
        return result
    
    #add Mentor
    def addMentor(self, mentor: models.MentorInfo):
        command = "EXEC sp_InsertMentor '%s', '%s', '%s', '%s'" % (mentor.language, mentor.fieldID, mentor.description, mentor.rating)

        self.cursor.execute(command)
        self.conn.commit()
        return "SUCCESS"
    
    #delete Mentor
    def deleteMentor(self, mentorid):
        command = "EXEC sp_deleteMentor '"+str(mentorid)+"'"
        self.cursor.execute(command)
        self.conn.commit()
        return "SUCCESS"

###################################################################################################################
#           MAIN PART
###################################################################################################################
app = FastAPI()
database = Database()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#get Mentor List
@app.get('/mentors/', tags=['Mentor List'])
async def getListMentor():
    return database.getListMentor()

#add Mentor
@app.post("/mentors/", response_model=models.MentorInfo)
def addMentor(mentor: models.MentorInfo):
    return database.addMentor(mentor)

#delete Mentor
@app.delete("/mentors/")
def deleteMentor(mentorid):
    return database.deleteMentor(mentorid)
