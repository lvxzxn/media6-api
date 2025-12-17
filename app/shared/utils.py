from bson import ObjectId


def serialize_mongo_document(doc: dict) -> dict:
    """Converte ObjectId para string."""
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc
