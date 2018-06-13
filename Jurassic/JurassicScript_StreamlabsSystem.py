# Imports
import sys
import datetime
import os
import codecs
import json
import time
import shutil
import csv
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Jurassic World Script"
Website = "https://www.StreamlabsChatbot.com"
Description = "Handles Dinosaur management, feeding, and files"
Creator = "Alex Carroll (aka. Cactus_Plant)"
Version = "0.1.0.0"

response = "Variable"
m_Command = "various"
m_CooldownSeconds = 0
m_CommandPermission = "moderator"
m_CommandInfo = ""

#--------------------------------
#Enums and internal tables
#--------------------------------
hunger_states_enum = {"satiated":6000,"hungry":3000, "starving":0}
dinos = {}
global dir

#--------------------------------
#Script Init
#--------------------------------

def Init():
	global dir
	dir = CreateDinoBase()
	ReadDinos()

	return

#------------------------------------
#Script Execute Function per message.
#------------------------------------
def Execute(data):
	global dir
	AddDino(data)
	InfoDino(data)
	FeedDino(data)
	RemoveDino(data)
	return

#--------------------------------
#Script Tick, occurs ~30/sec
#--------------------------------
def Tick():
	if len(dinos) > 0:
		for dino in dinos:
			dinos[dino].reduceFeed()

	return

def Unload():
 #Triggers when the bot closes / script is reloaded E.G. Dump SQL
 return
#-------------------------------------
#Logic Methods
#-------------------------------------

def AddDino(data):
	if data.IsChatMessage() and data.IsFromTwitch():
		if data.GetParam(0).lower() == "!dinoadd" and Parent.HasPermission(data.User,"moderator",m_CommandInfo) and data.GetParamCount() >= 3:
			name = ""
			for s in range(2, data.GetParamCount()):
				name = name + data.GetParam(s) + " "

			#Remove Excess Space
			name = name[:-1].lower();

			new_dino = Dinosaur(name, data.GetParam(1))
			dinos[new_dino.name] = new_dino
			Parent.SendTwitchMessage(("[UPLOADING...] | " +new_dino.name + " has been added to dinosaur database").upper())
			WriteDino(new_dino)

	return

def InfoDino(data):
	if data.IsChatMessage() and data.IsFromTwitch():
		if data.GetParam(0).lower() == "!dino" and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo) and data.GetParamCount() > 1:
			if len(dinos) > 0:
				name = ""
				for s in range(1, data.GetParamCount()):
					name = name + data.GetParam(s) + " "

				#Remove Excess Space
				name = name[:-1].lower()			
				if name in dinos.keys():
					d = dinos[name]
					hunger = "idfk"
					if d.fed > 12000:
						hunger = "satiated"
					elif d.fed > 6000:
						hunger = "hungry"
					else:
						hunger = "starving"
					Parent.SendTwitchMessage(("[Scan complete] Name: "+d.name+" | Type: "+d.type+" | Hunger: "+hunger).upper())
					

		return

def FeedDino(data):
	if data.IsChatMessage() and data.IsFromTwitch():
		if data.GetParam(0).lower() == "!dinofeed" and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo) and data.GetParamCount() > 1:
			if len(dinos) > 0:
				name = ""
				for s in range(1, data.GetParamCount()):
					name = name + data.GetParam(s) + " "

				#Remove Excess Space
				name = name[:-1].lower()
				if name in dinos.keys():
					d = dinos[name]
					if d.fed < 12000:
						Parent.SendTwitchMessage(("[DISPENSING FOOD...] "+d.name+" has accepted nourishment").upper())
						d.fed = d.fed + 6000
						d.fed = 18000 if d.fed > 18000 else d.fed
					else:
						Parent.SendTwitchMessage(("Food is not necessary | "+d.name+" properly satiated").upper())

def RemoveDino(data):
	if data.IsChatMessage() and data.IsFromTwitch():
		if data.GetParam(0).lower() == "!dinoremove" and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo) and data.GetParamCount() > 1:
			if len(dinos) > 0:
				name = ""
				for s in range(1, data.GetParamCount()):
					name = name + data.GetParam(s) + " "

				#Remove Excess Space
				name = name[:-1].lower()
				if name in dinos.keys():
					
					d = dinos[name]
					Parent.SendTwitchMessage(("RIP: "+d.name).upper())
					RemoveDinoFromFile(d)
					

#--------------------------------
#File IO
#--------------------------------

def ReadDinos():
	global dir
	with open(dir, 'rb') as file:
		keys = ['name', 'type']
		reader = csv.DictReader(file,keys, delimiter=';')
		for row in reader:
			
			new_dino = Dinosaur(row['name'], row['type'])
			dinos[new_dino.name] = new_dino

	return

def WriteDino(dino):
	global dir
	with open(dir, 'a') as file:
		keys = ['name', 'type']
		writer = csv.DictWriter(file, keys, delimiter=';')

		writer.writerow({'name':dino.name, 'type':dino.type})
	return

def RemoveDinoFromFile(dino):
	global dir
	del dinos[dino.name]
	with open(dir, 'w') as file:
		file.seek(0)
		file.truncate()

		keys = ['name', 'type']
		writer = csv.DictWriter(file, keys, delimiter=';')
		writer.writeheader()
		for d in dinos:
			dino = dinos[d]

			writer.writerow({'name':dino.name, 'type':dino.type})

def CreateDinoBase():
	directory = os.path.expanduser("~\My Documents") + "\\StreamLabs Script DB\\"
	if not os.path.exists(directory):
		os.makedirs(directory)
	if not os.path.isfile(directory + "\\dinos.csv"):
		with open(directory+"\\dinos.csv", 'w') as file:
			keys = ['name', 'type']
			writer = csv.DictWriter(file, keys, delimiter=';')

			writer.writeheader()

	return (directory + "\\dinos.csv")

#--------------------------------
#Classes
#--------------------------------


class Dinosaur:
	def __init__(self, n, t):
		self.name = n
		self.type = t
		self.fed = 15000

	def reduceFeed(self):
		if self.fed > 0:
			self.fed -= 1