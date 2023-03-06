import pymongo
from pymongo import MongoClient
from pymongo import errors
# import sshtunnel 

# sshtunnel.SSH_TIMEOUT = 5.0
# sshtunnel.TUNNEL_TIMEOUT = 5.0

mongo_url = "mongodb+srv://zachfeatherstone:f7z98knk4ecjd@cluster0.a0qxm9l.mongodb.net/?retryWrites=true&w=majority"
#mongo_url = "mongodb://localhost:27017"

#def insertDocument(server,results):
def insertDocument(results):
    client = pymongo.MongoClient(mongo_url)
    db_list = client.list_database_names()
    if(not 'URLS' in db_list):
        db = client['URLS']
    else:
        db = client.URLS
    collection_list = db.list_collection_names()
    if(not 'URLS' in collection_list):
        collection = db['URLS']
    else:
        collection = db.URLS
    if(len(results) > 0):
        try:
            collection.insert_many(results,ordered=False)
        except errors.BulkWriteError as e:
            print(e)
    print("Successfully inserted into Database")
    #server.close()
    
    return

#def getDocument(server,keyword):
def getDocument(keyword):
    
    
    #client = MongoClient(host='127.0.0.1',port=server.local_bind_port,username='zach',password='zach') # server.local_bind_port is assigned local port
    client = pymongo.MongoClient(mongo_url)
    db = client.URLS
    #print(client.list_database_names())
    collection = db.URLS
    #print(db.list_collection_names())
    myquery = { 'keywords' : {'$regex':keyword}}
    result = collection.find(myquery)
    collection_list = db.list_collection_names()
    if(not 'IDS' in collection_list):
        collection_id = db['IDS']
    else:
        collection_id = db.IDS
    id_cnt = collection_id.count_documents({'keyword':keyword})
    if(id_cnt == 0):
        collection_id.insert_one({'keyword' : keyword,'id_list' : ''})
    id_list = collection_id.find_one({'keyword':keyword})['id_list']
    new_list = []
    for doc in result:
        O_id = str(doc['_id'])
        if(O_id not in  id_list):
            new_list.append({'link' : doc['link'],'keywords' : doc['keywords'],'counts' : doc['counts']})
            id_list = id_list + ',' + O_id   
    collection_id.update_one({'keyword' : keyword},{'$set' : {'id_list' : id_list}},upsert=False)
    return new_list

def getAllHrefs():
    print("---Getting Existing URLS From DB---")
    client = pymongo.MongoClient(mongo_url)
    db = client.URLS
    #print(client.list_database_names())
    collection = db.URLS
    #print(db.list_collection_names())
    result = collection.find({},{'link' : 1})
    print("--Collecting complete---")
    hrefs = []
    for doc in result:
        hrefs.append(doc['link'])
    return hrefs

def insertTargetUrl(target_url):
    print("Adding TargetUrls")
    client = pymongo.MongoClient(mongo_url)
    db = client.URLS
    db_list = client.list_database_names()
    if(not 'URLS' in db_list):
        db = client['URLS']
    else:
        db = client.URLS
    collection_list = db.list_collection_names()
    if(not 'TARGETS' in collection_list):
        collection = db['TARGETS']
    else:
        collection = db.TARGETS
    try:
        collection.insert_one({'link':target_url})
    except errors.BulkWriteError as e:
        print(e)
    print("Successfully inserted target urls into Database")
    
def updateTargetUrl(target_url,origin_url):
    print("Adding TargetUrls")
    client = pymongo.MongoClient(mongo_url)
    db = client.URLS
    db_list = client.list_database_names()
    if(not 'URLS' in db_list):
        db = client['URLS']
    else:
        db = client.URLS
    collection_list = db.list_collection_names()
    if(not 'TARGETS' in collection_list):
        collection = db['TARGETS']
    else:
        collection = db.TARGETS
    print(origin_url)
    print(target_url)
    try:
        collection.update_one({'link' : origin_url},{"$set" : {'link' : target_url}})
    except errors.BulkWriteError as e:
        print(e)
    print("Successfully updated target urls into Database")
    
def getAllTargets():
    print("---Getting Existing URLS From DB---")
    client = pymongo.MongoClient(mongo_url)
    db = client.URLS
    #print(client.list_database_names())
    collection = db.TARGETS
    #print(db.list_collection_names())
    result = collection.find({},{'link' : 1})
    print("--Collecting complete---")
    targets = []
    for doc in result:
        print(doc)
        targets.append(doc['link'])
    return targets

def removeTargetUrl(target_url):
    print("---Getting Existing URLS From DB---")
    client = pymongo.MongoClient(mongo_url)
    db = client.URLS
    #print(client.list_database_names())
    collection = db.TARGETS
    
    collection.delete_one({'link':target_url})
    print("---Successfully removed---")
    result = collection.find({},{'link' : 1})
    print("--Collecting complete---")
    targets = []
    for doc in result:
        targets.append(doc['link'])
    return True
    
