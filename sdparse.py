import os.path

class Poke():
	def __init__(self, name):
		self.name = name
		self.hasNick = False
		self.nick = ""
		self.moves = []
		self.item = "unknown"
		self.ability = "unknown"

pokes = []
name = raw_input( "Who do you want to track: " )
nameLen = len(name.split(' '))
team = raw_input( "What team is the player on: " )
rank = raw_input( "What rank is the battle? (grunt/admin/leader): " )
filename = raw_input( "Enter file to read: " )
currentPoke = 0 # Index for current Pokemon
sendMessage = [] # Message that is printed when a Pokemon is sent out
attMessage = [] # Message that is printed when a Pokemon attacks.
sendSplit = 0
attSplit = 0
replay = ""

def getPokeList(line, pokes):
	pokes.append( Poke(line.split(' ')[nameLen + 1]) )
	pokes.append( Poke(line.split(' ')[nameLen + 3]) )
	pokes.append( Poke(line.split(' ')[nameLen + 5]) )
	pokes.append( Poke(line.split(' ')[nameLen + 7]) )
	pokes.append( Poke(line.split(' ')[nameLen + 9]) )
	pokes.append( Poke(line.split(' ')[nameLen +11]) )
	#Removes \r\n from last pokemon
	pokes[5].name = pokes[5].name.rstrip()

def setCurrentPoke(line, pokes, sendSplit):
	# Used to index current pokemon
	curr = 0
	# Used to index name of pokemon in case of nicknames
	indexOfName = 0 
	# Go through each word looking for the name of a pokemon
	# We go through by word instead of looking at the last word
	# so that we can find the length of nicknames with indexOfName
	for word in line.split(' '):
		for e in pokes:
			# Checks for names without nicknames but sets
			# nick to it's own name for easier checks
			# later on.
			if e.name + "!\r\n" == word:
				e.nick = e.name
				return curr
			# Names found like this mean there is a
			# nickname somewhere
			elif "(" + e.name +")!\r\n" == word:
				if not e.hasNick:
					for i in range(sendSplit, indexOfName):
						e.nick += line.split(' ')[i] + " "
					# Removes trailing whitespace
					e.nick = e.nick.rstrip()
					e.hasNick = True
				return curr
			else:
				curr += 1
		curr = 0
		indexOfName += 1
	return curr

def writeTeam(filename, replay, pokes, new):
	with open(filename, 'w' if new else 'a' ) as outfile:
		outfile.write("Replay - " + replay + "\n\n")
		for e in pokes:
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

def appendTeam(filename, replay, pokes):
	with open(filename, 'a') as outfile:
		outfile.write("\n\n====================\n\n")
	writeTeam(filename, replay, pokes, False)

with open(filename, "r") as infile:
	for line in infile:
		# Determines if the player has POV by looking for the phrase
		# Battle bewtween PlayerA and PlayerB started!
		# If we find name at index 2, then they have POV.		
		if line.split(' ')[0:2] == ['Battle', 'between']:
			if line.split(' ')[2] == name:
				sendMessage.append("Go!")
				sendSplit = 1
				attMessage.append("")
				attSplit = 0
			else:
				sendMessage.append(name)
				sendMessage.append( "sent" )
				sendMessage.append( "out" )
				# Takes into account names with spaces
				sendSplit = nameLen + len(sendMessage) - 1
				attMessage.append("The")
				attMessage.append("opposing")
				attSplit = 2

		# Looks for list of name's pokemon and stores them.
		# Have to make the line you check is at least as long as
		# the player's name. Then if the player has a name with
		# multiple words, just check the last one for the 's.
		# Should catch the first instance as the team immediately.
		# If anyone types their name with a 's and it catches again
		# we'll only pay attention to the first 6 instances so
		# it won't matter.
		if len(line.split(' ')) > nameLen-1:
			if name.split(' ')[nameLen-1] + "'s" == \
			line.split(' ')[nameLen-1]:
				getPokeList(line, pokes)

		# Find the current poke. If the pattern maches,
		# it's a switch line. First check looks for the
		# matching opening line. Second check looks for
		# the name of the pokemon.
		if sendMessage == line.split(' ')[0:sendSplit]:
			currentPoke = setCurrentPoke(line, pokes, sendSplit)

		# Looks to see if the current pokemon uses a new move
		if ' '.join(attMessage) in line and " used " in line:
			if pokes[currentPoke].nick in line:
				indexOfUsed = 0
				for e in line.split(' '):
					indexOfUsed += 1
					if e == "used":
						break
				if ' '.join(line.split(' ')[indexOfUsed:]).rstrip() not in pokes[currentPoke].moves:
					newMove = line.split(' ')[indexOfUsed:]
					newMove = ' '.join(newMove).rstrip()
					pokes[currentPoke].moves.append(newMove)

		# Gets the replay url
		if line.split(':')[0] == "http":
			replay = line.rstrip()

filename = "./" + team + "/" + rank + "/" + name + ".txt"
if os.path.isfile(filename):
	appendTeam(filename, replay, pokes)
else:
	writeTeam(filename, replay, pokes, True)