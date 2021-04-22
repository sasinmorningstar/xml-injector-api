from pymongo import MongoClient

client = MongoClient('mongodb+srv://backend_admin:*****@cluster0.vlrhj.mongodb.net/organization?retryWrites=true&w=majority')

organization_db = client.get_database('organization')
details_collection = organization_db.get_collection('details')


def add_row(family, message_type, businessObjectId, payload):
    details_collection.insert_one({'family':family, 'message_type':message_type, 'businessObjectId':businessObjectId,
    'payload':payload})