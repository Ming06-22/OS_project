import os

def read_script():
    result = {}
    folder = os.listdir("./scripts")
    
    with open("./scripts/0.txt", "r") as f:
        file = f.readlines()
        result["./scripts/0.txt"] = file
        next_file = file[1].split(" ")[-1][: -1]
    
    while next_file in folder:
        with open(f"./scripts/{next_file}", "r") as f:
            file = f.readlines()
            result[f"./scripts/{next_file}"] = file
            next_file = file[1].split(" ")[-1][: -1]

    return result