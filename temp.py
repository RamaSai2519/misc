from config import prod_client
from temp2 import WhatsappNotificationTemplates

dev_db = prod_client["whatsapp"]
collection = dev_db["templates"]

# Initialize templates
templates = WhatsappNotificationTemplates()


# Function to insert templates into MongoDB
def insert_templates_to_mongo():
    for template_name in dir(templates):
        if not template_name.startswith('__'):
            template = getattr(templates, template_name)
            template['template_name'] = template_name
            collection.insert_one(template)


if __name__ == "__main__":
    insert_templates_to_mongo()
    print("Templates have been successfully inserted into MongoDB.")
