from sys import (
    version_info,
)  # Found this fix online for me TKinter works but tkinter does not

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
seconds = 5

def create(x): # helper function for making mutiple inventory stocks
    for i in range(x):
        os.system("python default.py %s" % (i))

def order(machines): # used to make a refill order request
    refill_order = {}
    for i in range(len(machines)):
        refill_order[i] = []
        refill_order[i].append(machines[i].Refill_request())
    with open('RefillOrder.txt' ,'w') as outfile:
        json.dump(refill_order, outfile, indent=4,sort_keys=True)





class VendingMachine:
    
    # This is for connecting to a bitcoin node running locally,  in the config file need RPC set up
      # used to keep track of inventory display
    

    def __init__(self, master, id):
        
        self.M = master
        self.id = id
        self.rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % ("User", "Pass"))
        self.inventory = []
        
        # initialize GUI

        self.M.geometry("1000x600")
        self.M.title("Vending Machine")  # set title

        # Setting up ordering bar
        self.Label1 = tk.Label(self.M, text="Item You Want").grid(row=0)
        self.entry1 = tk.Entry(self.M)  # text input
        self.entry1.grid(row=0, column=1)  # adding it to the interface

        # set up the stock display

        with open("Stock_%s.txt" % (self.id)) as json_file:
            stock = json.load(json_file)
            row_count = 1
            for d in stock["Drinks"]:  # cylce through all the drinks
                label = "%s: %s cost:%s stock:%s" % (
                    d["slot"],
                    d["name"],
                    d["cost"],
                    d["stock"],
                )
                drink = tk.Label(self.M, text=label)
                drink.grid(row=row_count, column=0)
                self.inventory.append(drink)
                row_count += 1
            row_count = 1
            for s in stock["Snacks"]:  # cylce through all the snacks
                label = "%s: %s cost:%s stock:%s" % (
                    s["slot"],
                    s["name"],
                    s["cost"],
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

        with open("Stock_%s.txt" %(self.id), "r") as json_file:  # load in stock from the store
            stock = json.load(json_file)
        slot = int(self.entry1.get())  # identify which slot was used

        if slot > 6:
            item = "Snacks"  # figure out what kind of item they are ordering by number of slot, i will probably change the json file to just order based on slot not drinks and snacks
        else:
            item = "Drinks"
        for x in stock["%s" % (item)]:  # cycle through either drinks or snacks
            if int(x["slot"]) == slot:  # search for by item type by its slot
                supply = int(x["stock"])  # check our supply of item
                if supply != 0:  # if we have items in stock
                    adress = (
                        self.rpc_connection.getnewaddress()
                    )  # get a new bitcoin address from the node
                    # generate a bitcoin URI
                    request = "bitcoin:%s?amount=%s" % (adress, x["cost"])
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
                                "Stock_%s.txt" %(self.id), "w"
                            ) as outfile:  # updat JSON to represent the store
                                json.dump(stock, outfile, indent=4, sort_keys=True)
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
        with open("Stock_%s.txt" %(self.id)) as json_file:
            slot = 1
            stock = json.load(json_file)
            for i in self.inventory:  # cycle through the inventory dispaly

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

        self.entry1.delete(0, "end")  # resets the entry bar
        logo = tk.PhotoImage(file="Bitcoin.png").subsample(2, 2)  # get rid of the QR
        self.QR_.config(image=logo)
        self.QR_.photo = logo
        self.QR_.grid(row=0, column=4)
        self.payment_adress.config(text="")
        self.payment_adress.grid(row=1, column=4)
        self.M.update()
    
    def Refill_request(self):
        request = {}
        request["Machine %s" % (self.id)] = []
        
        with open("Stock_%d.txt" % ( self.id)) as json_file:
            slot = 1
            stock = json.load(json_file)
        for d in stock["Drinks"]:
            if int(d["stock"]) < 10:
                i = 10 - int(d["stock"])
                request["Machine %s" % (self.id)].append({
                    'name': str(d["name"]),
                    'amount': i
                })
        for s in stock["Snacks"]:
            if int(s["stock"]) < 10:
                i = 10 - int(s["stock"])
                request["Machine %s" % (self.id)].append({
                    'name': str(s["name"]),
                    'amount': i
                })
        return(request)
        
        

            
        

root = tk.Tk()

Machines = []
for x in range(5):    
    Machines.append(VendingMachine(tk.Toplevel(root),x))
order(Machines)
root.mainloop()


