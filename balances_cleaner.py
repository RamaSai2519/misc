from shared.db.users import get_user_collection, get_user_balances_collection

users_collection = get_user_collection()
balances_collection = get_user_balances_collection()

user_ids = users_collection.distinct('_id')
balance_ids = balances_collection.distinct('user')

for id in balance_ids:
    if id not in user_ids:
        balances_collection.delete_one({'user': id})
        print(f"Deleted balance for user {id}")
