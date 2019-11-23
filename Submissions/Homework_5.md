1.) For Homework 5 I am going to design a managerial system that will be able to give out sales reports and also request refills when it gets bellow a certain level and knows how much to order.  If this goes faster then expected then I will be working on making mutiple machines work on the same laptop and have the managerial system be able to handle it. 

2.) I was really ill for this past run and was not able to achieve as much as I wanted.  First off i took the time to convert the entire script into a more Object Oriented style.  I then changed the Functions to be more dynamic and be able to read off of mutiple json files.  I am able to have multiple instance of vending machines all with their own Stock.  Things that set me back was I had a tough time getting mutiple instances to work with a tkinter window.  I finally found out that it would be a better idea to just generate them like pop-up windows on a main window.   
3.)   For the next run I hope to be able to interact with mutiple vending mahcines at once and I need to put some intelegence behind the managerial system right now it just makes a JSON of what each machine will need to refill.  I think I can make the Main Window sort of like a managerial view but im not sure yet.  I ended up not using Kafka since I am doing everything in PYTHON right now and dont need a message handling system.
4.) Here is what it looks like right now  
Starting  
![Start(2)](https://user-images.githubusercontent.com/46725794/68518536-8eceb100-0249-11ea-80ff-81b1ab3723f1.jpg)  

 
After pressing buy QR code is displayed with an embeded amount and an address at the bottom to account for MTM Attacks 
![Buy(2)](https://user-images.githubusercontent.com/46725794/68518525-86767600-0249-11ea-80f3-6945c35e6253.jpg)


Pay  After you pay it will substract one from inventory and update back to the bitcoin logo
![pay(2)](https://user-images.githubusercontent.com/46725794/68518533-8c6c5700-0249-11ea-9d42-5d4e4465b3f2.jpg)
