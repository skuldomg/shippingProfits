# shippingProfits
Calculates profitable trade routs between the three CX in the browsergame Prosperous Universe (https://prosperousuniverse.com/)

# Requirements
* Python 3.x
* A Prosperous Universe account

# Usage
## Installation
Download the findProfits.py file and brokerdata folder and put them anywhere on your PC.

## Setup
The script requires data from the game that it reads and parses. Since there is no API yet and it is explicitely forbidden to pull any data from the game automatically, you'll need to do a bit of manual work. The brokerdata folder already contains empty .json files where you will copy that gamedata.
1. Set up a new SCRN in-game that contains all three exchanges (buffer comands: **CX CI1**, **CX NC1**, **CX IC1**).
2. Navigate to the first category of each exchange (Agricultural Products). Wait a second for all prices to load and open the browser's developer console (*CTRL+SHIFT+K* in Firefox).
3. You will see a bunch of output in the console, if you just loaded the screen, one of the last statements should read **COMEX_BROKER_DATA**
4. Right-click on **next state > Object { contracts: ...** just below and choose **Copy object**.
5. Paste the contents into **brokerdataAgriculture.json**
6. Repeat steps 2. - 5. with the remaining categories. You don't need to do it for all of them, you can choose the ones you're interested in or leave out useless once (for example Software or most of the Electronics categories).

## Running the script and making sense of the data
1. Run the script with **python findProfits.py**
2. Open the resulting **profits.csv**

The output table displays every product on the CX, how many units can be stored on one ship and its respective ask and bid prices on the different exchanges. **Columns K-P** display the profit per unit when shipping on the respective route. **Column R** tells you the best route, **column S** how much profit you will make with the best route and when filling up your ship completely. **Column T** tells you how much you need to invest up front to buy a shipload of the product.
Negative numbers obviously represent impossible routes (no matching buy/sell orders for the respective CX pair).

# Limitations
* Currently, I **do not account for exchange rates**. All currencies are assumed with a 1:1 conversion rate, which is obviously not the case in-game. For the moment, you will need to manually check the exchange rates to see whether or not they negatively influence the route.
* **Fuel costs** are not accounted for, as they can vary wildly. You will still need to subtract those from your profit. 
* **Check the actual amount of buy/sell orders in-game!** The script calculates profits based off of a whole shipload worth of products, and you may not be able to actually buy/sell the product in that amount for that price in-game. The calculation will only give you a starting point to see at a glance where profits may lie. Always double check manually!

# Errors
If you get an error that looks something like this:
```
    Traceback (most recent call last):
    File ".\findProfits.py", line 105, in <module>
    get_row("HOP")
    File ".\findProfits.py", line 11, in get_row
    weight = float(data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["material"]["weight"])
    KeyError: 'comex'
```
Make sure that you copied the correct object in **Setup step 4**.

# Screenshot
![screenshot](https://i.imgur.com/rTfG4Rk.png)
