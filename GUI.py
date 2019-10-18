import Tkinter
M=Tkinter.Tk() 
M.title('Vend ing Machine')
Label(M, text='Item You want').grid(row=0)
e1 = Entry(M)
e1.grid(row=0,column=1)
M.mainloop()