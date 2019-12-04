

from sys import (
    version_info,
)  # Found this fix online for me TKinter works but tkinter does not
import random
import requests


if version_info.major == 2:
    # We are using Python 2.x
    import Tkinter as tk
elif version_info.major == 3:
    # We are using Python 3.x
    import tkinter as tk

import json  # for reading the stores stock,  took recomendation of storing items on a text file
from bitcoinrpc.authproxy import (
    AuthServiceProxy,
)  # used to send RPC commands to Bitcoin Node
import qrcode  # to generate a QR
import time  # to keep track of time
import os  # currently using this to reset the store to a deafult with a python script

seconds = 30  # time to pay for transaction
number_of_machines = 2  # how many instances of machines we want
BitcoinURL = "https://api.coinmarketcap.com/v1/ticker/bitcoin"


def create(x):  # helper function for making mutiple inventory stocks
    for i in range(x):
        os.system("python default.py %s" % (i))


class VendingMachine:
    def __init__(self, master, id, price):
        self.price = price
        self.M = master
        self.id = id
        self.rpc_connection = AuthServiceProxy(
            "http://%s:%s@127.0.0.1:8332" % ("User", "Pass")
        )
        # This is for connecting to a bitcoin node running locally,  in the config file need RPC set up
        # used to keep track of inventory display
        self.inventory = []
        self.sales = 0
        # initialize GUI

        self.M.geometry("1000x600")
        self.M.title("Vending Machine %d" % (self.id))  # set title

        # Setting up ordering bar
        self.Label1 = tk.Label(self.M, text="Item You Want").grid(row=0)
        self.entry1 = tk.Entry(self.M)  # text input
        self.entry1.grid(row=0, column=1)  # adding it to the interface

        # set up the stock display

        with open("Stock_%s.json" % (self.id)) as json_file:
            stock = json.load(json_file)
            row_count = 1
            for d in stock["Drinks"]:  # cylce through all the drinks
                label = "%s: %s BTC:%.6f stock:%s" % (
                    d["slot"],
                    d["name"],
                    float(d["cost"])/self.price,
                    d["stock"],
                )
                drink = tk.Label(self.M, text=label)
                drink.grid(row=row_count, column=0)
                self.inventory.append(drink)
                row_count += 1
            row_count = 1
            for s in stock["Snacks"]:  # cylce through all the snacks
                label = "%s: %s BTC:%.6f stock:%s" % (
                    s["slot"],
                    s["name"],
                    float(s["cost"])/self.price,
                    s["stock"],
                )
                snack = tk.Label(self.M, text=label)
                snack.grid(row=row_count, column=1)
                self.inventory.append(snack)
                row_count += 1

        # set up buttons
        self.buy = tk.Button(self.M, text="Buy", command=self.BuyItem)
        self.buy.grid(row=0, column=2)

        self.refill = tk.Button(self.M, text="Refill", command=self.Refill).grid(
            row=0, column=3
        )
        # qr
        img = tk.PhotoImage(file="Bitcoin.png").subsample(2, 2)

        self.QR_ = tk.Label(self.M, image=img)
        self.QR_.photo = img
        self.QR_.grid(row=0, column=4)
        self.payment_adress = tk.Label(self.M, text="")
        self.payment_adress.grid(row=1, column=4)

    # intialize the start of buying an item and check for stock
    def BuyItem(self):
        unconfirmed = float(
            self.rpc_connection.getunconfirmedbalance()
        )  # check our unconfirmed balance incase we have a transaction that has not gone through yet

        with open(
            "Stock_%s.json" % (self.id), "r"
        ) as json_file:  # load in stock from the store
            stock = json.load(json_file)
        slot = int(self.entry1.get())  # identify which slot was used

        for i in stock:  # cycle through either drinks or snacks
            for x in stock[i]:
                if int(x["slot"]) == slot:  # search for by item type by its slot
                    supply = int(x["stock"])  # check our supply of item
                    if supply != 0:  # if we have items in stock
                        adress = (
                            self.rpc_connection.getnewaddress()
                        )  # get a new bitcoin address from the node
                        # generate a bitcoin URI
                        request = "bitcoin:%s?amount=%.6f" % (adress, float(x["cost"])/self.price)
                        # make a QR CODE

                        self.QR_gen = qrcode.QRCode(version=1, box_size=5)
                        self.QR_gen.add_data(request)
                        self.QR_gen.make()
                        qr = self.QR_gen.make_image()

                        qr.save("qr.png")
                        img = tk.PhotoImage(file="qr.png")
                        # add QR to GUI
                        self.QR_.config(image=img)
                        self.QR_.photo = img
                        self.QR_.grid(row=0, column=4)
                        self.payment_adress.config(text=adress)  # display address
                        self.M.update()  # update to show qr code
                        # below is a timer for an alloted time until payment is dropped
                        start = time.time()
                        elapsed = 0
                        while elapsed < seconds:
                            if unconfirmed < float(
                                self.rpc_connection.getunconfirmedbalance()
                            ):  # check if we got any new transactions since displaying the QR
                                x["stock"] = (
                                    supply - 1
                                )  # if we have it do a payment and reduce supply
                                with open(
                                    "Stock_%s.json" % (self.id), "w"
                                ) as outfile:  # updat JSON to represent the store
                                    json.dump(stock, outfile, indent=4, sort_keys=True)
                                self.sales += float(x["cost"])/self.price
                                self.update()
                                break
                            elapsed = time.time() - start
                        self.update()

                    else:
                        print("Sorry we are out")

    def Refill(self):  # calls python script to generate default store
        os.system("python default.py %s" % (self.id))
        self.update()

    def update(self):  # update the store front to reflect the JSON file
        with open("Stock_%s.json" % (self.id)) as json_file:
            slot = 1
            stock = json.load(json_file)
            for i in self.inventory:  # cycle through the inventory dispaly

                for j in stock:
                    for x in stock[j]:
                        if int(x["slot"]) == slot:

                            label = "%s: %s BTC:%.6f stock:%s" % (
                                x["slot"],
                                x["name"],
                                float(x["cost"]) / self.price,
                                x["stock"],
                            )
                            
                            i.config(text=label)
                slot += 1

        self.entry1.delete(0, "end")  # resets the entry bar
        logo = tk.PhotoImage(file="Bitcoin.png").subsample(2, 2)  # get rid of the QR
        self.QR_.config(image=logo)
        self.QR_.photo = logo
        self.QR_.grid(row=0, column=4)
        self.payment_adress.config(text="")
        self.payment_adress.grid(row=1, column=4)
        self.M.update()

    def RefillRequest(self):  # generate a refill request
        request = {}
        request["Machine %s" % (self.id)] = []

        with open("Stock_%d.json" % (self.id)) as json_file:
            slot = 1
            stock = json.load(json_file)
        for d in stock["Drinks"]:
            if int(d["stock"]) < 10:
                i = 10 - int(d["stock"])
                request["Machine %s" % (self.id)].append(
                    {"name": str(d["name"]), "amount": i}
                )
        for s in stock["Snacks"]:
            if int(s["stock"]) < 10:
                i = 10 - int(s["stock"])
                request["Machine %s" % (self.id)].append(
                    {"name": str(s["name"]), "amount": i}
                )
        return request

    def GenerateSales(
        self,
    ):  # used to fake sales in testing faster than manually doing all the transactions
        with open(
            "Stock_%s.json" % (self.id), "r"
        ) as json_file:  # load in stock from the store
            stock = json.load(json_file)
        # will try to but random amounts of each item up to what we have
        for i in stock:
            for x in stock[i]:
              fake_sales = random.randrange(1, 10, 1)
              if fake_sales <= int(x["stock"]):
                self.sales += fake_sales * float(x["cost"])/self.price

                x["stock"] = int(x["stock"]) - fake_sales  


        
        with open(
            "Stock_%s.json" % (self.id), "w"
        ) as outfile:  # updat JSON to represent the store
            json.dump(stock, outfile, indent=4, sort_keys=True)
        self.update()

    def unload(
        self, address
    ):  # To handle consolidating inputs after a set amount TODO: Need to figure out where to consolidate too
        pass


class Manager:
    def __init__(self, master, machines):
        self.master = master
        self.machines = machines
        # initalize the GUi for the Managment window
        self.master.geometry("500x500")
        self.master.title("Managment View")
        # used to ping an API and get current price of bitoin
        self.response = requests.get(BitcoinURL)
        self.response_json = self.response.json()
        self.Price = float(self.response_json[0]["price_usd"])
        self.Price_tracker = tk.Label(
            self.master, text="Price of Bitcoin %.2f" % (self.Price)
        )
        self.Price_tracker.pack()
        

        self.labels = []
        for i in range(len(self.machines)):
            self.Label = tk.Label(
                self.master,
                text="Machine_%d Sales in BTC: %f Sales in USD: %.2f"
                % (i, self.machines[i].sales, self.machines[i].sales * self.Price),
            )

            self.Label.pack()
            self.labels.append(self.Label)
        self.Total = tk.Label(self.master, text="Total Sales BTC: 0 USD:0")
        self.Total.pack()
        # refill button
        self.Refill_button = tk.Button(
            self.master, text="Generate Refill Order", command=self.order
        ).pack()
        self.FakeSales_button = tk.Button(
            self.master, text="Fake sales", command=self.FakeSales
        ).pack()
        self.Refill_button = tk.Button(
            self.master, text="Refill all", command=self.Restock
        ).pack()
        self.update()
        

    def update(self):  # this loops to update and reflect all the machines
        total = 0
        self.response = requests.get(BitcoinURL)
        self.response_json = self.response.json()
        self.Price = float(self.response_json[0]["price_usd"])
        self.Price_tracker.config(text="Price of Bitcoin %.2f" % (self.Price))
        for i in range(len(self.machines)):
            total += self.machines[i].sales
            self.labels[i].config(
                text="Machine_%d Sales in BTC: %f Sales in USD: %.2f"
                % (i, self.machines[i].sales, self.machines[i].sales * self.Price)
            )
            self.machines[i].price = self.Price
            self.machines[i].update()
        print(self.Price)
        self.Total.config(
            text="Total Sales BTC: %f USD: %.2f" % (total, self.Price * total)
        )
        self.master.update()
        self.master.after(10000, self.update)

    def Restock(self):  # will refill all the machines
        for i in self.machines:
            i.Refill()
    
    def order(self):  # used to make a refill order request
        refill_order = {}
        for i in range(len(self.machines)):
            refill_order[i] = []
            refill_order[i].append(self.machines[i].RefillRequest())
        with open("RefillOrder.json", "w") as outfile:
            json.dump(refill_order, outfile, indent=4, sort_keys=True)

    def FakeSales(self):  # used to generate fake sales on each machine
        for i in self.machines:
            i.GenerateSales()


root = tk.Tk()
response = requests.get(BitcoinURL)
response_json = response.json()
Price = float(response_json[0]["price_usd"])

Machines = []
for x in range(number_of_machines):
    Machines.append(VendingMachine(tk.Toplevel(root), x, Price))

Managment = Manager(root, Machines)
"""
TODO: finish to clear wallet after a certain amount,  Started to change json file to update with bitcoin Price
CURRENT ISSUES: can only interact with one vending machine at a time, also all of it is running off of one script would be better to split up so I can have mutplie at once
"""

root.mainloop()

