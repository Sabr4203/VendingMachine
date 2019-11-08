from sys import (
    version_info,
)  # Found this fix online for me TKinter works but tkinter does not

if version_info.major == 2:
    # We are using Python 2.x
    import Tkinter as tk
elif version_info.major == 3:
    # We are using Python 3.x
    import tkinter as tk

import json  # for reading the stores stock took recomendation of storing items on a text file
from bitcoinrpc.authproxy import (
    AuthServiceProxy,
    JSONRPCException,
)  # used to send RPC commands to Bitcoin Node
import qrcode  # to generate a QR
import time  # to keep track of time
import os  # currently using this to reset the store to a deafult with a python script


# This is for connecting to a bitcoin node running locally,  in the config file need RPC set up
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % ("User", "Pass"))


inventory = []  # used to keep track of inventory display

# intialize the start of buying an item and check for stock
def BuyItem():
    unconfirmed = float(
        rpc_connection.getunconfirmedbalance()
    )  # check our unconfirmed balance incase we have a transaction that has not gone through yet

    with open("Stock.txt", "r") as json_file:  # load in stock from the store
        stock = json.load(json_file)
    slot = int(entry1.get())  # identify which slot was used

    if slot > 6:
        item = "Snacks"  # figure out what kind of item they are ordering by number of slot, i will probably change the json file to just order based on slot not drinks and snacks
    else:
        item = "Drinks"
    for x in stock["%s" % (item)]:  # cycle through either drinks or snacks
        if int(x["slot"]) == slot:  # search for by item type by its slot
            supply = int(x["stock"])  # check our supply of item
            if supply != 0:  # if we have items in stock
                adress = (
                    rpc_connection.getnewaddress()
                )  # get a new bitcoin address from the node
                # generate a bitcoin URI
                request = "bitcoin:%s?amount=%s" % (adress, x["cost"])
                # make a QR CODE
                qr = qrcode.make(request, version=1)

                qr.save("qr.png")
                img = tk.PhotoImage(file="qr.png")
                # add QR to GUI
                QR_.config(image=img)
                QR_.photo = img
                QR_.grid(row=0, column=4)
                payment_adress.config(text=adress)  # display address
                M.update()  # update to show qr code
                # below is a timer to allow upto 60 seconds until payment is dropped
                start = time.time()
                elapsed = 0
                while elapsed < 20:
                    if unconfirmed < float(
                        rpc_connection.getunconfirmedbalance()
                    ):  # check if we got any new transactions since displaying the QR
                        x["stock"] = (
                            supply - 1
                        )  # if we have it do a payment and reduce supply
                        with open(
                            "Stock.txt", "w"
                        ) as outfile:  # updat JSON to represent the store
                            json.dump(stock, outfile, indent=4, sort_keys=True)
                        update()
                        break
            else:
                print("Sorry we are out")


def Refill():  # calls python script to generate default store
    os.system("python default.py")
    update()


def update():  # update the store front to reflect the JSON file
    with open("Stock.txt") as json_file:
        slot = 1
        stock = json.load(json_file)
        for i in inventory:  # cycle through the inventory dispaly

            # find item assoiceated with each slot
            if slot > 6:
                item = "Snacks"
            else:
                item = "Drinks"
            for x in stock["%s" % (item)]:
                if int(x["slot"]) == slot:

                    label = "%s: %s cost:%s stock:%s" % (
                        x["slot"],
                        x["name"],
                        x["cost"],
                        x["stock"],
                    )
                    i.config(text=label)
            slot += 1

    entry1.delete(0, "end")  # resets the entry bar
    logo = tk.PhotoImage(file="Bitcoin.png")  # get rid of the QR
    QR_.config(image=logo)
    QR_.photo = logo
    QR_.grid(row=0, column=4)
    payment_adress.config(text="")


# initialize GUI

M = tk.Tk()
M.title("Vending Machine")  # set title

# Setting up ordering bar
Label1 = tk.Label(M, text="Item You Want").grid(row=0)
entry1 = tk.Entry(M)  # text input
entry1.grid(row=0, column=1)  # adding it to the interface

# set up the stock display

with open("Stock.txt") as json_file:
    stock = json.load(json_file)
    row_count = 1
    for d in stock["Drinks"]:  # cylce through all the drinks
        label = "%s: %s cost:%s stock:%s" % (
            d["slot"],
            d["name"],
            d["cost"],
            d["stock"],
        )
        drink = tk.Label(M, text=label)
        drink.grid(row=row_count, column=0)
        inventory.append(drink)
        row_count += 1
    row_count = 1
    for s in stock["Snacks"]:  # cylce through all the snacks
        label = "%s: %s cost:%s stock:%s" % (
            s["slot"],
            s["name"],
            s["cost"],
            s["stock"],
        )
        snack = tk.Label(M, text=label)
        snack.grid(row=row_count, column=1)
        inventory.append(snack)
        row_count += 1

# set up buttons
buy = tk.Button(M, text="Buy", command=BuyItem)
buy.grid(row=0, column=2)

refill = tk.Button(M, text="Refill", command=Refill).grid(row=0, column=3)
# qr
img = tk.PhotoImage(file="Bitcoin.png")

QR_ = tk.Label(M, image=img)
QR_.photo = img
QR_.grid(row=0, column=4)
payment_adress = tk.Label(M, text="")
payment_adress.grid(row=1, column=4)
M.mainloop()

