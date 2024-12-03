import os, random
from hashlib import sha256

def transaction(msg):
    msg = msg.split(" ")
    source, target, amount = msg[0], msg[1], msg[2]

    folder = os.listdir("./scripts")
    if "0.txt" not in folder:
        with open(f"./scripts/0.txt", "w") as f:
            f.write("Sha256 of previous block: None\n")
            
            next_file = f"{random.randint(1, 1000)}.txt"
            while next_file in folder:
                next_file = f"{random.randint(1, 1000)}"
            f.write(f"Next block: {next_file}\n")
            
            f.write(f"{source}, {target}, {amount}\n")
            
        return f"Add transaction: {source}, {target}, {amount}"

    file_name = "0.txt"
    with open("./scripts/0.txt", "r") as f:
        file = f.readlines()
        next_file = file[1].split(" ")[-1][: -1]
        
    while next_file in folder:
        file_name = next_file
        with open(f"./scripts/{file_name}", "r") as f:
            file = f.readlines()
            next_file = file[1].split(" ")[-1][: -1]

    with open(f"./scripts/{file_name}", "r") as f:
        file = f.readlines()

    if len(file) == 7:
        sha256_hash = sha256()
        with open(f"./scripts/{file_name}", "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            hash_value = sha256_hash.hexdigest()

        with open(f"./scripts/{next_file}", "w") as f:
            f.write(f"Sha256 of previous bolck: {hash_value}\n")
            
            next_file = f"{random.randint(1, 1000)}.txt"
            while next_file in folder:
                next_file = f"{random.randint(1, 1000)}"
            f.write(f"Next block: {next_file}\n")
            
            f.write(f"{source}, {target}, {amount}\n")
    else:
        with open(f"./scripts/{file_name}", "a") as f:
            f.write(f"{source}, {target}, {amount}\n")
    
    return f"Add transaction: {source}, {target}, {amount}"