from flask import Flask, render_template, request
from functions.p2p import P2PNode

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/check_balance", methods = ["POST"])
def check_balance():
    user = request.values["user"]
    balance_user, balance = node.send_messages("check_balance", user)
    
    return render_template("check_balance.html", user = user, balance = balance, balance_user = balance_user)

@app.route("/check_logs", methods = ["POST"])
def check_logs():
    user = request.values["user"]
    logs = node.send_messages("check_logs", user)
    
    return render_template("check_logs.html", user = user, logs = logs)
    
@app.route("/transaction", methods = ["POST"])
def transaction():
    user = request.values["user"]
    amount = request.values["amount"]
    node.send_messages("transaction", f"{user} {amount}")
    
    return render_template("transaction.html", sender = node.ip, receiver = user, amount = amount)


if __name__ == "__main__":
    node = P2PNode()
    node.start()
    
    app.run()