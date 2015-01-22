class Poke():
	def __init__(self, name):
		self.name = name
		self.hasNick = False
		self.nick = ""
		self.moves = []
		self.item = ""
		self.ability = ""

pokes = []
name = raw_input( "Who do you want to track: " )
pov = bool( raw_input( 
	"Does that player have POV? Leave blank for false: " ) )
team = raw_input( "What team is the player on: " )
filename = raw_input( "Enter file to read: " )
currentPoke = 0 # Index for current Pokemon
sendMessage = [] # Message that is printed when a Pokemon is sent out
attMessage = [] # Message that is printed when a Pokemon attacks.

if pov:
	sendMessage.append("Go!")
	sendSplit = 1
	attMessage.append("")
	attSplit = 0
else:
	sendMessage.append(name)
	sendMessage.append( "sent" )
	sendMessage.append( "out" )
	# Takes into account names with spaces
	sendSplit = len(name.split(' ')) + len(sendMessage) - 1
	attMessage.append("The")
	attMessage.append("opposing")
	attSplit = 2

with open(filename, "r") as infile:
	for line in infile:
		#print line
		# Looks for list of name's pokemon and stores them.
		# Have to make the line you check is at least as long as
		# the player's name. Then if the player has a name with
		# multiple words, just check the last one for the 's.
		# Should catch the first instance as the team immediately.
		# If anyone types their name with a 's and it catches again
		# we'll only pay attention to the first 6 instances so
		# it won't matter.
		if len(line.split(' ')) > len(name.split(' '))-1:
			if name.split(' ')[len(name.split(' '))-1] + "'s" == \
			line.split(' ')[len(name.split(' '))-1]:
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +1]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +3]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +5]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +7]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +9]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' '))+11]) )
				#Removes \r\n from last pokemon
				pokes[5].name = pokes[5].name[:len(pokes[5].name)-2]
		
		# Find the current poke. If the pattern maches,
		# it's a switch line. First check looks for the
		# matching opening line. Second check looks for
		# the name of the pokemon.
		if sendMessage == line.split(' ')[0:sendSplit]:
			# Used to index current pokemon
			curr = 0
			# Used to index name of pokemon in case of nicknames
			indexOfName = 0 
			# Go through each word looking for the name of a pokemon
			for word in line.split(' '):
				for e in pokes:
					# Checks for names without nicknames but sets
					# nick to it's own name for easier checks
					# later on.
					if e.name + "!\r\n" == word:
						e.nick = e.name
						currentPoke = curr
						break
					# Names found like this mean there is a
					# nickname somewhere
					elif "(" + e.name +")!\r\n" == word:
						if not e.hasNick:
							for i in range(sendSplit, indexOfName):
								e.nick += line.split(' ')[i] + " "
							# Removes trailing whitespace
							e.nick = e.nick[0:len(e.nick)-1]
							e.hasNick = True
						currentPoke = curr
						break
					else:
						curr += 1
				curr = 0
				indexOfName += 1

		# Looks to see if the current pokemon uses a new move
		#if ' '.join(attMessage) in line and \
		#" used " in line:
		# USE THE CURRENT POKE VARIABLE
		if ' '.join(attMessage) in line and " used " in line:
			if pokes[currentPoke].nick in line:
				indexOfUsed = 0
				for e in line.split(' '):
					indexOfUsed += 1
					if e == "used":
						break
				if ' '.join(line.split(' ')[indexOfUsed:]) not in pokes[currentPoke].moves:
					newMove = line.split(' ')[indexOfUsed:]
					newMove = ' '.join(newMove)
					# TODO: remove the !\r\n from moves before
					#       adding it to the text file. Maybe
					#       have a "cleansing" function before
					#		the output. Or fix the above if so
					#		that it can find "Knock Off" instead
					#		of "Knock Off!\r\n"
					pokes[currentPoke].moves.append(newMove)