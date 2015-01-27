import os.path

class Poke():
	def __init__(self, name):
		self.name = name
		self.hasNick = False
		self.nick = ""
		self.moves = []
		self.item = "unknown"
		self.ability = "unknown"

class Player():
	def __init__(self, name, team):
		self.name = name
		# The number of words in the player's name
		self.nameLen = len(name.split(' '))
		self.pokes = []
		self.currentPoke = 0
		self.team = team
		self.sendMessage = []
		self.sendSplit = 0
		self.attMessage = []
		self.attSplit = 0

name = raw_input( "What is the name of the player with POV: " )
team = raw_input( "What team is " + name + " on: " )
povPlayer = Player(name, team)
povPlayer.sendMessage.append("Go!")
povPlayer.sendSplit = 1
povPlayer.attMessage.append("")
povPlayer.attSplit = 0

name = raw_input( "What is the name of the opposing player: " )
team = raw_input( "What team is " + name + " on: " )
oppPlayer = Player(name, team)
for i in range(0, oppPlayer.nameLen):
	oppPlayer.sendMessage.append(oppPlayer.name.split(' ')[i])
oppPlayer.sendMessage.append("sent")
oppPlayer.sendMessage.append("out")
oppPlayer.sendSplit = len(oppPlayer.sendMessage)
oppPlayer.attMessage.append("The")
oppPlayer.attMessage.append("opposing")
oppPlayer.attSplit = 2

rank = raw_input( "What rank is the battle? (grunt/admin/leader): " )
filename = raw_input( "Enter file to read: " )
replay = ""

def getPokeList(line, player):
	pokeList = line.split(":")[1].split('/')
	player.pokes.append( Poke(pokeList[0].strip()) )
	player.pokes.append( Poke(pokeList[1].strip()) )
	player.pokes.append( Poke(pokeList[2].strip()) )
	player.pokes.append( Poke(pokeList[3].strip()) )
	player.pokes.append( Poke(pokeList[4].strip()) )
	player.pokes.append( Poke(pokeList[5].strip()) )

def setCurrentPoke(line, player):
	# Used to index current pokemon
	curr = 0
	# Used to index name of pokemon in case of nicknames
	indexOfName = 0 
	# Go through each word looking for the name of a pokemon
	# We go through by word instead of looking at the last word
	# so that we can find the length of nicknames with indexOfName
	# We also set nicknames to their normal names so that finding
	# moves used is easier.
	for word in line.split(' '):
		for e in player.pokes:
			# This section only applies to Mr. Mime and Mime Jr.
			# As they are the only Pokemon with 2 word names.
			# Should probably find a way to clean this up and not
			# have the code be split/duplicated.
			if len(e.name.split(' ')) > 1:
				if e.name.split(' ')[1] + "!\r\n" == word:
					e.nick = e.name
					return curr
				# Names found like this mean there is a
				# nickname somewhere
				elif e.name.split(' ')[1] +")!\r\n" == word:
					if not e.hasNick:
						for i in range(player.sendSplit, indexOfName-1):
							e.nick += line.split(' ')[i] + " "
						# Removes trailing whitespace
						e.nick = e.nick.rstrip()
						e.hasNick = True
					return curr
			# This section applies to all other Pokemon
			elif e.name + "!\r\n" == word:
				e.nick = e.name
				return curr
			# Names found like this mean there is a
			# nickname somewhere
			elif "(" + e.name +")!\r\n" == word:
				if not e.hasNick:
					for i in range(player.sendSplit, indexOfName):
						e.nick += line.split(' ')[i] + " "
					# Removes trailing whitespace
					e.nick = e.nick.rstrip()
					e.hasNick = True
				return curr
			elif "(" + e.name + "-Mega)!\r\n" == word:
				return curr
			curr += 1
		curr = 0
		indexOfName += 1
	print "Couldn't find the right Pokemon in " + line
	return curr

def getPhazedPoke(line, player):
	curr = 0
	for e in player.pokes:
		if e.name + " " in line:
			e.nick = e.name
			return curr
		elif "(" + e.name + ")" in line:
			if not e.hasNick:
				e.nick = line.split('(')[0].rstrip()
				e.hasNick = True
			return curr
		curr += 1
	return 0

def addMove(line, player):
	indexOfUsed = 0
	for e in line.split(' '):
		indexOfUsed += 1
		if e == "used":
			break
	if ' '.join(line.split(' ')[indexOfUsed:]).rstrip('!\r\n') not in player.pokes[player.currentPoke].moves:
		newMove = line.split(' ')[indexOfUsed:]
		newMove = ' '.join(newMove).rstrip('!\r\n')
		player.pokes[player.currentPoke].moves.append(newMove)

def writeTeam(filename, replay, player, new):
	with open(filename, 'w' if new else 'a' ) as outfile:
		outfile.write("Replay - " + replay + "\n\n")
		for e in player.pokes:
			if e.hasNick:
				outfile.write(e.name + " (" + e.nick + ") @ " + e.item + "\n")
			else:
				outfile.write(e.name + " @ " + e.item + "\n")
			outfile.write("Ability: " + e.ability + "\n")
			for i in range(0, len(e.moves)):
				outfile.write("- " + e.moves[i] + "\n")
			for i in range(len(e.moves), 4):
				outfile.write("- \n")
			outfile.write("\n")

def appendTeam(filename, replay, player):
	with open(filename, 'a') as outfile:
		outfile.write("\n\n====================\n\n")
	writeTeam(filename, replay, player, False)

with open(filename, "r") as infile:
	prevLine = ""
	twoLinesBack = ""
	for line in infile:
		# Tries to find the players' last word in their name with a
		# 's after it. By finding this at the earliest index we find
		# the line of text with the list of pokemon.
		if len(line.split(' ')) > povPlayer.nameLen-1:
			if povPlayer.name.split(' ')[povPlayer.nameLen-1] + "'s" == \
			line.split(' ')[povPlayer.nameLen-1]:
				getPokeList(line, povPlayer)
		if len(line.split(' ')) > oppPlayer.nameLen-1:
			if oppPlayer.name.split(' ')[oppPlayer.nameLen-1] + "'s" == \
			line.split(' ')[oppPlayer.nameLen-1]:
				getPokeList(line, oppPlayer)
		
		# By looking for the send messages in the begginning of the
		# lines, we can find when Pokemon are switched out.
		# The function then searches the line to find the name and
		# nickname of the pokemon being sent out.
		if povPlayer.sendMessage == \
		line.split(' ')[0:povPlayer.sendSplit]:
			povPlayer.currentPoke = setCurrentPoke(line, povPlayer)

		if oppPlayer.sendMessage == \
		line.split(' ')[0:oppPlayer.sendSplit]:
			oppPlayer.currentPoke = setCurrentPoke(line, oppPlayer)

		# Looks to see if the current pokemon uses a new move.
		# This could be vulnerable to tampering via chat. Will
		# need to test, but the ":" not in line should help avoid
		# it.
		if " used " in line and ":" not in line:
			if ' '.join(oppPlayer.attMessage) in line:
				#print oppPlayer.pokes[oppPlayer.currentPoke].nick
				if oppPlayer.pokes[oppPlayer.currentPoke].nick in line:
					addMove(line, oppPlayer)
			else:
				if povPlayer.pokes[povPlayer.currentPoke].nick in line:
					addMove(line, povPlayer)

		if "was dragged out!" in line and ":" not in line:
			if " used " in prevLine:
				if "The opposing" in prevLine:
					povPlayer.currentPoke = getPhazedPoke(line, povPlayer)
				else:
					oppPlayer.currentPoke = getPhazedPoke(line, oppPlayer)
			elif " used " in twoLinesBack:
				if "The opposing" in twoLinesBack:
					povPlayer.currentPoke = getPhazedPoke(line, povPlayer)
				else:
					oppPlayer.currentPoke = getPhazedPoke(line, oppPlayer)

		# Gets the replay url
		if line.split(':')[0] == "http":
			replay = line.rstrip()
		twoLinesBack = prevLine
		prevLine = line

filename = \
"./" + povPlayer.team + "/" + rank + "/" + povPlayer.name + ".txt"

if os.path.isfile(filename):
	appendTeam(filename, replay, povPlayer)
else:
	writeTeam(filename, replay, povPlayer, True)

filename = \
"./" + oppPlayer.team + "/" + rank + "/" + oppPlayer.name + ".txt"

if os.path.isfile(filename):
	appendTeam(filename, replay, oppPlayer)
else:
	writeTeam(filename, replay, oppPlayer, True)