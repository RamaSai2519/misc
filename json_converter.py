import re
import json
from config import prodexperts_collection

query = {"persona": {"$type": "string"}}
experts = list(prodexperts_collection.find(query))


def extract_json(json_str: str) -> dict:
    def clean_json(json_str: str) -> str:
        json_str = re.sub(r'//.*', '', json_str)
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
        json_str = json_str.replace("\n", "").replace(
            "```", "").replace("json", "").strip()
        return json_str

    if "json" in json_str:
        match = re.search(r'```json\n(.*?)```', json_str, re.DOTALL)
        if match:
            response_text = clean_json(match.group(1))
            response_text = json.loads(response_text)
            return response_text
    cleaned_json_str = clean_json(json_str)
    return json.loads(cleaned_json_str)


for expert in experts:
    expert["persona"] = extract_json(expert.get("persona", ""))
    if expert["persona"] not in ["", {}]:
        prodexperts_collection.update_one({"_id": expert["_id"]}, {"$set": expert})
        print("Updated expert", expert.get("name", expert["phoneNumber"]))

print("Done")
