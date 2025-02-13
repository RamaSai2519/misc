from shared.db.users import get_user_collection, get_subscription_plans_collection, get_user_balances_collection
from shared.models.constants import user_balance_types


class Process:
    def __init__(self):
        self.users_collection = get_user_collection()
        self.balances_collection = get_user_balances_collection()
        self.plans_collection = get_subscription_plans_collection()

    def get_free_plan(self, name: str = 'default') -> dict:
        query = {'name': name}
        plan = self.plans_collection.find_one(query)
        return plan

    def compute(self):
        users = list(self.users_collection.find(
            {}, {'_id': 1, 'isPaidUser': 1}))
        balances = self.balances_collection.distinct('user')

        free_plan = self.get_free_plan()
        paid_plan = self.get_free_plan('club')

        free_plan_keys_to_remove = [
            field for field in free_plan if field not in user_balance_types]
        paid_plan_keys_to_remove = [
            field for field in paid_plan if field not in user_balance_types]

        for field in free_plan_keys_to_remove:
            free_plan.pop(field)
        for field in paid_plan_keys_to_remove:
            paid_plan.pop(field)

        print(free_plan)
        print(paid_plan)
        counter = 0
        for user in users:
            if user.get('isPaidUser') == True:
                plan = paid_plan
            else:
                plan = free_plan
            if user['_id'] not in balances:
                plan['user'] = user['_id']
                plan.pop('_id', None)
                self.balances_collection.insert_one(plan)
                counter += 1
                print(counter)


if __name__ == "__main__":
    process = Process()
    process.compute()
