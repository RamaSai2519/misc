from config import produsers_collection

produsers_collection.update_many({}, {"$set": {"wa_opt_out": False}})
