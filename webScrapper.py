import requests
import time
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from termcolor import colored, cprint

xlkPrevious = 0
vooPrevious = 0

americaDate = ""
localdate = ""

def closed():
	americaTime = datetime.now(timezone('US/Eastern'))
	open_time_string = "09:30:00"
	close_time_string = "16:00:00"

	openTime = datetime.strptime(open_time_string, "%H:%M:%S")
	openTime = americaTime.replace(hour=openTime.time().hour, minute=openTime.time().minute, second=openTime.time().second, microsecond=0)

	closeTime = datetime.strptime(close_time_string, "%H:%M:%S")
	closeTime = americaTime.replace(hour=closeTime.time().hour, minute=closeTime.time().minute, second=closeTime.time().second, microsecond=0)
	weekno = datetime.now(timezone('US/Eastern')).weekday()

	if weekno<5:
		return americaTime > openTime
	else:	
    		print("The market is closed now!!!")

	return False

def getPage(url):
	return requests.get(url)	

def getCurDate():
	return datetime.now().strftime("%d/%m/%Y")

def getUSCurDate():
	return datetime.now(timezone('US/Eastern')).strftime("%d/%m/%Y")

def getCurTime():
	return datetime.now().strftime("%H:%M")

def getCurUSTime():
	return datetime.now(timezone('US/Eastern')).strftime("%H:%M")

def getUSCurDay():
	day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
	day = datetime.now(timezone('US/Eastern')).weekday()
	return day_name[day]

def getCurDay():
	day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
	day = datetime.today().weekday()
	return day_name[day]

def getData(page, prevData):
	try:
		time = getCurTime()
		content = BeautifulSoup(page.content, 'html.parser')

		priceHeader = content.find(id='quote-header-info')
		
		name = priceHeader.find('h1', attrs={'data-reactid':'7'})
		price = priceHeader.find('span', attrs={'data-reactid':'14'})
		
		name = name.text
		price = re.sub("[^\d\.]","", price.text)
		price= float(price)

		if(prevData):
			margin = round((((price - prevData["curPrice"]) / prevData["curPrice"])*100), 2)
		else:
			margin = 0
			
		if prevData :
			data = {
				"time": time,
				"name": name,
				"prevPrice": prevData["curPrice"],
				"curPrice": price,
				"margin": margin,
			}
		else:
			data = {
				"time": time,
				"name": name,
				"prevPrice": price,
				"curPrice": price,
				"margin": margin,
			}

		return data

	except:
		print("Stock can't be find")
		sys.exit()
	
	
def toString(data):
	output = ""

	time = data["time"]
	name = data["name"]
	curPrice = str(data["curPrice"])
	prevPrice = str(data["prevPrice"])
	margin = data["margin"]

	name = colored(name, 'blue')
	
	diff = round(float(curPrice) - float(prevPrice),2)
	if(diff > 0):
		
		margin =" (" +  "+" + str(margin) + "%" + ")"
		diff = colored(diff, 'green')
		margin = colored(margin, 'green')
		output = time + "\n" + name + "\n" + "Previous Price: " + prevPrice + "\n" + "Current Price: " + curPrice + " " + diff + margin +  "\n"
	elif(diff == 0):
		diff = ""
		margin = ""
		margin = margin
		output = time + "\n" + name + "\n" + "Previous Price: " + prevPrice + "\n" + "Current Price: " + curPrice + margin +"\n"
	else:
		margin =" (" +   str(margin) + "%" + ")"
		diff = colored(diff, 'green')
		margin = colored(margin, 'red')
		output = time + "\n" + name + "\n" + "Previous Price: " + prevPrice + "\n" + "Current Price: " + curPrice + " " + diff  + margin +  "\n"
	  

	return output  


def main(argv):

	if(len(argv) == 1):
		raise Exception("Please enter the code of thestock you wanted to track")

	if(len(argv) > 2):
		raise Exception("Only one arguments is allowed")
	
 	
	stockCode = argv[1]

	url = f"https://in.finance.yahoo.com/quote/{stockCode}?p={stockCode}&.tsrc=fin-srch"

	data = {}
	
	print("Local time: ", getCurDay(), getCurDate(), getCurTime(), "\n")
	print("America time: ", getUSCurDay(), getUSCurDate(),   getCurUSTime(), "\n")

	while(closed()):
		americaDate = datetime.now(timezone('US/Eastern'))
		localDate = datetime.now()
		
		XLK = getPage(url)
		data = getData(XLK, data)

		print(toString(data))
			
		time.sleep(3)


if __name__ == "__main__":
	main(sys.argv)

