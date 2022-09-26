from typing import cast
import firebase_admin as fa
from firebase_admin import firestore
from firebase_admin import auth
import google.cloud.firestore as gcf
import google.cloud.firestore_v1.types as fstypes_1
import google.cloud.firestore_v1.document as doc
import google.cloud.firestore_v1.base_document as fsbd
import datetime

# CREDS_PATH = 'firebase_cert.json'

class FirebaseService:

    def __init__(self, credsPath, token = "1", name = "[DEFAULT]"):
        
        
        # try:
        #     self.projectCreds = fa.credentials.Certificate(credsPath)
        # except FileNotFoundError:
        #     print(f'FileNotFoundError: the file {credsPath} was not found')
        #     return
            # raise FileNotFoundError(f'the file {credsPath} was not found')
        self.projectCreds = fa.credentials.Certificate(credsPath)
        self.app = fa.initialize_app(self.projectCreds, name=name)
        self.fsdb: gcf.Client = firestore.client(app=self.app)
        self.token = auth.create_custom_token(token)

    def set(self, collectionName: str = 'testWrites', documentId: str = "", data: dict = {}, merge: bool = False, uniqueIdName: str = "_id"):
        print('got values: ',data)
        if documentId == "":
            newDocument = self.fsdb.collection(collectionName).document()
            data[uniqueIdName] = newDocument.id
        else:
            newDocument = self.fsdb.collection(collectionName).document(document_id=documentId)
        
        # data["timeUpdated"] = datetime.datetime.now()

        query: fstypes_1.WriteResult = newDocument.set(document_data=data,merge=merge)
        data['time'] = query.__dict__
        return data

    def getSubCollection(self, collectionName: str, documentId: str ,subcollectionName: str):
        print(f'fetching subcollection {subcollectionName} of collection {collectionName}')
        query: list[fsbd.DocumentSnapshot] = self.fsdb.collection(collectionName).document(documentId).collection(subcollectionName).get()
        print(query)
        return query

    def getCollection(self, collectionName: str = 'testWrites') -> "list[dict]":
        print('fetching all the documents of collection ',collectionName)
        query: list[fsbd.DocumentSnapshot] = self.fsdb.collection(collectionName).get()
        # print(query)
        data: list[dict] = []
        for document in query:
            data.append(document.to_dict())
        

        return data
    def getDocument(self, collectionName: str, documentId: str):
        print(f'fetching document {documentId} of collection {collectionName}')
        query: fsbd.DocumentSnapshot = self.fsdb.collection(collectionName).document(documentId).get()
        print(query)
        return query.to_dict()
    
    def getUsersfromAuth(self):
        countUsers = 0
        usersList = []
        page = auth.list_users() # max_results=3
        
        while page:
            print('total users processed: ',len(page.users))
            for user in page.users:
                # print('User: ', user.phone_number, user.user_metadata.creation_timestamp)
                
                userDict = {
                    "uid": user.uid,
                    "phoneNum": user.phone_number,
                    "createdAt": user.user_metadata.creation_timestamp
                }
                usersList.append(userDict)
                countUsers += 1
            page = page.get_next_page()
        # print(countUsers)
        return usersList
    
    
    def whereEqualToQuery(self, collectiionName: str, comparisonMetric: str, comparisonValue: str) -> 'list[dict]':
        print(f"fetching documents where {comparisonMetric} eqauls to {comparisonValue} in collection {collectiionName}")
        query = self.fsdb.collection(collectiionName).where(comparisonMetric, "==", comparisonValue).get()
        allDocs = []
        for data in query:
            allDocs.append(data.to_dict())
        return allDocs    


    # TODO add other firebase CRUD operations as well