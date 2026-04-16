from pymongo.database import Database
from pymongo import ReturnDocument
from .models import ProductCreate

def get_products(db: Database, name: str = None, min_price: float = None, max_price: float = None):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
            
    cursor = db.products.find(query)
    results = []
    for doc in cursor:
        doc["id"] = doc.get("_id_int", 0) 
        results.append(doc)
    return results

def create_product(db: Database, product: ProductCreate):
    
    last_p = db.products.find_one(sort=[("_id_int", -1)])
    new_id = (last_p["_id_int"] + 1) if last_p and "_id_int" in last_p else 1
    
    doc = product.model_dump()
    doc["_id_int"] = new_id
    
    db.products.insert_one(doc)
    doc["id"] = new_id
    return doc

def get_product_by_id(db: Database, product_id: int):
    doc = db.products.find_one({"_id_int": product_id})
    if doc:
        doc["id"] = doc["_id_int"]
    return doc

def update_product(db: Database, product_id: int, product_update: ProductCreate):
    doc = db.products.find_one_and_update(
        {"_id_int": product_id}, 
        {"$set": product_update.model_dump()}, 
        return_document=ReturnDocument.AFTER
    )
    if doc:
        doc["id"] = doc["_id_int"]
    return doc

def delete_product(db: Database, product_id: int):
    result = db.products.delete_one({"_id_int": product_id})
    return result.deleted_count > 0
