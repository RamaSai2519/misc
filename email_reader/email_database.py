from typing import Dict, Any
import sys
import os
print(os.getcwd())
sys.path.append(os.getcwd())


class EmailDatabase:
    def __init__(self, db_name: str = 'test', collection_name: str = 'emails') -> None:
        from shared.db.base import Database
        self.client = Database().client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_email(self, email_data: Dict[str, Any]) -> None:
        self.collection.insert_one(email_data)

    def close(self) -> None:
        self.client.close()
