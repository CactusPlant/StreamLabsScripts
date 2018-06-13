
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
ScriptName = "Pokemon Nuzlocke Updater"
Website = "https://www.StreamlabsChatbot.com"
Description = "!pkmn $slot $pokemon $name[Renames pokemon and updates picture]"
Creator = "Cactus_Plant"
Version = "1.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
m_Response = "This is a test message"
m_Command = "!pkmn"
m_CooldownSeconds = 10
m_CommandPermission = "moderator"
m_CommandInfo = ""

path_pokemon = "C:\\Users\\Cactus\\Documents\\Stream\\pokemon"
path_obs_image = "C:\\Users\\Cactus\\Documents\\Stream\\ScreenPKMN"

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------

def Init():
 return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global m_Response 
	m_Response = "Command Executed Master"
	if data.IsChatMessage() and data.IsFromTwitch() and data.IsWhisper():
		if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
			SwapSlot(data)
			# -Send Message- Parent.SendTwitchMessage(m_Response)

	return

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return

def Parse(parseString,user,target,message):
 if "$myparameter" in parseString:
  return parseString.replace("$myparameter","I am a cat!")
 return parseString

def Unload():
 #Triggers when the bot closes / script is reloaded E.G. Dump SQL
 return

def SwapSlot(data):
	#Move images
	name = "empty"
	for filename in os.listdir(path_pokemon):
		if data.GetParam(2).lower() in filename.lower():
			name = filename
			shutil.copy(path_pokemon + "\\" + filename,path_obs_image + "\\" + data.GetParam(1) + ".png")

			with open(path_obs_image +"\\"+ data.GetParam(1) + ".txt", 'w') as file:
				file.write(data.GetParam(3))

	
	#Rename files
	return