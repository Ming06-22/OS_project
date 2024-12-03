def overwrite(ledger):
    print(type(ledger))
    print(ledger)
    ledger = eval(ledger)
    for filename, content in ledger.items():
        with open(filename, "w") as f:
            for line in content:
                f.write(line)