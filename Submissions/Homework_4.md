1.) By my next Homework I should have a Bitcoin node running on a Raspberry Pi  
The node should be able to produce a payment request and tell when it has been fufilled.   
If I can get the Bitcoin Node up and running sooner then expected then I will also attempt to send the payment request to the GUI  
2.) I was not able to finish getting the Rasberry Pi to Sync it had an error in the middle and had to restart it is showing that it will take another 8 days.  To account for this I just used my laptop which already had a node up and running on it.  For my code I added more comments and changed my inventory over to a text file in JSON format rather then hard coding it in.  I found a library online to use python to do RPC commands to a node and thats what I did.  Because of this I think I will not be switching over to C++ since it works just fine with python.  I use the RPC commands to get a receiving address from the wallet on the node and then I also use the commands to query the balance of the wallet to know when a payment has been procced.  Some challenges that I encountered this homework was with the qr code generation.  That portion took me about 4 hours until I was able to get the qr to proppery display and read out on a Bitcoin wallet.  
3.)  For Homework 5 I am going to design a managerial system that will be able to give out sales reports and also request refills when it gets bellow a certain level and knows how much to order.  If this goes faster then expected then I will be working on making mutiple machines work on the same laptop and have the managerial system be able to handle it.  
4.) Here is what it looks like right now  
Starting  
  
After pressing buy QR code is dispaleyed with an embeded amount  
 
Pay  After you pay it will substract one from inventory and update back to the bitcoin logo