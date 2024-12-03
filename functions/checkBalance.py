import os
from collections import defaultdict

def checkBalance(user):
    file_name = "0.txt"
    folder = os.listdir("./scripts")
    balance_user, balance = 0, defaultdict(int)

    while file_name in folder:
        with open(f"./scripts/{file_name}", "r") as f:
            current_file = f.readlines()
            file_name = current_file[1].split(" ")[-1][: -1]
            for transaction in current_file[2: ]:
                source, target, amount = transaction.split(" ")
                source, target, amount = source[: -1], target[: -1], float(amount[: -1])

                if source == user:
                    balance_user -= amount
                    balance[target] += amount
                elif target == user:
                    balance_user += amount
                    balance[source] -= amount
                else:
                    balance[source] -= amount
                    balance[target] += amount
                    
    return balance_user, balance