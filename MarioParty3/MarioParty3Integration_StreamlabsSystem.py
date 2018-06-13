
#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import datetime
import os
import codecs
import json
import time
import shutil
import random

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "MP3 Interative"
Website = "https://www.StreamlabsChatbot.com"
Description = "Application for the Mario Party 3 Interactivity Integration"
Creator = "Cactus_Plant"
Version = "2.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
order_number = 0

cfd = "C:\\Users\\Cactus\\AppData\\Roaming\\Streamlabs\\Streamlabs Chatbot\\Services\\Scripts\\MarioParty3\\commands.txt"
out_log = "C:\\Users\\Cactus\\AppData\\Roaming\\Streamlabs\\Streamlabs Chatbot\\Services\\Scripts\\MarioParty3\\output.txt"
dict_item_costs = {0:25,1:25,2:25,3:25,4:25,5:25,6:25,7:25,8:25,9:35,10:35,11:50,12:40,13:25,14:50,15:40,16:35,17:50,18:100}
command_list = ["coinsup","coinsdown","starsup","starsdown","giveitem","takeitem","reverse","adjustroll"]
commands_global = ["reverse"]
commands_direct = ["coinsup","coinsdown","starsup","starsdown","giveitem","takeitem","adjustroll"]

next_sale = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(300, 300))
half_off = False
end_sale = False
#---------------------------------------
# Order Class
#---------------------------------------
class Order():
	user = ""
	command = ""
	target = ""
	value = 0
	type = ""
	def __init__(self, user,command,target,value,type):
		self.user = user
		self.command = command
		self.target = int(target)
		self.value = int(value)
		self.type = type

	def getCost(self):
		if self.command == "coinsup": return abs(self.value * 2)
		elif self.command == "coinsdown":return abs(self.value * 2)
		elif self.command == "starsup":return abs(self.value*100)
		elif self.command == "starsdown":return abs(self.value*100)
		elif self.command == "giveitem":return abs(dict_item_costs[self.value])
		elif self.command == "takeitem": return 50
		elif self.command == "reverse": return 50
		elif self.command == "adjustroll": return abs(self.value * 2)



#---------------------------------------
# [Required] Intialize Data (Only called on Load) and Tick Function
#---------------------------------------
def Tick():
	global half_off
	global next_sale
	#if next_sale < datetime.datetime.now():
	#	HalfOff()

	#if end_sale < datetime.datetime.now() and half_off == True:
	#	half_off = False
	#	Parent.SendTwitchMessage("----------HALF OFF ORDERS NOW OVER----------")
	return

def Init():
	order_mumber = 0

def Unload():
 return

def HalfOff():
	global half_off
	global next_sale
	half_off = True
	next_sale = datetime.datetime.now() + datetime.timedelta(seconds=60)
	Parent.SendTwitchMessage("----------HALF OFF ORDERS FOR 60 SECONDS!----------")

#---------------------------------------
# [Required] Begin actual coding
#---------------------------------------

def Execute(data):
	global order_number
	if data.IsChatMessage() and data.IsFromTwitch():
		if data.GetParam(0).lower() == "!order":
			order = CreateOrder(data)
			OrderExecution(order)

def CreateOrder(data):
	try:
		
		name = data.GetParam(1).lower()
		type = ""
		if name not in command_list:
			Parent.SendTwitchWhisper(data.User, "[ERROR] Invalid Command, please enter a valid command")
			return

		if name in commands_direct:
			type = "direct"
		elif name in commands_global:
			type = "global"

		if type == "global":
			order = Order(data.User,data.GetParam(1), 0,0,type)
			return order

		elif type == "direct":
			
			if data.GetParamCount() >= 4:
				#Error Checking
				player = 0
				value = 0
				try:
					player = int(data.GetParam(2))
				except:
					Parent.SendTwitchWhisper(data.User, "[ERROR T1E] Player value for command must be a number")

				try:
					value = int(data.GetParam(3))
				except:
					Parent.SendTwitchWhisper(data.User, "[ERROR T2E] Value for command must be a number")

				if player < 0 or player > 4:
					Parent.SendTwitchWhisper(data.User, "[ERROR 107T] Invalid number for player. Must be 1 2 3 or 4")
					return

				if name == "coinsup" or name == "coinsdown":
					if value < 1 or value > 50:
						Parent.SendTwitchWhisper(data.User, "[ERROR] invalid value for command [%s] - Must be between 1 and 50" % (name))
						return

				if name == "starsup" or name == "starsdown":
					if value < 1 or value > 10:
						Parent.SendTwitchWhisper(data.User, "[ERROR] invalid value for command [%s] - Must be between 1 and 10" % (name))
						return

				if name == "giveitem" or name == "takeitem":
					if value < 0 or value > 18:
						Parent.SendTwitchWhisper(data.User, "[ERROR] invalid value for command [%s] - Must be between 0 and 18" % (name))
						return

				if name == "adjustroll":
					if value < -35 or value > 35:
						Parent.SendTwitchWhisper(data.User, "[ERROR] invalid value for command [%s] - Must be between -35 and 35" % (name))
						return

				#END ERROR SECTION FOR DIRECT


				order = Order(data.User, name, player,value,type)
				return order
	except:
		Parent.SendTwitchWhisper(data.User, "[ERROR 40E] Invalid Command, please enter a valid command")

def OrderExecution(order):
	global half_off
	global order_number
	cost = int(order.getCost())/2 if half_off else order.getCost()
	if int(Parent.GetPoints(order.user)) >= cost:
		with open(cfd, 'a+') as file:
			order_number = order_number + 1
			strnum = (str(datetime.date.today())+"_"+str(order_number))
			file.write(
				"%s;%s;%s;%s;%s\n" 
				% (strnum,str(order.user),str(order.command),str(order.target),str(order.value)))

			
							
		with open(out_log, 'a+') as file:
			Parent.RemovePoints(order.user, cost)
			Parent.SendTwitchWhisper(order.user, "Order for command: %s successful. | Order number: %s | Remaining balance [%s] Honeycombs" % (order.command, strnum, str(Parent.GetPoints(order.user))))
			if order.command == "coinsup":
				file.write("%s has given player %s [%s] coins!\n" % (order.user,str(order.target), str(order.value)))
			elif order.command == "coinsdown":
				file.write("%s has taken [%s] coins from player %s!\n" % (order.user, str(order.value), str(order.target)))
			elif order.command == "starsup":
				file.write("%s has gifted [%s] stars to player %s!\n" % (order.user, str(order.value), str(order.target)))
			elif order.command == "starsdown":
				file.write("%s has stolen [%s] stars from player %s!\n" % (order.user, str(order.value), str(order.target)))
			elif order.command == "giveitem":
				file.write("%s has given an item to player %s!\n" % (order.user,str(order.target)))
			elif order.command == "takeitem":
				file.write("%s has taken an item from player %s!\n" % (order.user,str(order.target)))
			elif order.command == "reverse":
				file.write("%s has queued up a reverse curse on the players! \n" % (order.user))
			elif order.command == "adjustroll":
				file.write("%s has adjusted player %s's next roll by [%s]!\n" % (order.user,str(order.target), str(order.value)))

		
	else: Parent.SendTwitchWhisper(order.user, "[ERROR] You only have %s Honeycombs, you require %s for that command." % (str(Parent.GetPoints(order.user)), str(cost)))

