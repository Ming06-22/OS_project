import yaml
import socket
import threading
import time
from collections import defaultdict

from functions.transaction import transaction
from functions.checkBalance import checkBalance
from functions.checkLogs import checkLogs
from functions.read_script import read_script
#from checkChain import checkChain
#from checkAllChains import checkAllChains
from functions.overwrite import overwrite

class P2PNode:
    def __init__(self):
        with open("peers.yaml", "r") as file:
            data = yaml.load(file, Loader = yaml.Loader)
            print(data)
            
        self.ip = data["ip"]
        self.port = data["port"]
        self.peers = data["peers"]
        self.flag = True
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.state = defaultdict(int)

    def start(self):
        threading.Thread(target = self._listen).start()

    def _listen(self):
        while True:
            raw_message, addr = self.sock.recvfrom(16384)
            raw_message = raw_message.decode("utf-8")
            print(f"{addr[0]} {raw_message}")

            msg = raw_message.split(" ")    # "command who amount"
            if msg[0] == "transaction":
                transaction(f"{addr[0]} {msg[1]} {msg[2]}")
            elif msg[0] == "overwrite":
                overwrite(" ".join(msg[1: ]))
            elif msg[0] == "check":
                result = read_script()
                self.sock.sendto(f"state {str(result)}".encode("utf-8"), addr)
            elif msg[0] == "state":
                result = " ".join(msg[1: ])
                self.state[result] += 1

    def send_messages(self, cmd, msg):
        while not self.flag:
            pass

        self.flag = False
        
        if cmd == "transaction":
            scripts = read_script()
            self.state[str(scripts)] += 1
            for peer in self.peers:
                self.sock.sendto("check".encode("utf-8"), peer)

            while sum(self.state.values()) != len(self.peers) + 1:
                pass
                
            print(self.state)

            if len(self.state) == 1:
                self.state = defaultdict(int)
                result = transaction(f"{self.ip} {msg}")
                for peer in self.peers:
                    self.sock.sendto(f"{cmd} {msg}".encode("utf-8"), peer)

                self.flag = True

                return result
            else:
                ledger = count = 0
                for k, v in self.state.items():
                    if v > count:
                        ledger = k

                overwrite(ledger)
                for peer in self.peers:
                    self.sock.sendto(f"{overwrite} {str(ledger)}".encode("utf-8"), peer)

                transaction(f"{self.ip} {msg}")
                for peer in self.peers:
                    self.sock.sendto(f"transaction {msg}".encode("utf-8"), peer)

                self.state = defaultdict(int)

                self.flag = True
                
        elif cmd == "check_balance":
            scripts = read_script()
            self.state[str(scripts)] += 1
            for peer in self.peers:
                self.sock.sendto("check".encode("utf-8"), peer)

            while sum(self.state.values()) != len(self.peers) + 1:
                pass
                
            print(self.state)

            if len(self.state) == 1:
                self.state = defaultdict(int)
            else:
                ledger = count = 0
                for k, v in self.state.items():
                    if v > count:
                        ledger = k

                overwrite(ledger)
                for peer in self.peers:
                    self.sock.sendto(f"{overwrite} {str(ledger)}".encode("utf-8"), peer)

            user = msg
            self.flag = True
            
            return checkBalance(user)
        
        elif cmd == "check_logs":
            scripts = read_script()
            self.state[str(scripts)] += 1
            for peer in self.peers:
                self.sock.sendto("check".encode("utf-8"), peer)

            while sum(self.state.values()) != len(self.peers) + 1:
                pass
                
            print(self.state)

            if len(self.state) == 1:
                self.state = defaultdict(int)
            else:
                ledger = count = 0
                for k, v in self.state.items():
                    if v > count:
                        ledger = k

                overwrite(ledger)
                for peer in self.peers:
                    self.sock.sendto(f"{overwrite} {str(ledger)}".encode("utf-8"), peer)

            user = msg
            self.flag = True
            
            return checkLogs(user)
        
        elif cmd == "checkChain":
            check, m = checkChain()
            print(m)
        elif cmd == "checkAllChains":
            self.state = defaultdict(set)
            correct, sha_value, content = checkAllChains()
            self.state[content].add(((self.ip, self.port), str(correct), sha_value))
            for peer in self.peers:
                self.sock.sendto("check".encode("utf-8"), peer)

            time.sleep(1)

            flag = len(self.state) == 1
            main, length = None, (len(self.peers) + 1) / 2
            for content, msg in self.state.items():
                for m in msg:
                    addr, correct, sha_value = m[0], m[1], m[2]
                    if correct == "False":
                        flag = False
                if len(msg) > length:
                    main = content
                    length = len(m)

            if flag:
                transaction(["Angel", message[1], 100])
                for peer in self.peers:
                    self.sock.sendto(f"transaction Angel {message[1]} 100".encode("utf-8"), peer)
                print("True")
            elif main == None:
                print("It's an untrusted system.")
            else:
                print("False")
                for content, m in self.state.items():
                    if content != main:
                        msg = "overwrite " + main
                        for peer in m:
                            self.sock.sendto(msg.encode("utf-8"), peer[0])