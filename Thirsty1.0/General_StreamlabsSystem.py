import sys
import datetime
import os
import codecs
import json
import time
import shutil


ScriptName = "Thirsty General Script"
Website = "https://www.StreamlabsChatbot.com"
Description = "General Bot that handles day to day activities"
Creator = "Cactus_Plant"
Version = "1.0.0.0"

m_Command = "!points"
m_CooldownSeconds = 10
m_CommandPermission = "moderator"
m_CommandInfo = ""

def Execute(data):
	if data.IsFromTwitch() and data.IsChatMessage():
		#Returns Honeycomb balance of user without delay.
		if data.GetParam(0).lower() == "!combs":
			Parent.SendTwitchWhisper(data.User, "%s Honeycombs balance: [%s]" %(data.User, GetPoints(data.User)))

def Init():
	pass

def Tick():
	pass

def GetPoints(user):
	return Parent.GetPoints(user)

