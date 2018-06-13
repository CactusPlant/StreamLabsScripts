
	


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

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "MP3 Interative"
Website = "https://www.StreamlabsChatbot.com"
Description = "Application for the Mario Party 3 Interactivity Integration"
Creator = "Cactus_Plant"
Version = "1.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
m_response = ""
m_Command = "!order"
m_CooldownSeconds = 0
m_CommandPermission = "everyone"
m_CommandInfo = ""

command_list = ["coinsup","coinsdown","starsup","starsdown","giveitem","takeitem","reverse","adjustroll", "bank", "chancetime"]
order_number = 0
cfd = "C:\\Users\\Cactus\\AppData\\Roaming\\Streamlabs\\Streamlabs Chatbot\\Services\\Scripts\\MarioParty3\\commands.txt"
out_log = "C:\\Users\\Cactus\\AppData\\Roaming\\Streamlabs\\Streamlabs Chatbot\\Services\\Scripts\\MarioParty3\\output.txt"

dict_item_costs = {0:25,1:25,2:25,3:25,4:25,5:25,6:25,7:25,8:25,9:35,10:35,11:50,12:40,13:25,14:50,15:40,16:35,17:50,18:100}

#---------------------------------------
# Order Class
#---------------------------------------
class Order():
	user = ""
	command = ""
	target = ""
	value = 0
	def __init__(self, user,command,target,value=0, value2=0):
		self.user = user
		self.command = command
		self.target = int(target)
		self.value = int(value)
		self.value2 = value2

	def getCost(self):
		if self.command == "coinsup": return self.value * 2
		elif self.command == "coinsdown":return self.value * 2
		elif self.command == "starsup":return self.value*100
		elif self.command == "starsdown":return self.value*100
		elif self.command == "giveitem":return dict_item_costs[self.value]
		elif self.command == "takeitem": return 50
		elif self.command == "reverse": return 25
		elif self.command == "adjustroll": return self.value * 2



#---------------------------------------
# [Required] Intialize Data (Only called on Load) and Tick Function
#---------------------------------------
def Tick(): 
	return

def Init():
	order_mumber = 0

def Unload():
 return

#---------------------------------------
# [Required] Begin actual coding
#---------------------------------------

def Execute(data):
	global order_number
	if data.IsChatMessage() and data.IsFromTwitch():
		if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command):
			#Checking order for requirements ------------------------------
			if data.GetParam(1).lower() not in command_list: 
				Parent.SendTwitchMessage("/w %s ERROR[Invalid Command] You either entered an invalid command, or did not enter one at all" % data.User)
				return
			try:
				int(data.GetParam(2))
			except:
				Parent.SendTwitchMessage("/w %s ERROR:[Invalid Player] Please enter either 1,2,3 or 4 as your player option" % data.User)
				return
			try:
				if not(int(data.GetParam(3)) < 51 and int(data.GetParam(3)) >= 0) and (data.GetParam(1) != "adjustroll") and (data.GetParam(1) != "bank"): 
					Parent.SendTwitchMessage("/w %s ERROR:[Invalid Value] Please enter a valid number for the command [%s] -Must be less than 50 and 0 or greater-" % (data.User, data.GetParam(1)))
					return
				if int(data.GetParam(3)) <= 0 and data.GetParam(1) == "bank":
					Parent.SendTwitchMessage("/w %s ERROR:[Invalid Value] Please enter a valid number for the command [%s] -Must be 0 or greater-" % (data.User, data.GetParam(1)))

			except:
				Parent.SendTwitchMessage("/w %s ERROR:[Invalid Value] Please enter a valid number for the command [%s]" % (data.User, data.GetParam(1)))
				return

			try:
				if data.GetParam(1) == "giveitem" and (int(data.GetParam(3)) < 0 or int(data.GetParam(3)) > 18):
					Parent.SendTwitchMessage("/w %s Please enter a number between 0 and 18 for command %s" % (data.User, data.GetParam(1)))
					return
			except:
				Parent.SendTwitchMessage("/w %s Please enter a number between 0 and 18 for command %s" % (data.User, data.GetParam(1)))
			try:
				if data.GetParam(1) == "adjustroll" and (int(data.GetParam(3)) < -39 or int(data.GetParam(3)) > 39):
					Parent.SendTwitchMessage("/w %s Please enter a number between -39 and 39 for command %s" % (data.User, data.GetParam(1)))
					return
			except:
				Parent.SendTwitchMessage("/w %s Please enter a number between -39 and 39 for command %s" % (data.User, data.GetParam(1)))
				return



			if data.GetParamCount() == 4:
					order = Order(data.User,data.GetParam(1).lower(), data.GetParam(2),data.GetParam(3))


					if int(Parent.GetPoints(data.User)) >= order.getCost():

						#Check if the target is valid
						if order.target <= 4 and order.target > 0:
							#Formulate and post to log for LUA script to read
							

							with open(cfd, 'a+') as file:
								order_number = order_number + 1
								strnum = (str(datetime.date.today())+"_"+str(order_number))
								file.write(
									"%s;%s;%s;%s;%s\n" 
								   % (strnum,str(order.user),str(order.command),str(order.target),str(order.value)))
								
							with open(out_log, 'a+') as file:
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
									file.write("%s has queued up a reverse curse on player %s!\n" % (order.user,str(order.target)))
								elif order.command == "adjustroll":
									file.write("%s has adjusted player %s's next roll by [%s]!\n" % (order.user,str(order.target), str(order.value)))
								elif order.command == "bank":
									file.write("%s has given %s coins to the bank!" % (order.user, str(order.value)))
							
							total = order.getCost()
							if total < 0: total = total * -1;
							Parent.RemovePoints(data.User, total)
							Parent.SendTwitchMessage("/w %s Order for command: %s successful. | Order number: %s | Remaining balance [%s] Honeycombs" % (data.User, order.command, strnum, str(Parent.GetPoints(data.User))))
						else:
							Parent.SendTwitchMessage("/w " + data.User + " Please enter a number between 1 and 4 for player number. Thank you.")
					#Handle Exceptions and failures
					else: Parent.SendTwitchMessage("/w %s  ERROR: You only have %s Honeycombs, you require %s for that command." % (data.User, str(Parent.GetPoints(data.User)), str(abs(order.getCost()))))


