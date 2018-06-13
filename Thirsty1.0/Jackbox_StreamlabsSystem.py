# Imports
import sys
import datetime
import os
import codecs
import json
import time
import shutil
import math

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Jackbox Stuff"
Website = "https://www.StreamlabsChatbot.com"
Description = "!jackbox [code]| ???"
Creator = "Cactus_Plant"
Version = "1.0.0.0"

m_Command = "!jackbox"
m_CooldownSeconds = 10
m_CommandPermission = "moderator"
m_CommandInfo = ""
code = "XXXX"

patrons = {}
wager_time = datetime.datetime.now() - datetime.timedelta(seconds=60)
can_wager = False


def Init():
	return

def Execute(data):
	global code
	global patrons
	global can_wager
	global wager_time

	if data.IsChatMessage() and data.IsWhisper():
		if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
			code = data.GetParam(1)
			Parent.SendTwitchMessage("CODE UPDATED! The room code is | %s |! You can join at Jackbox.tv ! Be sure to click the gear in the top left and log in with twitch!" % code)
	elif data.IsChatMessage():
		if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,"everyone",m_CommandInfo):
			Parent.SendTwitchMessage("Come and join the fun! The room code is | %s |! You can join at Jackbox.tv ! Be sure to click the gear in the top left and log in with twitch!" % code)

		if data.GetParam(0).lower() == "!openwager" and Parent.HasPermission(data.User,"caster",m_CommandInfo):
			OpenWager()
			Parent.SendTwitchMessage("-----WAGERING OPEN!-----")

		if data.GetParam(0).lower() == "!payout" and Parent.HasPermission(data.User,"caster",m_CommandInfo):
			Payout(data.GetParam(1).lower())

		if data.GetParam(0).lower() == "!wager":
			if can_wager == True:
				Wager(data)
			

	return #End function
	
def Tick():
	global patrons
	global can_wager
	global wager_time
	if datetime.datetime.now() > wager_time and can_wager == True:
		can_wager = False
		Parent.SendTwitchMessage("-----WAGERING CLOSED-----")
	return

def Unload():
 #Triggers when the bot closes / script is reloaded E.G. Dump SQL
 return

def Wager(data):

	global patrons
	global can_wager
	global wager_time
	if data.IsChatMessage():
		wager = 0
		try:
			wager = abs(int(data.GetParam(2)))
		except:
			Parent.SendTwitchMessage("/w %s ERROR - Please enter a valid number for wager" % (data.User))
			return

		#Check Balance
		if Parent.GetPoints(data.User) >= wager:
			pass
		else:
			Parent.SendTwitchMessage("/w %s Insufficent Balance for wager. Balance == [%s], wager total == [%s]" % (data.User, str(Parent.GetPoints(data.user)),str(wager)))
			return
		if data.GetParamCount() >= 3:
			if data.User in patrons:
				patrons[data.User].Wager(data.GetParam(1), wager)
				Parent.RemovePoints(data.User, wager)
				Parent.SendTwitchMessage("/w %s Wager complete, total wager on %s: %s - Remaining Honeycombs == [%s]" % (data.User, data.GetParam(1),
																											 str(patrons[data.User].GetTotalWager(data.GetParam(1).lower())),str(Parent.GetPoints(data.User))))
			else:
				patrons[data.User] = Patron(data.User);
				patrons[data.User].Wager(data.GetParam(1), wager)
				Parent.RemovePoints(data.User, wager)
				Parent.SendTwitchMessage("/w %s New Wager complete, total wager on %s: %s - Remaining Honeycombs == [%s]" % (data.User, data.GetParam(1), 
																												 str(patrons[data.User].GetTotalWager(data.GetParam(1).lower())),str(Parent.GetPoints(data.User))))


def Payout(target):
	global patrons
	global can_wager
	global wager_time
	winner_payout = 0
	for patron in patrons:
		for key in patrons[patron].wagers:
			win_award = math.floor(patrons[patron].wagers[key]*0.1)
			winner_payout += win_award
		if target in patrons[patron].wagers:
			award = math.floor(patrons[patron].wagers[target]*1.5)
			Parent.AddPoints(patrons[patron].user,  award)
			Parent.SendTwitchMessage("/w %s Congratulations! Your wager on %s earned you [%s] Honeycombs! New Balance: [%s]" % (patrons[patron].user, target, str(award),str(Parent.GetPoints(patrons[patron].user))))

	Parent.AddPoints(target,  winner_payout)
	Parent.SendTwitchMessage("/w %s Congratulations! You won this game of jackbox and earned [%s] Honeycombs! New Balance: [%s]" % (target, str(winner_payout),str(Parent.GetPoints(target))))

	patrons.clear()

def OpenWager():
	global patrons
	global can_wager
	global wager_time
	wager_time = datetime.datetime.now() + datetime.timedelta(seconds=60)
	can_wager = True
	return

class Patron():
	def __init__(self,user):
		self.user = user
		self.wagers = {} # [target] [value]

	def Wager(self, target, value):
		#Add to existing or create new wager
		if target.lower() in self.wagers:
			self.wagers[target.lower()] += value
		else:
			self.wagers[target.lower()] = value

	def GetTotalWager(self, w):
		if w in self.wagers:
			return self.wagers[w]
		else: return -1
