import Tkinter

inventory = [3,3,3,3]
inventoryDisplay = []
def BuyItem():
    qr.grid(row=0,column=4)

    

def Refill():
    for i in range(len(inventory)):
        inventory[i]=5
    print(inventory)
    update()
def update():
    a = 0
    for i in inventoryDisplay:
        i.config(text=inventory[a])
        a += 1
def payment():
    qr.grid_remove()
    i = int(entry1.get()) - 1
    if inventory[i] != 0 :
        inventory[i] += -1 
        print(inventory)
    entry1.delete(0, 'end')
    update()


M=Tkinter.Tk() 
M.title('Vending Machine')
Label1 = Tkinter.Label(M, text='Item You want').grid(row=0)
entry1 = Tkinter.Entry(M)

entry1.grid(row=0,column=1)
Snack1 = Tkinter.Label(M, text='1: Ice Tea').grid(row=1,column = 0)

snack = Tkinter.Label(M, text= inventory[0])
snack.grid(row = 1,column = 1)
inventoryDisplay.append(snack)

Snack2 = Tkinter.Label(M, text='2: Coke').grid(row=2,column = 0)

snack = Tkinter.Label(M, text= inventory[1])
snack.grid(row = 2,column = 1)
inventoryDisplay.append(snack)

Snack3 = Tkinter.Label(M, text='3: Sprite').grid(row=3,column = 0)

snack = Tkinter.Label(M, text= inventory[2])
snack.grid(row = 3,column = 1)
inventoryDisplay.append(snack)

Snack4 = Tkinter.Label(M, text='4: Coffe').grid(row=4,column = 0)

snack = Tkinter.Label(M, text= inventory[3])
snack.grid(row = 4,column = 1)
inventoryDisplay.append(snack)


img = Tkinter.PhotoImage(file = "Bicoin.png") 
img1 = img.subsample(2, 2)
qr = Tkinter.Label(M, image = img1)


buy = Tkinter.Button(M, text='Buy', command=BuyItem)
buy.grid(row=0,column=2)
pay = Tkinter.Button(M, text= "Pay" , command=payment)
pay.grid(row=1,column = 2)
refill = Tkinter.Button(M,text="Refill", command=Refill).grid(row=0,column=3)


M.mainloop()